"""
Reporter Agent - Scientific Narrative Generation

Converts insights and alerts into scientific reports and narratives.
Makes the system's findings human-readable and actionable.
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
import json
import logging

from wildlifeai.agents.base import Agent, Message, MessageBus

logger = logging.getLogger(__name__)


class ReporterAgent(Agent):
    """
    Reporter Agent generates scientific narratives from insights.
    
    Transforms raw patterns into actionable conservation intelligence.
    
    Capabilities:
    - Generate summary reports
    - Create alert notifications
    - Produce scientific narratives
    - Export findings in multiple formats
    
    Publishes:
    - 'report' messages with formatted findings
    
    Subscribes to:
    - 'insight' messages
    - 'alert' messages
    - 'generate_report' requests
    """
    
    def __init__(
        self,
        message_bus: MessageBus,
        output_dir: Optional[str] = None
    ):
        self.output_dir = Path(output_dir) if output_dir else Path("reports")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.insights_buffer: List[Dict] = []
        self.alerts_buffer: List[Dict] = []
        
        super().__init__("reporter_agent", message_bus)
    
    def _setup_subscriptions(self):
        """Subscribe to insights and alerts."""
        self.message_bus.subscribe('insight', self._handle_insight)
        self.message_bus.subscribe('alert', self._handle_alert)
        self.message_bus.subscribe('generate_report', self._generate_report)
    
    def process(self, message: Message) -> Optional[Message]:
        """Process incoming messages."""
        if message.type == 'insight':
            return self._handle_insight(message)
        elif message.type == 'alert':
            return self._handle_alert(message)
        elif message.type == 'generate_report':
            return self._generate_report(message)
        return None
    
    def _handle_insight(self, message: Message):
        """Store insight for reporting."""
        insight = message.data.copy()
        insight['timestamp'] = message.timestamp
        insight['sender'] = message.sender
        self.insights_buffer.append(insight)
        
        # Auto-generate narrative insight
        narrative = self._create_insight_narrative(insight)
        logger.info(f"📊 INSIGHT: {narrative}")
        
        # Update count
        count = self.get_state('insights_reported', 0)
        self.update_state('insights_reported', count + 1)
    
    def _handle_alert(self, message: Message):
        """Handle critical alerts."""
        alert = message.data.copy()
        alert['timestamp'] = message.timestamp
        alert['sender'] = message.sender
        self.alerts_buffer.append(alert)
        
        # Generate alert narrative
        narrative = self._create_alert_narrative(alert)
        logger.warning(f"🚨 ALERT: {narrative}")
        
        # Publish formatted alert
        self.publish('report', {
            'type': 'alert',
            'narrative': narrative,
            'data': alert
        })
        
        count = self.get_state('alerts_reported', 0)
        self.update_state('alerts_reported', count + 1)
    
    def _create_insight_narrative(self, insight: Dict[str, Any]) -> str:
        """
        Convert insight data into scientific narrative.
        
        This is where data becomes knowledge.
        """
        insight_type = insight.get('type')
        
        if insight_type == 'temporal_pattern':
            species = insight.get('species')
            pattern = insight.get('pattern')
            ratio = insight.get('nocturnal_ratio', 0)
            return (
                f"{species} exhibits {pattern} behavior pattern with "
                f"{ratio:.0%} of activity during nighttime hours. "
                f"This suggests adaptation to predator avoidance or thermal regulation."
            )
        
        elif insight_type == 'spatial_pattern':
            species = insight.get('species')
            location = insight.get('dominant_location')
            concentration = insight.get('concentration', 0)
            return (
                f"{species} shows strong territorial preference for {location}, "
                f"accounting for {concentration:.0%} of all sightings. "
                f"This indicates established territory or critical resource availability."
            )
        
        elif insight_type == 'species_interaction':
            sp1, sp2 = insight.get('species_pair', ['', ''])
            count = insight.get('co_occurrence_count', 0)
            return (
                f"{sp1} and {sp2} co-occur frequently ({count} instances), "
                f"suggesting shared habitat preferences or possible predator-prey dynamics."
            )
        
        else:
            return insight.get('description', 'Pattern detected')
    
    def _create_alert_narrative(self, alert: Dict[str, Any]) -> str:
        """
        Convert alert data into actionable narrative.
        
        Critical for conservation decision-making.
        """
        alert_type = alert.get('type')
        
        if alert_type == 'activity_spike':
            species = alert.get('species')
            ratio = alert.get('increase_ratio', 0)
            severity = alert.get('severity', 'medium')
            causes = alert.get('possible_causes', [])
            
            narrative = (
                f"⚠️ ANOMALY DETECTED: {species} activity has increased {ratio:.1f}x "
                f"above baseline (Severity: {severity.upper()}). "
            )
            
            if causes:
                narrative += f"\nPossible ecological factors: {causes[0]}"
            
            narrative += "\n\nRecommended action: Investigate environmental changes in affected zones."
            
            return narrative
        
        return alert.get('description', 'Alert condition detected')
    
    def _generate_report(self, message: Message = None):
        """Generate comprehensive scientific report."""
        report_type = message.data.get('type', 'summary') if message else 'summary'
        
        if report_type == 'summary':
            report = self._create_summary_report()
        elif report_type == 'detailed':
            report = self._create_detailed_report()
        else:
            report = {'error': 'Unknown report type'}
        
        # Save to file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = self.output_dir / f"{report_type}_report_{timestamp}.json"
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"Report generated: {report_path}")
        
        # Publish report
        self.publish('report', {
            'type': 'generated_report',
            'report_path': str(report_path),
            'report': report
        })
        
        return report
    
    def _create_summary_report(self) -> Dict[str, Any]:
        """Create summary report of all findings."""
        return {
            'report_type': 'summary',
            'generated_at': datetime.now().isoformat(),
            'total_insights': len(self.insights_buffer),
            'total_alerts': len(self.alerts_buffer),
            'key_findings': [
                self._create_insight_narrative(insight)
                for insight in self.insights_buffer[-5:]  # Last 5 insights
            ],
            'critical_alerts': [
                self._create_alert_narrative(alert)
                for alert in self.alerts_buffer
            ],
            'insights_by_type': self._group_by_type(self.insights_buffer),
            'alert_severity_distribution': self._count_severity(self.alerts_buffer)
        }
    
    def _create_detailed_report(self) -> Dict[str, Any]:
        """Create detailed scientific report."""
        return {
            'report_type': 'detailed',
            'generated_at': datetime.now().isoformat(),
            'executive_summary': self._create_executive_summary(),
            'insights': {
                'total': len(self.insights_buffer),
                'by_type': self._group_by_type(self.insights_buffer),
                'narratives': [
                    {
                        'insight': insight,
                        'narrative': self._create_insight_narrative(insight)
                    }
                    for insight in self.insights_buffer
                ]
            },
            'alerts': {
                'total': len(self.alerts_buffer),
                'by_severity': self._count_severity(self.alerts_buffer),
                'narratives': [
                    {
                        'alert': alert,
                        'narrative': self._create_alert_narrative(alert)
                    }
                    for alert in self.alerts_buffer
                ]
            },
            'recommendations': self._generate_recommendations()
        }
    
    def _create_executive_summary(self) -> str:
        """Create executive summary for report."""
        total_insights = len(self.insights_buffer)
        total_alerts = len(self.alerts_buffer)
        
        summary = f"Wildlife Monitoring Summary\n\n"
        summary += f"Analyzed {total_insights} ecological patterns and detected {total_alerts} anomalies.\n\n"
        
        if total_alerts > 0:
            summary += "CRITICAL FINDINGS:\n"
            for alert in self.alerts_buffer[:3]:
                summary += f"- {self._create_alert_narrative(alert)}\n"
        
        return summary
    
    def _group_by_type(self, items: List[Dict]) -> Dict[str, int]:
        """Group items by type and count."""
        counts = {}
        for item in items:
            item_type = item.get('type', 'unknown')
            counts[item_type] = counts.get(item_type, 0) + 1
        return counts
    
    def _count_severity(self, alerts: List[Dict]) -> Dict[str, int]:
        """Count alerts by severity."""
        counts = {'high': 0, 'medium': 0, 'low': 0}
        for alert in alerts:
            severity = alert.get('severity', 'medium')
            counts[severity] = counts.get(severity, 0) + 1
        return counts
    
    def _generate_recommendations(self) -> List[str]:
        """Generate conservation recommendations based on findings."""
        recommendations = []
        
        # Based on alerts
        if self.alerts_buffer:
            high_severity = [a for a in self.alerts_buffer if a.get('severity') == 'high']
            if high_severity:
                recommendations.append(
                    "URGENT: Investigate high-severity anomalies immediately. "
                    "Deploy field teams to affected zones."
                )
        
        # Based on patterns
        temporal_patterns = [i for i in self.insights_buffer if i.get('type') == 'temporal_pattern']
        if temporal_patterns:
            recommendations.append(
                "Consider adjusting patrol schedules to align with detected activity patterns "
                "for improved monitoring efficiency."
            )
        
        if not recommendations:
            recommendations.append("Continue routine monitoring. No immediate action required.")
        
        return recommendations
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get reporter statistics."""
        return {
            'insights_reported': len(self.insights_buffer),
            'alerts_reported': len(self.alerts_buffer),
            'reports_generated': self.get_state('reports_generated', 0),
            'output_directory': str(self.output_dir)
        }
