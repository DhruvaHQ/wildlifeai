# WildlifeAI

[![Tests](https://github.com/DhruvaHQ/wildlifeai/actions/workflows/tests.yml/badge.svg)](https://github.com/DhruvaHQ/wildlifeai/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/DhruvaHQ/wildlifeai/branch/main/graph/badge.svg)](https://codecov.io/gh/DhruvaHQ/wildlifeai)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**WildlifeAI is a modular multi-agent framework designed to automate ecological intelligence extraction from wildlife camera-trap data.**

Instead of focusing solely on species detection, WildlifeAI introduces a cognitive pipeline that transforms raw observations into structured ecological insights through coordinated AI agents. The system combines computer vision, temporal pattern analysis, and autonomous reasoning to generate actionable conservation intelligence.

## Architecture Overview

### Multi-Agent Cognitive System

```
                    Controller Agent
                   (Executive Function)
                          |
        +-----------------+-----------------+
        |                 |                 |
   Vision Agent     Insight Agent    Memory Agent    Reporter Agent
   (Detection)      (Reasoning)      (Learning)      (Narrative)
        |                 |                 |              |
    Species          Patterns         Baselines       Reports
    Detection        Analysis         & History       & Alerts
```

### Data Flow Pipeline

```
Camera Trap Images
        |
        v
    Vision Agent -----> Structured Observations
                              |
                              v
                        Insight Agent -----> Patterns & Anomalies
                              |
                +-------------+-------------+
                |                           |
                v                           v
          Memory Agent                Reporter Agent
        (Learn Baselines)           (Generate Narratives)
                |                           |
                v                           v
        Historical Context            Scientific Reports
```

## Motivation

Many wildlife AI efforts struggle not due to model performance, but due to the lack of robust and reproducible data pipelines. WildlifeAI addresses this gap by providing a clean, modular framework designed for experimentation and future model integration.

## Key Features

- **Modular pipeline architecture** with clear separation of concerns
- **Image metadata and EXIF extraction** for camera-trap workflows
- **Config-driven execution** for reproducibility
- **Structured logging and error handling**
- **Command-line interface (CLI)** for experiment control
- **Model-agnostic ML interface** for species classification
- **Multiple output formats** (JSON and CSV)

## NEW: Deep Learning Support

WildlifeAI now includes production-ready **PyTorch-based species classification**:

- **ResNet50 & EfficientNet** models with transfer learning
- **GPU acceleration** for fast inference
- **Batch processing** for efficiency
- **Training utilities** for custom models
- **Pre-trained weights** ready to use

```python
from wildlifeai.models import SpeciesClassifier

classifier = SpeciesClassifier(model_path="models/wildlife_model.pth")
result = classifier.predict("camera_trap_image.jpg")
# {"deer": 0.92, "elk": 0.05, "moose": 0.03}
```

See [ML_GUIDE.md](ML_GUIDE.md) for complete documentation.

## REVOLUTIONARY: Cognitive Architecture

### This is NOT just species detection. This is AUTONOMOUS ECOLOGICAL INTELLIGENCE.

WildlifeAI features a **multi-agent cognitive system** that performs:

- **Autonomous Pattern Discovery** - Finds behavioral patterns without being told what to look for
- **Ecological Reasoning** - Generates scientific hypotheses and conservation insights
- **Anomaly Detection** - Identifies unusual activity and population changes  
- **Scientific Narratives** - Transforms data into actionable reports
- **Learning & Memory** - Builds baselines and improves over time

### Example: From Detection to Intelligence

**Traditional AI:**
```
image → "tiger detected" → done
```

**WildlifeAI Cognitive System:**
```python
from wildlifeai.agents.controller import create_cognitive_system

# Create autonomous intelligence system
controller, bus, registry = create_cognitive_system()

# Process images - rest happens AUTOMATICALLY
controller.publish('system_command', {
    'command': 'process_images',
    'image_paths': camera_trap_images
})

# System autonomously:
# 1. Detects species (Vision Agent)
# 2. Analyzes patterns (Insight Agent)  
# 3. Learns baselines (Memory Agent)
# 4. Generates reports (Reporter Agent)
```

**Output:**
```
INSIGHT: Tiger exhibits nocturnal pattern (87% nighttime activity).
Ecological context: Suggests adaptation to thermal regulation.

ALERT: Elephant activity increased 2.3x above baseline.
Possible cause: Water scarcity migration pattern.
Recommendation: Investigate environmental changes in affected zones.
```

### 5 Cognitive Agents Working Together:

```
                Controller (Executive Function)
                          |
        +-----------------+------------------+
        |                 |                  |
   Vision Agent     Insight Agent     Memory Agent     Reporter Agent
   (Detection)      (Reasoning)       (Learning)       (Narrative)
```

See [COGNITIVE_ARCHITECTURE.md](COGNITIVE_ARCHITECTURE.md) for complete details.

**Run demo:** `python examples/cognitive_system_demo.py`

### Why This is Revolutionary:

- **Multi-Agent Architecture** - Modern AI design, not a pipeline  
- **Autonomous Reasoning** - Makes decisions, doesn't just execute  
- **Scientific Value** - Generates conservation insights, not just labels  
- **Research-Grade** - PhD-level systems thinking

**This transforms wildlife AI from detection into INTELLIGENCE.**

## Project Structure

```
src/wildlifeai/
├── cli.py              # Command-line interface
├── pipeline.py         # Pipeline orchestration
├── utils.py            # Image processing utilities
├── models.py           # ML model interface
├── training.py         # Training utilities
├── agents/             # Cognitive agent system
│   ├── base.py         # Agent framework
│   ├── controller.py   # System orchestrator
│   ├── vision_agent.py # Species detection
│   ├── insight_agent.py# Pattern analysis
│   ├── memory_agent.py # Learning & baselines
│   └── reporter_agent.py# Narrative generation
└── __init__.py         # Package initialization
```

## Installation

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

## Quick Start

### Basic Pipeline

```bash
# Process images in a folder
poetry run wildlifeai process test_images

# Use config file
poetry run wildlifeai process --config config.json
```

### Cognitive System Demo

```bash
# See autonomous intelligence in action
python examples/cognitive_system_demo.py
```

**See complete end-to-end example with real output:** [EXAMPLE.md](EXAMPLE.md)

## Usage

### Simple Detection

```python
from wildlifeai.models import SpeciesClassifier

classifier = SpeciesClassifier()
predictions = classifier.predict("wildlife_image.jpg")
print(predictions)
```

### Full Pipeline with Cognitive System

```python
from wildlifeai.agents.controller import create_cognitive_system

# Initialize cognitive system
controller, message_bus, registry = create_cognitive_system(
    model_path="models/wildlife_resnet50.pth"
)

# Process images autonomously
controller.publish('system_command', {
    'command': 'process_images',
    'image_paths': ['img1.jpg', 'img2.jpg', 'img3.jpg']
})

# Generate scientific report
controller.publish('system_command', {
    'command': 'generate_report',
    'report_type': 'detailed'
})

# Get system status
status = controller.get_system_status()
print(status)
```

## Configuration

Example `config.json`:

```json
{
  "image_folder": "camera_trap_images",
  "json_output": "wildlife_metadata.json",
  "csv_output": "wildlife_metadata.csv"
}
```

## Output Formats

### JSON Output

```json
[
  {
    "filename": "tiger_001.jpg",
    "format": "JPEG",
    "width": 1920,
    "height": 1080,
    "exif": {...},
    "species_prediction": {
      "tiger": 0.93,
      "leopard": 0.05,
      "unknown": 0.02
    }
  }
]
```

### CSV Output

```csv
filename,format,width,height,species,confidence
tiger_001.jpg,JPEG,1920,1080,tiger,0.93
```

## ML Model Integration

WildlifeAI supports easy integration with custom ML models:

```python
from wildlifeai.models import SpeciesClassifier

# Create model for training
classifier = SpeciesClassifier.create_model(
    num_classes=10,
    model_name="resnet50"
)

# Train (see ML_GUIDE.md for details)
from wildlifeai.training import train_model

trained_classifier = train_model(
    train_dir="data/train",
    val_dir="data/val",
    num_epochs=20
)

# Save model
trained_classifier.save("models/my_wildlife_model.pth", class_names=species_list)
```

## Development

### Running Tests

Run all tests:
```bash
poetry run pytest
```

Run with coverage report:
```bash
poetry run pytest --cov=src/wildlifeai --cov-report=html
```

View coverage in browser:
```bash
# Open htmlcov/index.html in your browser
```

Run specific test file:
```bash
poetry run pytest tests/test_utils.py -v
```

### Code Quality

```bash
# Format code with Black
poetry run black src/ tests/

# Lint with Flake8
poetry run flake8 src/ tests/
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/wildlifeai.git`
3. Install dependencies: `poetry install --with dev`
4. Create a branch: `git checkout -b feature/your-feature`
5. Make changes and add tests
6. Run tests: `poetry run pytest`
7. Submit a pull request

## Testing Guide

See [TESTING.md](TESTING.md) for comprehensive testing documentation.

## Documentation

- [ML_GUIDE.md](ML_GUIDE.md) - Machine learning implementation guide
- [COGNITIVE_ARCHITECTURE.md](COGNITIVE_ARCHITECTURE.md) - Multi-agent system architecture
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [TESTING.md](TESTING.md) - Testing guide

## Roadmap

### Completed
- [x] Core pipeline architecture
- [x] EXIF metadata extraction
- [x] CLI interface
- [x] PyTorch model integration
- [x] Multi-agent cognitive system
- [x] Autonomous pattern analysis
- [x] Scientific narrative generation
- [x] Comprehensive test suite
- [x] CI/CD pipeline

### Upcoming
- [ ] Web dashboard for visualization
- [ ] Real-time streaming analysis
- [ ] Advanced anomaly detection
- [ ] LLM-powered narrative generation
- [ ] Federated learning support
- [ ] Mobile app integration

## Citation

If you use WildlifeAI in your research, please cite:

```bibtex
@software{wildlifeai2026,
  title={WildlifeAI: Autonomous Ecological Intelligence for Wildlife Conservation},
  author={Dhruva},
  year={2026},
  url={https://github.com/DhruvaHQ/wildlifeai}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with PyTorch and torchvision
- Inspired by conservation AI initiatives worldwide
- Thanks to the open-source community

## Contact

- GitHub: [@DhruvaHQ](https://github.com/DhruvaHQ)
- Issues: [GitHub Issues](https://github.com/DhruvaHQ/wildlifeai/issues)

---

**Transform wildlife conservation with autonomous AI intelligence.**
