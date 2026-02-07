"""
Quick demo of WildlifeAI species classification.

This demo uses a pre-trained ResNet50 model (ImageNet weights) to
demonstrate the classification pipeline. For real wildlife classification,
you'll need to train on wildlife-specific data.
"""
from pathlib import Path
import sys

# Add src to path for demo
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from wildlifeai.models import SpeciesClassifier
from wildlifeai.pipeline import run_pipeline


def demo_classification(image_folder: str = "test_images"):
    """
    Run a quick classification demo.
    
    Args:
        image_folder: Path to folder containing test images
    """
    print("🦁 WildlifeAI Classification Demo\n")
    print("=" * 60)
    
    # Initialize classifier (using ImageNet pre-trained weights)
    print("\n📦 Loading model...")
    classifier = SpeciesClassifier(
        model_name="resnet50",
        num_classes=1000  # ImageNet classes
    )
    
    # Show model info
    info = classifier.get_model_info()
    print(f"   Model: {info['model_name']}")
    print(f"   Device: {info['device']}")
    print(f"   Parameters: {info['total_parameters']:,}")
    
    # Run pipeline
    print(f"\n🔍 Processing images from '{image_folder}'...")
    results = run_pipeline(
        image_folder=image_folder,
        json_output="demo_output.json",
        csv_output="demo_output.csv",
        model_path=None  # Will use default classifier
    )
    
    # Display results
    print(f"\n✅ Processed {len(results)} images\n")
    print("=" * 60)
    print("\nTop Predictions:")
    print("-" * 60)
    
    for item in results:
        print(f"\n📸 {item['filename']}")
        print(f"   Size: {item['width']}x{item['height']}")
        
        predictions = item.get('species_prediction', {})
        if predictions:
            print("   Predictions:")
            for species, confidence in list(predictions.items())[:3]:
                print(f"      {species}: {confidence:.2%}")
    
    print("\n" + "=" * 60)
    print("\n💾 Results saved to:")
    print(f"   - demo_output.json")
    print(f"   - demo_output.csv")
    print("\n" + "=" * 60)
    
    print("\n📝 Note: This demo uses ImageNet pre-trained weights.")
    print("   For real wildlife classification, train on wildlife data!")
    print("\n   See: examples/train_wildlife_model.py\n")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="WildlifeAI Quick Demo")
    parser.add_argument(
        "folder",
        nargs="?",
        default="test_images",
        help="Path to folder containing images"
    )
    
    args = parser.parse_args()
    
    try:
        demo_classification(args.folder)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
