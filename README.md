# WildlifeAI

[![Tests](https://github.com/DhruvaHQ/wildlifeai/actions/workflows/tests.yml/badge.svg)](https://github.com/DhruvaHQ/wildlifeai/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/DhruvaHQ/wildlifeai/branch/main/graph/badge.svg)](https://codecov.io/gh/DhruvaHQ/wildlifeai)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A modular multi-agent framework for automated ecological intelligence extraction from wildlife camera-trap data.

https://wildlifeairealoutput.netlify.app/

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

## Evaluation Results

**System performance validated on synthetic test cases with known ground truth patterns.**

### Pattern Detection Accuracy

| Pattern Type | Precision | Recall | F1-Score |
|-------------|-----------|--------|----------|
| Temporal    | 0.95      | 0.95   | 0.95     |
| Spatial     | 0.88      | 0.91   | 0.89     |
| Anomaly     | 0.85      | 0.80   | 0.82     |

### Baseline Comparison

Compared against detection-only pipeline (no pattern analysis):

| Method                  | Pattern F1 | Anomaly F1 | Insight Types |
|------------------------|------------|------------|---------------|
| Baseline (Detection)   | 0.00       | 0.00       | 1 (species)   |
| **Multi-Agent System** | **0.95**   | **0.82**   | **4+**        |

### Key Findings

- **95% accuracy** on temporal pattern detection (nocturnal/diurnal behavior)
- **82% F1-score** on anomaly detection (activity spikes/declines)
- Generates **4x more insight types** than baseline detection
- Processes 100 observations in **2-3 seconds** (with analysis)

**See `experiments/baseline_vs_multiagent/` for full experimental validation.**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
