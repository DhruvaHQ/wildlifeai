"""
Memory Agent - Historical Context and Learning

Stores baselines, learns patterns over time, and provides historical context.
This enables the system to "remember" and improve its reasoning.
"""
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from collections import defaultdict
import json
from pathlib import Path
import logging

from wildlifeai.agents.base import Agent, Message, MessageBus

logger = logging.getLogger(__name__)


class MemoryAgent(Agent):
    """
    Memory Agent maintains historical knowledge and baselines.
    
    This is what makes the system "learn" and improve over time.
    
    Capabilities:
    -

 Store observation history
    - Maintain species baselines (normal behavior)
    - Track pattern evolution
    - Provide historical context for insights
    - Enable long-term trend analysis
    
    Publishes:
    - 'baseline_update' when baselines are recalculated
    - 'memory_response' for historical queries
    
    Subscribes to:
    - 'observation' messages (to build history)
    - 'insight' messages (to learn from patterns)
    - 'query_history' requests
    """
    
    def __init__(
        self,
        message_bus: MessageBus,
        storage_path: Optional[str] = None,
        baseline_window_days: int = 30
    ):
        self.storage_path = Path(storage_path) if storage_path else Path("data/memory")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.baseline_window = timedelta(days=baseline_window_days)
        
        # In-memory stores
        self.baselines: Dict[str, Dict] = {}
        self.learned_patterns: List[Dict] = []
        
        super().__init__("memory_agent", message_bus)
        self._load_memory()
    
    def _setup_subscriptions(self):
        """Subscribe to observations and insights."""
        self.message_bus.subscribe('observation', self._handle_observation)
        self.message_bus.subscribe('insight', self._handle_insight)
        self.message_bus.subscribe('alert', self._handle_alert)
        self.message_bus.subscribe('query_history', self._handle_query)
        self.message_bus.subscribe('save_memory', self._save_memory)
    
    def process(self, message: Message) -> Optional[Message]:
        """Process incoming messages."""
        if message.type == 'observation':
            return self._handle_observation(message)
        elif message.type == 'insight':
            return self._handle_insight(message)
        elif message.type == 'query_history':
            return self._handle_query(message)
        return None
    
    def _handle_observation(self, message: Message):
        """Store observation and update baselines."""
        obs = message.data
        species = obs.get('species', 'unknown')
        
        # Update baseline statistics
        if species not in self.baselines:
            self.baselines[species] = {
                'first_seen': message.timestamp,
                'last_seen': message.timestamp,
                'total_sightings': 0,
                'locations': defaultdict(int),
                'hourly_activity': defaultdict(int),
                'confidence_scores': []
            }
        
        baseline = self.baselines[species]
        baseline['last_seen'] = message.timestamp
        baseline['total_sightings'] += 1
        
        # Location tracking
        camera_id = obs.get('camera_id', 'unknown')
        baseline['locations'][camera_id] += 1
        
        # Time tracking
        hour = message.timestamp.hour
        baseline['hourly_activity'][hour] += 1
        
        # Confidence tracking
        confidence = obs.get('confidence', 0)
        baseline['confidence_scores'].append(confidence)
        
        # Update state
        self.update_state(f'baseline_{species}', baseline)
        
        logger.debug(f"Updated baseline for {species}")
    
    def _handle_insight(self, message: Message):
        """Store learned insights."""
        insight = message.data.copy()
        insight['learned_at'] = message.timestamp
        insight['source'] = message.sender
        
        self.learned_patterns.append(insight)
        
        # Update state
        total_patterns = self.get_state('total_patterns', 0)
        self.update_state('total_patterns', total_patterns + 1)
        
        logger.info(f"Learned new pattern: {insight.get('type')}")
    
    def _handle_alert(self, message: Message):
        """Store alerts in memory."""
        alert = message.data.copy()
        alert['occurred_at'] = message.timestamp
        
        # Store in learned patterns with high priority
        alert['priority'] = 'alert'
        self.learned_patterns.append(alert)
        
        logger.warning(f"Stored alert: {alert.get('description')}")
    
    def _handle_query(self, message: Message):
        """Handle historical queries."""
        query_type = message.data.get('type')
        
        if query_type == 'baseline':
            species = message.data.get('species')
            baseline = self.get_baseline(species)
            self.publish('memory_response', {'baseline': baseline})
        
        elif query_type == 'patterns':
            species = message.data.get('species')
            patterns = self.get_learned_patterns(species)
            self.publish('memory_response', {'patterns': patterns})
        
        elif query_type == 'summary':
            summary = self.get_memory_summary()
            self.publish('memory_response', summary)
    
    def get_baseline(self, species: str) -> Optional[Dict[str, Any]]:
        """Get baseline behavior for a species."""
        return self.baselines.get(species)
    
    def get_learned_patterns(self, species: Optional[str] = None) -> List[Dict]:
        """Get learned patterns, optionally filtered by species."""
        if species:
            return [p for p in self.learned_patterns if p.get('species') == species]
        return self.learned_patterns
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Get summary of memory state."""
        return {
            'total_species_tracked': len(self.baselines),
            'total_patterns_learned': len(self.learned_patterns),
            'species_baselines': {
                species: {
                    'total_sightings': data['total_sightings'],
                    'first_seen': data['first_seen'].isoformat(),
                    'last_seen': data['last_seen'].isoformat(),
                    'primary_location': max(data['locations'].items(), key=lambda x: x[1])[0] if data['locations'] else None
                }
                for species, data in self.baselines.items()
            }
        }
    
    def _save_memory(self, message: Message = None):
        """Persist memory to disk."""
        try:
            # Save baselines
            baselines_data = {}
            for species, data in self.baselines.items():
                baselines_data[species] = {
                    'first_seen': data['first_seen'].isoformat(),
                    'last_seen': data['last_seen'].isoformat(),
                    'total_sightings': data['total_sightings'],
                    'locations': dict(data['locations']),
                    'hourly_activity': dict(data['hourly_activity']),
                    'avg_confidence': sum(data['confidence_scores']) / len(data['confidence_scores']) if data['confidence_scores'] else 0
                }
            
            with open(self.storage_path / 'baselines.json', 'w') as f:
                json.dump(baselines_data, f, indent=2)
            
            # Save learned patterns
            patterns_data = []
            for pattern in self.learned_patterns:
                pattern_copy = pattern.copy()
                if 'learned_at' in pattern_copy:
                    pattern_copy['learned_at'] = pattern_copy['learned_at'].isoformat()
                if 'occurred_at' in pattern_copy:
                    pattern_copy['occurred_at'] = pattern_copy['occurred_at'].isoformat()
                patterns_data.append(pattern_copy)
            
            with open(self.storage_path / 'patterns.json', 'w') as f:
                json.dump(patterns_data, f, indent=2)
            
            logger.info(f"Memory persisted to {self.storage_path}")
            
        except Exception as e:
            logger.error(f"Failed to save memory: {e}")
    
    def _load_memory(self):
        """Load memory from disk."""
        try:
            # Load baselines
            baselines_file = self.storage_path / 'baselines.json'
            if baselines_file.exists():
                with open(baselines_file, 'r') as f:
                    baselines_data = json.load(f)
                
                for species, data in baselines_data.items():
                    self.baselines[species] = {
                        'first_seen': datetime.fromisoformat(data['first_seen']),
                        'last_seen': datetime.fromisoformat(data['last_seen']),
                        'total_sightings': data['total_sightings'],
                        'locations': defaultdict(int, data['locations']),
                        'hourly_activity': defaultdict(int, data['hourly_activity']),
                        'confidence_scores': []
                    }
                
                logger.info(f"Loaded {len(self.baselines)} species baselines")
            
            # Load patterns
            patterns_file = self.storage_path / 'patterns.json'
            if patterns_file.exists():
                with open(patterns_file, 'r') as f:
                    patterns_data = json.load(f)
                
                for pattern in patterns_data:
                    if 'learned_at' in pattern:
                        pattern['learned_at'] = datetime.fromisoformat(pattern['learned_at'])
                    if 'occurred_at' in pattern:
                        pattern['occurred_at'] = datetime.fromisoformat(pattern['occurred_at'])
                    self.learned_patterns.append(pattern)
                
                logger.info(f"Loaded {len(self.learned_patterns)} learned patterns")
        
        except Exception as e:
            logger.warning(f"Could not load memory: {e}")
