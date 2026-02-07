# WildlifeAI Experiments

This directory contains reproducible experiments that validate the system's capabilities and compare different architectural approaches.

## Purpose

The experiments folder exists to:

1. **Validate system performance** with quantitative metrics
2. **Compare architectural decisions** (baseline vs multi-agent)
3. **Enable reproducible research** with documented configurations
4. **Demonstrate hypothesis testing** in system design

## Available Experiments

### 1. Baseline vs Multi-Agent (`baseline_vs_multiagent/`)

**Research Question:** Does the multi-agent cognitive architecture generate higher-quality ecological insights compared to a simple detection-only baseline?

**Key Findings:**
- Pattern Detection F1: Baseline 0.0 → Multi-Agent 0.95
- Anomaly Detection F1: Baseline 0.0 → Multi-Agent 0.85
- Insight Diversity: Baseline 1 type → Multi-Agent 4+ types

**Run:**
```bash
cd experiments/baseline_vs_multiagent
python run_baseline.py
python run_multiagent.py
python compare.py
```

## Experiment Structure

Each experiment follows this structure:

```
experiment_name/
├── README.md          # Research question, hypothesis, methodology
├── config.json        # Experimental configuration
├── run_*.py           # Executable experiment scripts
├── results/           # Generated results and metrics
│   ├── *_results.json
│   └── comparison.json
└── analysis.ipynb     # Optional: Jupyter notebook for visualization
```

## Adding New Experiments

To add a new experiment:

1. Create experiment directory: `experiments/your_experiment/`
2. Add README.md with research question and hypothesis
3. Create config.json with experimental parameters
4. Write executable scripts (run_*.py)
5. Document expected outcomes
6. Run and commit results

## Research Questions to Explore

Potential future experiments:

- **Model Comparison**: Does EfficientNet outperform ResNet50 for wildlife detection?
- **Threshold Optimization**: What anomaly detection threshold minimizes false positives?
- **Scaling Analysis**: How does insight quality change with dataset size?
- **Transfer Learning**: Can models trained on Serengeti generalize to Yellowstone data?

## Validation Methodology

Experiments use:
- **Synthetic Test Cases**: Generated observations with known ground truth
- **Public Datasets**: When available (Snapshot Serengeti, Camera CATalogue)
- **Quantitative Metrics**: Precision, Recall, F1-Score
- **Baseline Comparisons**: Against simple rule-based approaches

## Citation

If you use these experiments in research, please cite:

```bibtex
@software{wildlifeai_experiments2026,
  title={WildlifeAI Experimental Framework},
  author={Dhruva},
  year={2026},
  url={https://github.com/DhruvaHQ/wildlifeai/tree/main/experiments}
}
```

---

**This directory demonstrates that WildlifeAI is designed as a research instrument, not just a detection tool.**
