from typing import Dict, List, Optional, Tuple
import logging
from pathlib import Path

import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import timm
import json

logger = logging.getLogger(__name__)


class SpeciesClassifier:
    """
    Wildlife species classification model using transfer learning.
    
    This implementation uses ResNet50 pre-trained on ImageNet and fine-tuned
    for wildlife species classification. Supports easy model loading,
    inference, and batch processing.
    
    Example Usage:
        # For inference with pre-trained model
        classifier = SpeciesClassifier(model_path="models/wildlife_resnet50.pth")
        prediction = classifier.predict("images/deer.jpg")
        # Returns: {"deer": 0.85, "elk": 0.10, "moose": 0.05}
        
        # For training from scratch
        classifier = SpeciesClassifier.create_model(
            num_classes=10,
            model_name="resnet50"
        )
    """

    def __init__(
        self,
        model_path: Optional[str] = None,
        num_classes: int = 1000,
        model_name: str = "resnet50",
        device: Optional[str] = None,
    ):
        """
        Initialize the species classifier.
        
        Args:
            model_path: Path to saved model weights (.pth file)
            num_classes: Number of species classes
            model_name: Model architecture (resnet50, efficientnet_b0, etc.)
            device: Device to run inference on (cuda/cpu). Auto-detected if None.
        """
        self.model_path = model_path
        self.num_classes = num_classes
        self.model_name = model_name
        
        # Auto-detect device
        if device is None:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)
        
        logger.info(f"Using device: {self.device}")
        
        # Load class names if available
        self.class_names = self._load_class_names()
        
        # Initialize model
        self.model = self._create_model()
        
        # Load weights if provided
        if model_path:
            self._load_weights(model_path)
        else:
            logger.warning("No model path provided - using ImageNet pre-trained weights")
        
        self.model.to(self.device)
        self.model.eval()
        
        # Define image preprocessing
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def _create_model(self) -> nn.Module:
        """Create the model architecture."""
        if self.model_name == "resnet50":
            model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
            # Replace final layer for custom number of classes
            num_features = model.fc.in_features
            model.fc = nn.Linear(num_features, self.num_classes)
        elif self.model_name.startswith("efficientnet"):
            model = timm.create_model(self.model_name, pretrained=True, num_classes=self.num_classes)
        else:
            raise ValueError(f"Unsupported model: {self.model_name}")
        
        return model

    def _load_weights(self, model_path: str):
        """Load model weights from file."""
        try:
            checkpoint = torch.load(model_path, map_location=self.device)
            
            # Handle different checkpoint formats
            if isinstance(checkpoint, dict):
                if 'model_state_dict' in checkpoint:
                    self.model.load_state_dict(checkpoint['model_state_dict'])
                    if 'num_classes' in checkpoint:
                        self.num_classes = checkpoint['num_classes']
                    if 'class_names' in checkpoint:
                        self.class_names = checkpoint['class_names']
                else:
                    self.model.load_state_dict(checkpoint)
            else:
                self.model.load_state_dict(checkpoint)
            
            logger.info(f"Successfully loaded model from {model_path}")
        except Exception as e:
            logger.error(f"Failed to load model weights: {e}")
            raise

    def _load_class_names(self) -> Optional[List[str]]:
        """Load class names from companion JSON file."""
        if not self.model_path:
            return None
        
        # Look for classes.json next to model file
        model_dir = Path(self.model_path).parent
        classes_file = model_dir / "classes.json"
        
        if classes_file.exists():
            try:
                with open(classes_file, 'r') as f:
                    data = json.load(f)
                    return data.get('classes', None)
            except Exception as e:
                logger.warning(f"Could not load class names: {e}")
        
        return None

    def predict(self, image_path: str, top_k: int = 5) -> Dict[str, float]:
        """
        Predict species probabilities for a single image.
        
        Args:
            image_path: Path to the image file
            top_k: Return top K predictions
            
        Returns:
            Dictionary mapping species names to confidence scores (0-1)
            Example: {"deer": 0.85, "elk": 0.10, "moose": 0.03, ...}
        """
        try:
            # Load and preprocess image
            image = Image.open(image_path).convert('RGB')
            image_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            # Run inference
            with torch.no_grad():
                outputs = self.model(image_tensor)
                probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            
            # Get top K predictions
            top_probs, top_indices = torch.topk(probabilities, min(top_k, self.num_classes))
            
            # Create results dictionary
            results = {}
            for prob, idx in zip(top_probs.cpu().numpy(), top_indices.cpu().numpy()):
                if self.class_names and idx < len(self.class_names):
                    class_name = self.class_names[idx]
                else:
                    class_name = f"class_{idx}"
                results[class_name] = float(prob)
            
            return results
            
        except Exception as e:
            logger.error(f"Prediction failed for {image_path}: {e}")
            return {"unknown": 1.0}

    def predict_batch(
        self, 
        image_paths: List[str], 
        batch_size: int = 32,
        top_k: int = 5
    ) -> List[Dict[str, float]]:
        """
        Predict species for multiple images efficiently.
        
        Args:
            image_paths: List of paths to image files
            batch_size: Number of images to process at once
            top_k: Return top K predictions per image
            
        Returns:
            List of prediction dictionaries, one per image
        """
        from tqdm import tqdm
        
        results = []
        
        # Process in batches
        for i in tqdm(range(0, len(image_paths), batch_size), desc="Processing images"):
            batch_paths = image_paths[i:i + batch_size]
            batch_images = []
            
            # Load and preprocess batch
            for path in batch_paths:
                try:
                    image = Image.open(path).convert('RGB')
                    image_tensor = self.transform(image)
                    batch_images.append(image_tensor)
                except Exception as e:
                    logger.error(f"Failed to load {path}: {e}")
                    results.append({"unknown": 1.0})
                    continue
            
            if not batch_images:
                continue
            
            # Create batch tensor
            batch_tensor = torch.stack(batch_images).to(self.device)
            
            # Run inference
            with torch.no_grad():
                outputs = self.model(batch_tensor)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)
            
            # Process each result in batch
            for probs in probabilities:
                top_probs, top_indices = torch.topk(probs, min(top_k, self.num_classes))
                
                batch_result = {}
                for prob, idx in zip(top_probs.cpu().numpy(), top_indices.cpu().numpy()):
                    if self.class_names and idx < len(self.class_names):
                        class_name = self.class_names[idx]
                    else:
                        class_name = f"class_{idx}"
                    batch_result[class_name] = float(prob)
                
                results.append(batch_result)
        
        return results

    @classmethod
    def create_model(
        cls,
        num_classes: int,
        model_name: str = "resnet50",
        pretrained: bool = True
    ) -> 'SpeciesClassifier':
        """
        Create a new model for training.
        
        Args:
            num_classes: Number of species classes to predict
            model_name: Model architecture name
            pretrained: Use ImageNet pre-trained weights
            
        Returns:
            New SpeciesClassifier instance ready for training
        """
        classifier = cls(
            model_path=None,
            num_classes=num_classes,
            model_name=model_name
        )
        return classifier

    def save(self, save_path: str, class_names: Optional[List[str]] = None):
        """
        Save model weights and metadata.
        
        Args:
            save_path: Path to save model (.pth file)
            class_names: Optional list of class names to save
        """
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save model checkpoint
        checkpoint = {
            'model_state_dict': self.model.state_dict(),
            'num_classes': self.num_classes,
            'model_name': self.model_name,
        }
        
        if class_names:
            checkpoint['class_names'] = class_names
        
        torch.save(checkpoint, save_path)
        logger.info(f"Model saved to {save_path}")
        
        # Save class names separately
        if class_names:
            classes_file = save_path.parent / "classes.json"
            with open(classes_file, 'w') as f:
                json.dump({'classes': class_names}, f, indent=2)
            logger.info(f"Class names saved to {classes_file}")

    def get_model_info(self) -> Dict[str, any]:
        """Get model information and statistics."""
        total_params = sum(p.numel() for p in self.model.parameters())
        trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        
        return {
            'model_name': self.model_name,
            'num_classes': self.num_classes,
            'device': str(self.device),
            'total_parameters': total_params,
            'trainable_parameters': trainable_params,
            'model_path': self.model_path,
            'has_class_names': self.class_names is not None,
        }
