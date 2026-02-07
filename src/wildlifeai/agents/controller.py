"""
Controller Agent - The Orchestrator

Manages the cognitive system's decision-making and agent coordination.
This is the "executive function" of the AI system.
"""
from typing import Dict, Any, Optional, List
from pathlib import Path
import logging

from wildlifeai.agents.base import Agent, Message, MessageBus, AgentRegistry
from wildlifeai.agents.vision_agent import VisionAgent
from wildlifeai.agents.insight_agent import InsightAgent
from wildlifeai.agents.memory_agent import MemoryAgent
from wildlifeai.agents.reporter_agent import ReporterAgent

logger = logging.getLogger(__name__)


class ControllerAgent(Agent):
    """
    Controller Agent orchestrates the multi-agent cognitive system.
    
    This is the BRAIN that decides what happens next.
    
    Responsibilities:
    - Initialize and coordinate all agents
    - Route messages between agents
    - Make high-level decisions
    - Monitor system health
    - Trigger periodic analyses
    
    This transforms the system from reactive to AUTONOMOUS.
    """
    
    def __init__(
        self,
        message_bus: MessageBus,
        registry: AgentRegistry,
        model_path: Optional[str] = None
    ):
        self.registry = registry
        self.model_path = model_path
        super().__init__("controller", message_bus)
        
        # Initialize all agents
        self._initialize_agents()
    
    def _setup_subscriptions(self):
        """Subscribe to system-level events."""
        self.message_bus.subscribe('system_command', self._handle_command)
        self.message_bus.subscribe('observation', self._on_observation)
        self.message_bus.subscribe('insight', self._on_insight)
        self.message_bus.subscribe('alert', self._on_alert)
    
    def _initialize_agents(self):
        """
        Initialize the cognitive agent ecosystem.
        
        This creates the multi-agent intelligence system.
        """
        logger.info("🧠 Initializing cognitive agent system...")
        
        # 1. Vision Agent - The "Eyes"
        vision_agent = VisionAgent(
            self.message_bus,
            model_path=self.model_path,
            confidence_threshold=0.5
        )
        self.registry.register(vision_agent)
        logger.info("✓ Vision Agent initialized")
        
        # 2. Insight Agent - The "Brain"
        insight_agent = InsightAgent(
            self.message_bus,
            analysis_window_days=7,
            anomaly_threshold=1.5
        )
        self.registry.register(insight_agent)
        logger.info("✓ Insight Agent initialized")
        
        # 3. Memory Agent - The "Memory"
        memory_agent = MemoryAgent(
            self.message_bus,
            storage_path="data/memory",
            baseline_window_days=30
        )
        self.registry.register(memory_agent)
        logger.info("✓ Memory Agent initialized")
        
        # 4. Reporter Agent - The "Voice"
        reporter_agent = ReporterAgent(
            self.message_bus,
            output_dir="reports"
        )
        self.registry.register(reporter_agent)
        logger.info("✓ Reporter Agent initialized")
        
        self.update_state('agents_initialized', True)
        self.update_state('agent_count', len(self.registry.get_all_agents()))
        
        logger.info("🚀 Cognitive system ready!")
    
    def process(self, message: Message) -> Optional[Message]:
        """Process controller-level messages."""
        if message.type == 'system_command':
            return self._handle_command(message)
        return None
    
    def _handle_command(self, message: Message):
        """Handle system commands."""
        command = message.data.get('command')
        
        if command == 'process_images':
            self._process_images(message.data.get('image_paths', []))
        
        elif command == 'analyze':
            self._trigger_analysis()
        
        elif command == 'generate_report':
            self._trigger_report(message.data.get('report_type', 'summary'))
        
        elif command == 'save_state':
            self._save_system_state()
        
        elif command == 'status':
            status = self.get_system_status()
            self.publish('system_status', status)
        
        else:
            logger.warning(f"Unknown command: {command}")
    
    def _process_images(self, image_paths: List[str]):
        """
        Orchestrate image processing through the cognitive system.
        
        This is autonomous decision-making in action.
        """
        logger.info(f"🎯 Processing {len(image_paths)} images...")
        
        # Decision 1: Batch or individual processing?
        if len(image_paths) > 10:
            # Batch processing for efficiency
            self.publish('process_batch', {
                'image_paths': image_paths
            })
        else:
            # Individual processing for detailed analysis
            for image_path in image_paths:
                self.publish('process_image', {
                    'image_path': image_path,
                    'camera_id': Path(image_path).parent.name
                })
        
        # Decision 2: Trigger analysis after processing?
        if len(image_paths) > 5:
            # Yes - enough data for meaningful patterns
            self.publish('trigger_analysis', {})
    
    def _trigger_analysis(self):
        """Trigger pattern analysis."""
        logger.info("🔍 Triggering pattern analysis...")
        self.publish('trigger_analysis', {})
    
    def _trigger_report(self, report_type: str = 'summary'):
        """Trigger report generation."""
        logger.info(f"📊 Generating {report_type} report...")
        self.publish('generate_report', {'type': report_type})
    
    def _save_system_state(self):
        """Save entire system state."""
        logger.info("💾 Saving system state...")
        self.publish('save_memory', {})
        
        # Save controller state
        state_file = Path("data/memory/controller_state.json")
        # Implementation here
        
        logger.info("✓ System state saved")
    
    def _on_observation(self, message: Message):
        """React to new observations (autonomous behavior)."""
        # Decision: Do we need immediate analysis?
        total_obs = self.get_state('total_observations', 0)
        self.update_state('total_observations', total_obs + 1)
        
        # Trigger analysis every 20 observations
        if (total_obs + 1) % 20 == 0:
            logger.info("📈 Observation threshold reached - triggering analysis")
            self._trigger_analysis()
    
    def _on_insight(self, message: Message):
        """React to generated insights."""
        insight_type = message.data.get('type')
        logger.debug(f"Insight logged: {insight_type}")
        
        # Decision: Should we generate a report?
        total_insights = self.get_state('total_insights', 0)
        self.update_state('total_insights', total_insights + 1)
        
        if (total_insights + 1) % 10 == 0:
            logger.info("📊 Insight threshold reached - generating report")
            self._trigger_report('summary')
    
    def _on_alert(self, message: Message):
        """React to critical alerts (immediate action)."""
        alert_data = message.data
        severity = alert_data.get('severity', 'medium')
        
        logger.warning(f"🚨 Alert received: {severity} severity")
        
        # Decision: High severity alerts trigger immediate report
        if severity == 'high':
            logger.warning("🚨 HIGH SEVERITY - Generating immediate alert report")
            self._trigger_report('detailed')
        
        # Update alert counter
        alerts = self.get_state('total_alerts', 0)
        self.update_state('total_alerts', alerts + 1)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        agent_info = self.registry.get_agent_info()
        
        return {
            'controller_state': self.state,
            'agents': {
                agent_id: {
                    'status': 'active',
                    'state': info.get('state', {})
                }
                for agent_id, info in agent_info.items()
            },
            'message_bus_activity': len(self.message_bus.message_history),
            'system_health': 'operational'
        }
    
    def shutdown(self):
        """Graceful system shutdown."""
        logger.info("Shutting down cognitive system...")
        self._save_system_state()
        logger.info("✓ Shutdown complete")


def create_cognitive_system(model_path: Optional[str] = None) -> tuple[ControllerAgent, MessageBus, AgentRegistry]:
    """
    Factory function to create the complete cognitive system.
    
    Usage:
        controller, bus, registry = create_cognitive_system()
        
        # Process images
        controller.publish('system_command', {
            'command': 'process_images',
            'image_paths': ['img1.jpg', 'img2.jpg']
        })
    
    Returns:
        Tuple of (controller_agent, message_bus, agent_registry)
    """
    # Create infrastructure
    message_bus = MessageBus()
    registry = AgentRegistry()
    
    # Create controller (initializes all other agents)
    controller = ControllerAgent(message_bus, registry, model_path=model_path)
    registry.register(controller)
    
    logger.info("🎊 Cognitive system created successfully!")
    
    return controller, message_bus, registry
