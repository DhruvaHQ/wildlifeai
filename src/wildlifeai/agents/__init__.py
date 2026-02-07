"""
WildlifeAI Cognitive Agent System

Multi-agent architecture for autonomous ecological intelligence.
"""

from wildlifeai.agents.base import Agent, Message, MessageBus, AgentRegistry
from wildlifeai.agents.vision_agent import VisionAgent
from wildlifeai.agents.insight_agent import InsightAgent
from wildlifeai.agents.memory_agent import MemoryAgent
from wildlifeai.agents.reporter_agent import ReporterAgent
from wildlifeai.agents.controller import ControllerAgent

__all__ = [
    'Agent',
    'Message',
    'MessageBus',
    'AgentRegistry',
    'VisionAgent',
    'InsightAgent',
    'MemoryAgent',
    'ReporterAgent',
    'ControllerAgent',
]
