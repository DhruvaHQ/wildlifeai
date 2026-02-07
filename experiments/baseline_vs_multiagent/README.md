# Experiment: Baseline vs Multi-Agent Pipeline

## Research Question

**Does the multi-agent cognitive architecture generate higher-quality ecological insights compared to a simple detection-only baseline?**

## Hypothesis

The multi-agent system (Vision + Insight + Memory + Reporter) will:
1. Generate more diverse insight types
2. Detect behavioral patterns with higher accuracy
3. Identify anomalies more reliably

## Experimental Setup

### Baseline Pipeline
- Species detection only
- No pattern analysis
- No anomaly detection
- Simple JSON output

### Multi-Agent Pipeline
- Full cognitive system
- Autonomous pattern discovery
- Anomaly detection with baselines
- Scientific narrative generation

### Dataset
- 100 synthetic camera-trap observations
- Known temporal patterns (nocturnal/diurnal species)
- Injected activity anomalies
- Multiple species across 10 days

### Evaluation Metrics
- **Pattern Detection**: Precision, Recall, F1-Score
- **Anomaly Detection**: True Positive Rate, False Positive Rate
- **Insight Quality**: Diversity, Coverage, Confidence
- **Runtime Performance**: Processing time per observation

## Configuration

See `config.json` for experimental parameters:
- Insight Agent anomaly threshold: 1.5
- Memory Agent baseline window: 7 days
- Vision Agent confidence threshold: 0.7

## Running the Experiment

```bash
# Run baseline
python experiments/baseline_vs_multiagent/run_baseline.py

# Run multi-agent
python experiments/baseline_vs_multiagent/run_multiagent.py

# Compare results
python experiments/baseline_vs_multiagent/compare.py
```

## Results

See `results/` directory:
- `baseline_results.json` - Baseline pipeline outputs
- `multiagent_results.json` - Multi-agent system outputs
- `comparison.json` - Side-by-side metrics comparison
- `evaluation_report.txt` - Detailed analysis

## Expected Outcomes

Based on design, we expect:
- **Pattern Detection F1**: Baseline ~0.0 (no pattern analysis), Multi-Agent ~0.85+
- **Anomaly Detection**: Baseline ~0.0 (no anomaly detection), Multi-Agent ~0.75+
- **Insight Diversity**: Baseline ~1 type (species only), Multi-Agent ~4+ types

## Notes

This experiment validates that the cognitive architecture provides measurable improvements over simple detection pipelines for ecological intelligence extraction.

## References

- Multi-agent system architecture: See `COGNITIVE_ARCHITECTURE.md`
- Evaluation methodology: See `src/wildlifeai/evaluation.py`
