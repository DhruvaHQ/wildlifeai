"""
Training utilities for wildlife species classification models.
"""
from typing import Optional, Tuple, Dict, List
from pathlib import Path
import logging

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
from tqdm import tqdm
import json

from wildlifeai.models import SpeciesClassifier

logger = logging.getLogger(__name__)


class WildlifeDataset(Dataset):
    """
    Dataset for wildlife images organized in folders by species.
    
    Expected structure:
        data/
        ├── train/
        │   ├── deer/
        │   │   ├── img1.jpg
        │   │   └── img2.jpg
        │   ├── elk/
        │   └── moose/
        └── val/
            ├── deer/
            ├── elk/
            └── moose/
    """
    
    def __init__(
        self,
        data_dir: str,
        transform: Optional[transforms.Compose] = None,
        extensions: Tuple[str, ...] = ('.jpg', '.jpeg', '.png')
    ):
        """
        Initialize wildlife dataset.
        
        Args:
            data_dir: Path to dataset directory
            transform: Image transformations to apply
            extensions: Valid image file extensions
        """
        self.data_dir = Path(data_dir)
        self.transform = transform or self._default_transform()
        self.extensions = extensions
        
        # Discover classes and images
        self.classes = sorted([d.name for d in self.data_dir.iterdir() if d.is_dir()])
        self.class_to_idx = {cls: idx for idx, cls in enumerate(self.classes)}
        
        # Build image list
        self.samples = []
        for class_name in self.classes:
            class_dir = self.data_dir / class_name
            for img_path in class_dir.iterdir():
                if img_path.suffix.lower() in self.extensions:
                    self.samples.append((str(img_path), self.class_to_idx[class_name]))
        
        logger.info(f"Found {len(self.samples)} images in {len(self.classes)} classes")
    
    def _default_transform(self):
        """Default image transformations."""
        return transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
    
    def __len__(self) -> int:
        return len(self.samples)
    
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        img_path, label = self.samples[idx]
        
        try:
            image = Image.open(img_path).convert('RGB')
            if self.transform:
                image = self.transform(image)
            return image, label
        except Exception as e:
            logger.error(f"Failed to load {img_path}: {e}")
            # Return a blank image on error
            return torch.zeros(3, 224, 224), label


def get_data_transforms(augment: bool = True) -> Tuple[transforms.Compose, transforms.Compose]:
    """
    Get training and validation transforms.
    
    Args:
        augment: Whether to apply data augmentation for training
        
    Returns:
        Tuple of (train_transform, val_transform)
    """
    if augment:
        train_transform = transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(15),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
    else:
        train_transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
    
    val_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    
    return train_transform, val_transform


def train_epoch(
    model: nn.Module,
    dataloader: DataLoader,
    criterion: nn.Module,
    optimizer: optim.Optimizer,
    device: torch.device,
    epoch: int
) -> Tuple[float, float]:
    """
    Train for one epoch.
    
    Returns:
        Tuple of (average_loss, accuracy)
    """
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    pbar = tqdm(dataloader, desc=f"Epoch {epoch}")
    for images, labels in pbar:
        images, labels = images.to(device), labels.to(device)
        
        # Forward pass
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        
        # Backward pass
        loss.backward()
        optimizer.step()
        
        # Statistics
        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()
        
        # Update progress bar
        pbar.set_postfix({
            'loss': f'{running_loss / (pbar.n + 1):.3f}',
            'acc': f'{100. * correct / total:.2f}%'
        })
    
    avg_loss = running_loss / len(dataloader)
    accuracy = 100. * correct / total
    
    return avg_loss, accuracy


def validate(
    model: nn.Module,
    dataloader: DataLoader,
    criterion: nn.Module,
    device: torch.device
) -> Tuple[float, float]:
    """
    Validate the model.
    
    Returns:
        Tuple of (average_loss, accuracy)
    """
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for images, labels in tqdm(dataloader, desc="Validating"):
            images, labels = images.to(device), labels.to(device)
            
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
    
    avg_loss = running_loss / len(dataloader)
    accuracy = 100. * correct / total
    
    return avg_loss, accuracy


def train_model(
    train_dir: str,
    val_dir: str,
    output_dir: str = "models",
    model_name: str = "resnet50",
    num_epochs: int = 10,
    batch_size: int = 32,
    learning_rate: float = 0.001,
    device: Optional[str] = None
) -> SpeciesClassifier:
    """
    Train a wildlife species classifier.
    
    Args:
        train_dir: Path to training data directory
        val_dir: Path to validation data directory
        output_dir: Directory to save model checkpoints
        model_name: Model architecture to use
        num_epochs: Number of training epochs
        batch_size: Batch size for training
        learning_rate: Learning rate
        device: Device to train on (cuda/cpu)
        
    Returns:
        Trained SpeciesClassifier
    """
    # Setup
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    else:
        device = torch.device(device)
    
    logger.info(f"Training on device: {device}")
    
    # Create datasets
    train_transform, val_transform = get_data_transforms(augment=True)
    
    train_dataset = WildlifeDataset(train_dir, transform=train_transform)
    val_dataset = WildlifeDataset(val_dir, transform=val_transform)
    
    num_classes = len(train_dataset.classes)
    class_names = train_dataset.classes
    
    logger.info(f"Classes: {class_names}")
    logger.info(f"Training samples: {len(train_dataset)}")
    logger.info(f"Validation samples: {len(val_dataset)}")
    
    # Create dataloaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=4,
        pin_memory=True
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=4,
        pin_memory=True
    )
    
    # Create model
    classifier = SpeciesClassifier.create_model(
        num_classes=num_classes,
        model_name=model_name
    )
    classifier.model.to(device)
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(classifier.model.parameters(), lr=learning_rate)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='max', patience=2, verbose=True)
    
    # Training loop
    best_acc = 0.0
    history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}
    
    for epoch in range(1, num_epochs + 1):
        logger.info(f"\nEpoch {epoch}/{num_epochs}")
        
        # Train
        train_loss, train_acc = train_epoch(
            classifier.model, train_loader, criterion, optimizer, device, epoch
        )
        
        # Validate
        val_loss, val_acc = validate(classifier.model, val_loader, criterion, device)
        
        # Update scheduler
        scheduler.step(val_acc)
        
        # Log results
        logger.info(f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}%")
        logger.info(f"Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.2f}%")
        
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)
        
        # Save best model
        if val_acc > best_acc:
            best_acc = val_acc
            best_model_path = output_dir / f"{model_name}_best.pth"
            classifier.save(str(best_model_path), class_names=class_names)
            logger.info(f"✓ Saved best model (acc: {best_acc:.2f}%)")
    
    # Save final model
    final_model_path = output_dir / f"{model_name}_final.pth"
    classifier.save(str(final_model_path), class_names=class_names)
    
    # Save training history
    history_path = output_dir / "training_history.json"
    with open(history_path, 'w') as f:
        json.dump(history, f, indent=2)
    
    logger.info(f"\nTraining complete! Best validation accuracy: {best_acc:.2f}%")
    logger.info(f"Best model saved to: {best_model_path}")
    
    return classifier
