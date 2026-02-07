# 🤖 Machine Learning Implementation Guide

## What's New

WildlifeAI now includes a **production-ready deep learning classifier** for wildlife species identification!

---

## 🚀 Quick Start

### 1. Install ML Dependencies

```bash
poetry lock
poetry install
```

This adds:
- **PyTorch** - Deep learning framework
- **torchvision** - Pre-trained models and transforms
- **timm** - Advanced model architectures
- **tqdm** - Progress bars

### 2. Run Quick Demo

```bash
# Uses pre-trained ImageNet weights (for demo purposes)
python examples/quick_demo.py test_images
```

---

## 📚 What Was Added

### New Files

```
wildlifeai/
├── src/wildlifeai/
│   ├── models.py        ✨ ENHANCED: Real PyTorch classifier
│   └── training.py      ✨ NEW: Training utilities
├── examples/
│   ├── quick_demo.py           ✨ NEW: Quick demo script
│   └── train_wildlife_model.py ✨ NEW: Training script
├── data/                ✨ NEW: Dataset directory
└── models/              ✨ NEW: Model checkpoints
```

### Enhanced `models.py`

**Before:** Placeholder returning `{"unknown": 1.0}`

**After:** Full PyTorch implementation with:
- ✅ ResNet50 / EfficientNet support
- ✅ Transfer learning from ImageNet
- ✅ Batch processing
- ✅ GPU acceleration
- ✅ Model save/load
- ✅ Custom class names

---

## 🎓 Training Your Own Model

### Step 1: Prepare Your Data

Organize images by species:

```
data/
├── train/
│   ├── deer/
│   │   ├── deer001.jpg
│   │   └── deer002.jpg
│   ├── elk/
│   └── moose/
└── val/
    ├── deer/
    ├── elk/
    └── moose/
```

### Step 2: Train

```bash
python examples/train_wildlife_model.py \
    --train-dir data/train \
    --val-dir data/val \
    --epochs 20 \
    --batch-size 32 \
    --model resnet50
```

### Step 3: Use Trained Model

```python
from wildlifeai.models import SpeciesClassifier

# Load your trained model
classifier = SpeciesClassifier(
    model_path="models/resnet50_best.pth"
)

# Predict
results = classifier.predict("images/wildlife.jpg")
print(results)
# Output: {"deer": 0.92, "elk": 0.05, "moose": 0.03}
```

---

## 🔬 Architecture Details

### SpeciesClassifier

**Key Features:**
- Transfer learning from ImageNet
- Automatic GPU detection
- Configurable architectures
- Built-in preprocessing
- Batch inference support

**Supported Models:**
- `resnet50` (default, 25M params)
- `efficientnet_b0` (5M params, faster)
- `efficientnet_b2` (9M params, balanced)

### Example Usage

```python
from wildlifeai.models import SpeciesClassifier

# Create new model for training
classifier = SpeciesClassifier.create_model(
    num_classes=10,
    model_name="resnet50"
)

# Load pre-trained model
classifier = SpeciesClassifier(
    model_path="models/my_model.pth"
)

# Single image prediction
result = classifier.predict("image.jpg", top_k=3)

# Batch prediction (efficient)
results = classifier.predict_batch(
    ["img1.jpg", "img2.jpg", "img3.jpg"],
    batch_size=32
)

# Get model info
info = classifier.get_model_info()
print(info)
```

---

## 🎯 Training API

### Basic Training

```python
from wildlifeai.training import train_model

classifier = train_model(
    train_dir="data/train",
    val_dir="data/val",
    output_dir="models",
    num_epochs=10,
    batch_size=32,
    learning_rate=0.001
)
```

### Advanced Training

```python
from wildlifeai.training import (
    WildlifeDataset,
    get_data_transforms,
    train_epoch,
    validate
)
from torch.utils.data import DataLoader

# Custom dataset
train_transform, val_transform = get_data_transforms(augment=True)
train_dataset = WildlifeDataset("data/train", transform=train_transform)

# Custom training loop
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
# ... your custom training code
```

---

## 📊 Data Augmentation

Training includes automatic augmentation:
- ✅ Random crops and resizing
- ✅ Horizontal flips
- ✅ Random rotation (±15°)
- ✅ Color jittering
- ✅ Normalization (ImageNet stats)

---

## 💾 Model Checkpointing

Models are saved with metadata:

```python
# Model checkpoint includes:
{
    'model_state_dict': ...,    # Model weights
    'num_classes': 10,           # Number of classes
    'model_name': 'resnet50',    # Architecture
    'class_names': [...]         # Class labels
}

# Class names saved separately
models/classes.json:
{
    "classes": ["deer", "elk", "moose", ...]
}
```

---

## 🚀 Performance Tips

### GPU Acceleration

```python
# Automatic GPU detection
classifier = SpeciesClassifier(
    model_path="models/model.pth"
)  # Uses CUDA if available

# Force CPU
classifier = SpeciesClassifier(
    model_path="models/model.pth",
    device="cpu"
)
```

### Batch Processing

```python
# Process 100 images efficiently
image_paths = [f"images/{i}.jpg" for i in range(100)]

# BAD: Slow (100 individual predictions)
for path in image_paths:
    result = classifier.predict(path)

# GOOD: Fast (batched)
results = classifier.predict_batch(
    image_paths,
    batch_size=32  # Adjust based on GPU memory
)
```

---

## 🎛️ Integration with Pipeline

The existing pipeline automatically uses the ML model:

```python
from wildlifeai.pipeline import run_pipeline

# Option 1: Use default (ImageNet weights)
results = run_pipeline(
    image_folder="test_images",
    json_output="output.json"
)

# Option 2: Use your trained model
results = run_pipeline(
    image_folder="test_images",
    json_output="output.json",
    model_path="models/wildlife_resnet50.pth"
)
```

---

## 🧪 Testing

Tests are updated for ML components:

```bash
# Run all tests
poetry run pytest

# Test specific module
poetry run pytest tests/test_models.py -v
```

---

## 📖 Public Datasets

For training, consider these datasets:

1. **iWildCam** - Camera trap images
   - https://github.com/visipedia/iwildcam_comp

2. **Snapshot Serengeti** - 3M+ images
   - https://lila.science/datasets/snapshot-serengeti

3. **Caltech Camera Traps** - Varied ecosystems
   - https://lila.science/datasets/caltech-camera-traps

---

## 🔮 Next Steps

1. **Get Data** - Download a wildlife dataset
2. **Train Model** - Use `train_wildlife_model.py`
3. **Evaluate** - Check validation accuracy
4. **Deploy** - Use in your pipeline
5. **Iterate** - Improve with more data/tuning

---

## 💡 Example Workflow

```bash
# 1. Setup
poetry install

# 2. Organize your data
# data/train/deer/*.jpg
# data/train/elk/*.jpg
# data/val/deer/*.jpg
# data/val/elk/*.jpg

# 3. Train
python examples/train_wildlife_model.py \
    --train-dir data/train \
    --val-dir data/val \
    --epochs 20 \
    --model resnet50

# 4. Inference
python examples/quick_demo.py my_images/

# 5. Use in production
poetry run wildlifeai process camera_trap_images/ \
    --config config.json
```

---

## 🆘 Troubleshooting

**Out of memory:**
```python
# Reduce batch size
classifier.predict_batch(images, batch_size=16)
```

**Slow training:**
```python
# Use smaller model
classifier = SpeciesClassifier.create_model(
    num_classes=10,
    model_name="efficientnet_b0"  # Lighter than ResNet50
)
```

**Poor accuracy:**
- Collect more training data
- Use data augmentation
- Train for more epochs
- Try different model architectures

---

**Ready to classify some wildlife!** 🦁🐻🦌
