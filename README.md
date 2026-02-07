\# 🦁 WildlifeAI

**WildlifeAI** is an open-source Python framework that turns raw camera trap images into structured wildlife intelligence using a configurable, end-to-end AI pipeline.

## 💡 Motivation

Many wildlife AI efforts struggle not due to model performance, but due to the lack of robust and reproducible data pipelines. WildlifeAI addresses this gap by providing a clean, modular framework designed for experimentation and future model integration.

## ✨ Key Features

- 🔧 **Modular pipeline architecture** with clear separation of concerns
- 📸 **Image metadata and EXIF extraction** for camera-trap workflows
- ⚙️ **Config-driven execution** for reproducibility
- 📝 **Structured logging and error handling**
- 🖥️ **Command-line interface (CLI)** for experiment control
- 🤖 **Model-agnostic ML interface** for future species classification
- 📊 **Multiple output formats** (JSON and CSV)

## 📁 Project Structure

```
src/wildlifeai/
├── cli.py          # Command-line interface
├── pipeline.py     # Pipeline orchestration
├── utils.py        # Image processing utilities
├── models.py       # ML model interface (placeholder)
└── __init__.py     # Package initialization
```

## 🚀 Installation

### Using Poetry (Recommended)

```bash
git clone https://github.com/DhruvaHQ/wildlifeai.git
cd wildlifeai
poetry install
```

### Using pip

```bash
git clone https://github.com/DhruvaHQ/wildlifeai.git
cd wildlifeai
pip install -e .
```

## 📖 Usage

### Basic Usage

Process images from a folder:

```bash
poetry run wildlifeai process test_images
```

### Using Configuration File

Create a `config.json`:

```json
{
    "image_folder": "test_images",
    "json_output": "image_metadata.json",
    "csv_output": "image_metadata.csv"
}
```

Run with config:

```bash
poetry run wildlifeai process --config config.json
```

### Override Config Options

```bash
poetry run wildlifeai process --config config.json --json my_output.json --csv my_output.csv
```

Or specify folder directly:

```bash
poetry run wildlifeai process my_images --json results.json --csv results.csv
```

## 📊 Output Format

### JSON Output

```json
[
    {
        "filename": "wildlife_001.jpg",
        "format": "JPEG",
        "width": 1920,
        "height": 1080,
        "mode": "RGB",
        "datetime": "2024:01:15 14:30:22",
        "camera_make": "Canon",
        "camera_model": "EOS 5D Mark IV",
        "species_prediction": {
            "deer": 0.85,
            "unknown": 0.15
        }
    }
]
```

### CSV Output

Tabular format compatible with Excel, pandas, and other data analysis tools.

## 🔮 Future ML Integration

The `SpeciesClassifier` in `models.py` provides a clean interface for integrating your own models:

```python
from wildlifeai.models import SpeciesClassifier

class MyCustomClassifier(SpeciesClassifier):
    def __init__(self, model_path: str):
        # Load your model
        self.model = load_model(model_path)
    
    def predict(self, image_path: str) -> Dict[str, float]:
        # Your prediction logic
        return {"species_name": confidence}
```

## 🛠️ Development

### Running Tests

```bash
poetry run pytest
```

### Code Quality

```bash
# Format code
poetry run black src/

# Lint
poetry run flake8 src/
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

Built for wildlife researchers, conservationists, and AI practitioners working on camera trap analysis.

---

**Note**: This is an early-stage framework. The ML model interface is currently a placeholder. Contributions for model integration are especially welcome!



