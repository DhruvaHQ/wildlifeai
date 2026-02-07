"""
Train a wildlife species classification model.

This script demonstrates how to train a custom model on wildlife data.

Usage:
    python examples/train_wildlife_model.py --help
"""
import sys
from pathlib import Path
import argparse

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from wildlifeai.training import train_model


def main():
    parser = argparse.ArgumentParser(
        description="Train WildlifeAI species classifier",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--train-dir",
        type=str,
        required=True,
        help="Path to training data directory (organized by species folders)"
    )
    
    parser.add_argument(
        "--val-dir",
        type=str,
        required=True,
        help="Path to validation data directory"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default="models",
        help="Directory to save trained models"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        default="resnet50",
        choices=["resnet50", "efficientnet_b0", "efficientnet_b2"],
        help="Model architecture to use"
    )
    
    parser.add_argument(
        "--epochs",
        type=int,
        default=10,
        help="Number of training epochs"
    )
    
    parser.add_argument(
        "--batch-size",
        type=int,
        default=32,
        help="Batch size for training"
    )
    
    parser.add_argument(
        "--lr",
        type=float,
        default=0.001,
        help="Learning rate"
    )
    
    args = parser.parse_args()
    
    print("🦁 WildlifeAI Model Training\n")
    print("=" * 60)
    print(f"   Training data: {args.train_dir}")
    print(f"   Validation data: {args.val_dir}")
    print(f"   Model: {args.model}")
    print(f"   Epochs: {args.epochs}")
    print(f"   Batch size: {args.batch_size}")
    print(f"   Learning rate: {args.lr}")
    print("=" * 60 + "\n")
    
    # Train the model
    classifier = train_model(
        train_dir=args.train_dir,
        val_dir=args.val_dir,
        output_dir=args.output_dir,
        model_name=args.model,
        num_epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.lr
    )
    
    print("\n✅ Training complete!")
    print(f"\nModel info:")
    info = classifier.get_model_info()
    for key, value in info.items():
        print(f"   {key}: {value}")


if __name__ == "__main__":
    main()
