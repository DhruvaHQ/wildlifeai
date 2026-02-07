"""
Run baseline detection-only pipeline for experimental comparison.
"""
import sys
from pathlib import Path
import json
import time
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from wildlifeai.evaluation import SyntheticValidator


def run_baseline_experiment():
    """Run baseline detection-only pipeline on synthetic test data."""
    print("=" * 80)
    print("EXPERIMENT: Baseline Detection-Only Pipeline")
    print("=" * 80)
    
    # Load configuration
    config_path = Path(__file__).parent / "config.json"
    with open(config_path) as f:
        config = json.load(f)
    
    # Generate synthetic test data
    print("\nGenerating synthetic observations...")
    validator = SyntheticValidator()
    
    all_observations = []
    
    # Generate observations
    tiger_obs = validator.generate_temporal_test_case('tiger', 'nocturnal', 25)
    deer_obs = validator.generate_temporal_test_case('deer', 'diurnal', 25)
    elephant_obs, _ = validator.generate_anomaly_test_case('elephant')
    
    all_observations.extend(tiger_obs)
    all_observations.extend(deer_obs)
    all_observations.extend(elephant_obs)
    
    print(f"Generated {len(all_observations)} synthetic observations")
    
    # Process through baseline (detection only - no pattern analysis)
    print("\nProcessing through baseline pipeline...")
    start_time = time.time()
    
    # Baseline just outputs species detections
    detections = []
    for obs in all_observations:
        detections.append({
            'species': obs['species'],
            'confidence': obs['confidence'],
            'timestamp': obs['timestamp'].isoformat(),
            'camera_id': obs['camera_id']
        })
    
    processing_time = time.time() - start_time
    
    # Baseline metrics (no pattern/anomaly detection)
    results = {
        'experiment': 'baseline_detection_only',
        'timestamp': datetime.now().isoformat(),
        'config': config['baseline_config'],
        'dataset_size': len(all_observations),
        'processing_time_seconds': processing_time,
        'metrics': {
            'pattern_detection': {
                'precision': 0.0,
                'recall': 0.0,
                'f1_score': 0.0,
                'note': 'Baseline has no pattern detection capability'
            },
            'anomaly_detection': {
                'precision': 0.0,
                'recall': 0.0,
                'f1_score': 0.0,
                'note': 'Baseline has no anomaly detection capability'
            },
            'insight_quality': {
                'total_insights': 0,
                'unique_types': 1,  # Only species detection
                'species_coverage': len(set(d['species'] for d in detections)),
                'note': 'Baseline only provides species labels'
            }
        },
        'raw_outputs': {
            'detections_count': len(detections),
            'sample_detections': detections[:5]
        }
    }
    
    # Save results
    results_dir = Path(__file__).parent / "results"
    results_dir.mkdir(exist_ok=True)
    
    results_path = results_dir / "baseline_results.json"
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n✓ Results saved to {results_path}")
    
    # Print summary
    print("\n" + "=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    print(f"\nDetections: {len(detections)}")
    print(f"Pattern Detection: Not available (baseline)")
    print(f"Anomaly Detection: Not available (baseline)")
    print(f"Insight Types: Species labels only")
    print(f"Processing Time: {processing_time:.2f} seconds")
    print("=" * 80)
    
    return results


if __name__ == "__main__":
    run_baseline_experiment()
