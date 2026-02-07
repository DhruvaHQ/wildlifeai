"""
Run multi-agent cognitive system for experimental comparison.
"""
import sys
from pathlib import Path
import json
import time
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from wildlifeai.agents.controller import create_cognitive_system
from wildlifeai.agents.base import Message
from wildlifeai.evaluation import SyntheticValidator, PatternEvaluator


def run_multiagent_experiment():
    """Run multi-agent pipeline on synthetic test data."""
    print("=" * 80)
    print("EXPERIMENT: Multi-Agent Cognitive System")
    print("=" * 80)
    
    # Load configuration
    config_path = Path(__file__).parent / "config.json"
    with open(config_path) as f:
        config = json.load(f)
    
    # Initialize system
    print("\nInitializing cognitive system...")
    controller, message_bus, registry = create_cognitive_system()
    
    # Generate synthetic test data
    print("\nGenerating synthetic observations...")
    validator = SyntheticValidator()
    
    all_observations = []
    
    # Generate temporal pattern observations
    tiger_obs = validator.generate_temporal_test_case('tiger', 'nocturnal', 25)
    deer_obs = validator.generate_temporal_test_case('deer', 'diurnal', 25)
    all_observations.extend(tiger_obs)
    all_observations.extend(deer_obs)
    
    # Generate anomaly observations
    elephant_obs, anomaly_gt = validator.generate_anomaly_test_case('elephant')
    all_observations.extend(elephant_obs)
    
    print(f"Generated {len(all_observations)} synthetic observations")
    
    # Process through system
    print("\nProcessing through multi-agent system...")
    start_time = time.time()
    
    for obs in all_observations:
        message_bus.publish(Message(
            type='observation',
            sender='experiment',
            data=obs,
            timestamp=obs['timestamp']
        ))
    
    # Trigger analysis
    controller.publish('trigger_analysis', {})
    
    processing_time = time.time() - start_time
    
    # Collect results
    print("\nCollecting results...")
    insights = message_bus.get_history('insight')
    alerts = message_bus.get_history('alert')
    
    # Evaluate
    evaluator = PatternEvaluator()
    
    # Extract detected patterns
    detected_patterns = [msg.data for msg in insights if msg.data.get('type') == 'temporal_pattern']
    ground_truth_patterns = [
        {'species': 'tiger', 'pattern': 'nocturnal'},
        {'species': 'deer', 'pattern': 'diurnal'}
    ]
    
    pattern_metrics = evaluator.evaluate_temporal_patterns(
        detected_patterns,
        ground_truth_patterns
    )
    
    # Extract detected anomalies
    detected_anomalies = [msg.data for msg in alerts]
    anomaly_metrics = evaluator.evaluate_anomaly_detection(
        detected_anomalies,
        [anomaly_gt]
    )
    
    # Insight quality
    all_insights = [msg.data for msg in insights]
    quality_metrics = evaluator.evaluate_insight_quality(all_insights)
    
    # Compile results
    results = {
        'experiment': 'multiagent_cognitive_system',
        'timestamp': datetime.now().isoformat(),
        'config': config['multiagent_config'],
        'dataset_size': len(all_observations),
        'processing_time_seconds': processing_time,
        'metrics': {
            'pattern_detection': pattern_metrics,
            'anomaly_detection': anomaly_metrics,
            'insight_quality': quality_metrics
        },
        'raw_outputs': {
            'insights_count': len(insights),
            'alerts_count': len(alerts),
            'insights': [msg.data for msg in insights[:5]],  # Sample
            'alerts': [msg.data for msg in alerts[:5]]
        }
    }
    
    # Save results
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    
    results_path = results_dir / "multiagent_results.json"
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n✓ Results saved to {results_path}")
    
    # Print summary
    print("\n" + "=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    print(f"\nPattern Detection:")
    print(f"  Precision: {pattern_metrics['precision']:.3f}")
    print(f"  Recall: {pattern_metrics['recall']:.3f}")
    print(f"  F1-Score: {pattern_metrics['f1_score']:.3f}")
    
    print(f"\nAnomaly Detection:")
    print(f"  Precision: {anomaly_metrics['precision']:.3f}")
    print(f"  Recall: {anomaly_metrics['recall']:.3f}")
    print(f"  F1-Score: {anomaly_metrics['f1_score']:.3f}")
    
    print(f"\nInsight Quality:")
    print(f"  Total Insights: {quality_metrics['total_insights']}")
    print(f"  Unique Types: {quality_metrics['unique_types']}")
    print(f"  Species Coverage: {quality_metrics['species_coverage']}")
    
    print(f"\nProcessing Time: {processing_time:.2f} seconds")
    print("=" * 80)
    
    return results


if __name__ == "__main__":
    run_multiagent_experiment()
