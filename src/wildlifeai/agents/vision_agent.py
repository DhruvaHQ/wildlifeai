"""
Vision Agent - Species Detection and Observation Generation

Wraps the ML models and generates structured observations from images.
This is the "eyes" of the cognitive system.
"""
from typing import Dict, Any, Optional, List
from pathlib import Path
import logging

from wildlifeai.agents.base import Agent, Message, MessageBus
from wildlifeai.models import SpeciesClassifier

logger = logging.getLogger(__name__)


class VisionAgent(Agent):
    """
    Vision Agent processes images and generates species observations.
    
    Responsibilities:
    - Load and process wildlife images
    - Run species detection models
    - Generate structured observation records
    - Publish observations to the message bus
    
    Publishes:
    - 'observation' messages for each detected species
    
    Subscribes to:
    - 'process_image' requests
    - 'process_batch' requests
    """
    
    def __init__(
        self,
        message_bus: MessageBus,
        model_path: Optional[str] = None,
        confidence_threshold: float = 0.5
    ):
        self.classifier = None
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        super().__init__("vision_agent", message_bus)
        
    def _setup_subscriptions(self):
        """Subscribe to image processing requests."""
        self.message_bus.subscribe('process_image', self._handle_process_image)
        self.message_bus.subscribe('process_batch', self._handle_process_batch)
    
    def _initialize_model(self):
        """Lazy load the ML model."""
        if self.classifier is None:
            logger.info("Initializing species classifier...")
            self.classifier = SpeciesClassifier(model_path=self.model_path)
            self.update_state('model_loaded', True)
            self.update_state('model_info', self.classifier.get_model_info())
    
    def process(self, message: Message) -> Optional[Message]:
        """Process incoming messages."""
        if message.type == 'process_image':
            return self._handle_process_image(message)
        elif message.type == 'process_batch':
            return self._handle_process_batch(message)
        return None
    
    def _handle_process_image(self, message: Message):
        """Handle single image processing request."""
        self._initialize_model()
        
        image_path = message.data.get('image_path')
        camera_id = message.data.get('camera_id', 'unknown')
        location = message.data.get('location')
        
        if not image_path:
            logger.error("No image_path in message")
            return
        
        try:
            # Run species detection
            predictions = self.classifier.predict(str(image_path), top_k=3)
            
            # Filter by confidence threshold
            top_species = max(predictions.items(), key=lambda x: x[1])
            species_name, confidence = top_species
            
            if confidence >= self.confidence_threshold:
                # Create structured observation
                observation = {
                    'species': species_name,
                    'confidence': float(confidence),
                    'image_path': str(image_path),
                    'camera_id': camera_id,
                    'location': location,
                    'predictions': predictions,
                    'filename': Path(image_path).name
                }
                
                # Publish observation
                self.publish(
                    'observation',
                    observation,
                    metadata={'agent': 'vision', 'type': 'detection'}
                )
                
                logger.info(f"Detected {species_name} ({confidence:.2%}) in {Path(image_path).name}")
                
                # Update statistics
                detections = self.get_state('total_detections', 0)
                self.update_state('total_detections', detections + 1)
            else:
                logger.debug(f"Low confidence detection ({confidence:.2%}) - skipped")
                
        except Exception as e:
            logger.error(f"Vision processing error: {e}")
    
    def _handle_process_batch(self, message: Message):
        """Handle batch image processing request."""
        self._initialize_model()
        
        image_paths = message.data.get('image_paths', [])
        camera_id = message.data.get('camera_id', 'unknown')
        
        if not image_paths:
            logger.error("No image_paths in batch message")
            return
        
        try:
            # Batch prediction
            results = self.classifier.predict_batch(
                [str(p) for p in image_paths],
                batch_size=32
            )
            
            # Process each result
            for image_path, predictions in zip(image_paths, results):
                top_species = max(predictions.items(), key=lambda x: x[1])
                species_name, confidence = top_species
                
                if confidence >= self.confidence_threshold:
                    observation = {
                        'species': species_name,
                        'confidence': float(confidence),
                        'image_path': str(image_path),
                        'camera_id': camera_id,
                        'predictions': predictions,
                        'filename': Path(image_path).name
                    }
                    
                    self.publish('observation', observation)
            
            logger.info(f"Processed batch of {len(image_paths)} images")
            
        except Exception as e:
            logger.error(f"Batch processing error: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get vision agent statistics."""
        return {
            'total_detections': self.get_state('total_detections', 0),
            'model_loaded': self.get_state('model_loaded', False),
            'model_info': self.get_state('model_info', {}),
            'confidence_threshold': self.confidence_threshold
        }
