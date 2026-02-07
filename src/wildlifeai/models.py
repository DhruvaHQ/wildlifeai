from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class SpeciesClassifier:
    """
    Placeholder species classification model.

    This class defines the interface for future ML models.
    Replace this implementation with your own CNN, Vision Transformer,
    or other classification model.
    
    Example Usage:
        classifier = SpeciesClassifier(model_path="path/to/weights.pth")
        prediction = classifier.predict("image.jpg")
        # Returns: {"deer": 0.85, "elk": 0.10, "unknown": 0.05}
    """

    def __init__(self, model_path: str | None = None):
        """
        Initialize the species classifier.
        
        Args:
            model_path: Optional path to pre-trained model weights
        """
        self.model_path = model_path
        self.model = None
        
        if model_path:
            logger.info(f"Model path provided: {model_path}")
            # TODO: Load model here
            # self.model = load_model(model_path)
        else:
            logger.warning("No model path provided - using placeholder predictions")

    def predict(self, image_path: str) -> Dict[str, float]:
        """
        Predict species probabilities for a given image.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary mapping species names to confidence scores (0-1)
            Example: {"deer": 0.85, "elk": 0.10, "unknown": 0.05}
        
        NOTE:
            This is a placeholder implementation. Replace with real ML inference:
            
            Example implementation:
            ```python
            from PIL import Image
            import torch
            
            img = Image.open(image_path)
            img_tensor = self.preprocess(img)
            with torch.no_grad():
                logits = self.model(img_tensor)
                probs = torch.softmax(logits, dim=1)
            return {species: prob for species, prob in zip(self.classes, probs)}
            ```
        """
        # Placeholder prediction (stub)
        return {
            "unknown": 1.0
        }
    
    def predict_batch(self, image_paths: List[str]) -> List[Dict[str, float]]:
        """
        Predict species for multiple images efficiently.
        
        Args:
            image_paths: List of paths to image files
            
        Returns:
            List of prediction dictionaries, one per image
            
        NOTE:
            Override this method to implement batch processing for better performance.
        """
        return [self.predict(path) for path in image_paths]
