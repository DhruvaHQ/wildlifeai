"""
Insight Agent - THE KILLER FEATURE

Analyzes patterns in observations and generates ecological insights.
This is what transforms the system from "detection" to "intelligence".

The Insight Agent doesn't just collect data - it REASONS about it.
"""
from typing import Dict, Any, Optional, List
from collections import defaultdict, Counter
from datetime import datetime, timedelta
import logging
import statistics

from wildlifeai.agents.base import Agent, Message, MessageBus

logger = logging.getLogger(__name__)


class InsightAgent(Agent):
    """
    Insight Agent performs ecological pattern analysis and reasoning.
    
    This is the "brain" of the cognitive system.
    
    Capabilities:
    - Temporal pattern detection (activity changes)
    - Spatial analysis (territory shifts)
    - Behavioral anomalies (unusual patterns)
    - Species interactions (co-occurrence)
    - Population trends (abundance changes)
    
    Publishes:
    - 'insight' messages when patterns are detected
    - 'alert' messages for significant anomalies
    
    Subscribes to:
    - 'observation' messages from Vision Agent
    - 'query_insights' requests
    """
    
    def __init__(
        self,
        message_bus: MessageBus,
        analysis_window_days: int = 7,
        anomaly_threshold: float = 1.5  # 50% above baseline
    ):
        self.analysis_window = timedelta(days=analysis_window_days)
        self.anomaly_threshold = anomaly_threshold
        self.observations: List[Dict] = []
        super().__init__("insight_agent", message_bus)
    
    def _setup_subscriptions(self):
        """Subscribe to observations."""
        self.message_bus.subscribe('observation', self._handle_observation)
        self.message_bus.subscribe('query_insights', self._handle_query)
        self.message_bus.subscribe('trigger_analysis', self._analyze_all)
    
    def process(self, message: Message) -> Optional[Message]:
        """Process incoming messages."""
        if message.type == 'observation':
            return self._handle_observation(message)
        elif message.type == 'query_insights':
            return self._handle_query(message)
        elif message.type == 'trigger_analysis':
            return self._analyze_all(message)
        return None
    
    def _handle_observation(self, message: Message):
        """Store observation and analyze for patterns."""
        observation = message.data
        observation['timestamp'] = message.timestamp
        self.observations.append(observation)
        
        # Update state
        total_obs = self.get_state('total_observations', 0)
        self.update_state('total_observations', total_obs + 1)
        
        # Periodic analysis trigger
        if len(self.observations) % 10 == 0:  # Analyze every 10 observations
            self._analyze_patterns()
        
        logger.debug(f"Stored observation: {observation.get('species')}")
    
    def _analyze_patterns(self):
        """
        Core intelligence: Analyze observation patterns for insights.
        
        This is where the magic happens - autonomous ecological reasoning.
        """
        if len(self.observations) < 5:
            return  # Need minimum data
        
        # Run different analysis types
        self._analyze_temporal_patterns()
        self._analyze_spatial_patterns()
        self._analyze_species_interactions()
        self._detect_anomalies()
        
        logger.info("Pattern analysis complete")
    
    def _analyze_temporal_patterns(self):
        """Analyze time-based activity patterns."""
        # Group observations by species and hour
        species_by_hour = defaultdict(lambda: defaultdict(int))
        
        for obs in self.observations:
            species = obs.get('species', 'unknown')
            timestamp = obs.get('timestamp', datetime.now())
            hour = timestamp.hour
            species_by_hour[species][hour] += 1
        
        # Detect nocturnal vs diurnal patterns
        for species, hourly_counts in species_by_hour.items():
            night_hours = sum(hourly_counts.get(h, 0) for h in range(0, 6) + range(20, 24))
            day_hours = sum(hourly_counts.get(h, 0) for h in range(6, 20))
            total = night_hours + day_hours
            
            if total > 0:
                nocturnal_ratio = night_hours / total
                
                if nocturnal_ratio > 0.7:
                    insight = {
                        'type': 'temporal_pattern',
                        'species': species,
                        'pattern': 'nocturnal',
                        'nocturnal_ratio': nocturnal_ratio,
                        'confidence': 'high' if total > 20 else 'medium',
                        'description': f"{species} shows strong nocturnal activity pattern ({nocturnal_ratio:.0%} of sightings at night)"
                    }
                    self.publish('insight', insight)
                    logger.info(f"Insight: {species} is primarily nocturnal")
    
    def _analyze_spatial_patterns(self):
        """Analyze location-based patterns."""
        # Group by species and camera/location
        species_locations = defaultdict(Counter)
        
        for obs in self.observations:
            species = obs.get('species', 'unknown')
            camera_id = obs.get('camera_id', 'unknown')
            species_locations[species][camera_id] += 1
        
        # Detect territory preferences
        for species, locations in species_locations.items():
            if len(locations) > 1:
                total_sightings = sum(locations.values())
                dominant_location = locations.most_common(1)[0]
                location_id, count = dominant_location
                
                concentration = count / total_sightings
                
                if concentration > 0.6:  # 60% in one location
                    insight = {
                        'type': 'spatial_pattern',
                        'species': species,
                        'dominant_location': location_id,
                        'concentration': concentration,
                        'total_locations': len(locations),
                        'description': f"{species} shows strong preference for {location_id} ({concentration:.0%} of sightings)"
                    }
                    self.publish('insight', insight)
                    logger.info(f"Insight: {species} territorial pattern detected")
    
    def _analyze_species_interactions(self):
        """Analyze species co-occurrence patterns."""
        # Group observations by camera and time window (1 hour)
        time_windows = defaultdict(list)
        
        for obs in self.observations:
            camera = obs.get('camera_id', 'unknown')
            timestamp = obs.get('timestamp', datetime.now())
            # Round to hour
            window_key = (camera, timestamp.replace(minute=0, second=0, microsecond=0))
            time_windows[window_key].append(obs.get('species'))
        
        # Find co-occurrences
        co_occurrences = defaultdict(int)
        for species_list in time_windows.values():
            if len(species_list) > 1:
                unique_species = set(species_list)
                for sp1 in unique_species:
                    for sp2 in unique_species:
                        if sp1 < sp2:  # Avoid duplicates
                            co_occurrences[(sp1, sp2)] += 1
        
        # Report significant co-occurrences
        for (sp1, sp2), count in co_occurrences.items():
            if count >= 3:  # At least 3 co-occurrences
                insight = {
                    'type': 'species_interaction',
                    'species_pair': [sp1, sp2],
                    'co_occurrence_count': count,
                    'description': f"{sp1} and {sp2} frequently detected together ({count} instances)"
                }
                self.publish('insight', insight)
                logger.info(f"Insight: {sp1}/{sp2} co-occurrence detected")
    
    def _detect_anomalies(self):
        """
        Detect unusual patterns that deviate from baseline.
        
        This generates ALERTS for significant changes.
        """
        # Calculate baseline sighting frequency
        species_counts = Counter(obs.get('species') for obs in self.observations)
        
        # Analyze recent activity vs historical
        now = datetime.now()
        recent_cutoff = now - timedelta(days=1)  # Last 24 hours
        historical_cutoff = now - timedelta(days=7)  # Previous week
        
        recent_sightings = Counter(
            obs.get('species') for obs in self.observations
            if obs.get('timestamp', now) > recent_cutoff
        )
        
        historical_sightings = Counter(
            obs.get('species') for obs in self.observations
            if historical_cutoff > obs.get('timestamp', now) > recent_cutoff
        )
        
        # Detect spikes
        for species in set(recent_sightings.keys()) | set(historical_sightings.keys()):
            recent_count = recent_sightings.get(species, 0)
            historical_avg = historical_sightings.get(species, 0) / 7  # Per day
            
            if historical_avg > 0:
                ratio = recent_count / historical_avg
                
                if ratio > self.anomaly_threshold:
                    # ANOMALY DETECTED!
                    alert = {
                        'type': 'activity_spike',
                        'species': species,
                        'recent_count': recent_count,
                        'baseline_avg': historical_avg,
                        'increase_ratio': ratio,
                        'severity': 'high' if ratio > 2.0 else 'medium',
                        'description': f"ANOMALY: {species} activity increased {ratio:.1f}x above baseline",
                        'possible_causes': self._suggest_ecological_causes('spike', species)
                    }
                    self.publish('alert', alert)
                    logger.warning(f"ALERT: {species} activity spike detected!")
    
    def _suggest_ecological_causes(self, pattern_type: str, species: str) -> List[str]:
        """
        Suggest possible ecological explanations for detected patterns.
        
        This is CORE to scientific value - providing context and hypotheses.
        """
        if pattern_type == 'spike':
            return [
                "Migration pattern or seasonal movement",
                "Resource abundance (water, food) in area",
                "Displacement from other territories",
                "Breeding season behavior",
                "Response to human activity changes"
            ]
        elif pattern_type == 'decline':
            return [
                "Seasonal migration out of area",
                "Resource scarcity (drought, food shortage)",
                "Increased predation pressure",
                "Habitat disturbance",
                "Competition from other species"
            ]
        return ["Requires further investigation"]
    
    def _analyze_all(self, message: Message = None):
        """Trigger comprehensive analysis."""
        logger.info("Running comprehensive analysis...")
        self._analyze_patterns()
    
    def _handle_query(self, message: Message):
        """Handle insight query requests."""
        query_type = message.data.get('type', 'summary')
        
        if query_type == 'summary':
            summary = self.get_summary()
            self.publish('insight_response', summary)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all insights and patterns."""
        species_counts = Counter(obs.get('species') for obs in self.observations)
        
        # Calculate observation statistics
        if self.observations:
            timestamps = [obs.get('timestamp', datetime.now()) for obs in self.observations]
            time_span = max(timestamps) - min(timestamps) if len(timestamps) > 1 else timedelta(0)
        else:
            time_span = timedelta(0)
        
        return {
            'total_observations': len(self.observations),
            'unique_species': len(species_counts),
            'species_counts': dict(species_counts.most_common(10)),
            'time_span_days': time_span.days,
            'observation_rate': len(self.observations) / max(time_span.days, 1) if time_span.days > 0 else 0,
            'insights_generated': self.get_state('total_observations', 0)
        }
    
    def get_insights_by_type(self, insight_type: str) -> List[Dict]:
        """Get all insights of a specific type from message history."""
        insights = []
        for msg in self.message_bus.get_history('insight'):
            if msg.data.get('type') == insight_type:
                insights.append(msg.data)
        return insights
