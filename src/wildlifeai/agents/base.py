"""
Base Agent class for WildlifeAI cognitive architecture.

This module defines the foundation for the multi-agent system that enables
autonomous ecological reasoning and insight generation.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)


@dataclass
class Message:
    """
    Message passed between agents in the cognitive system.
    
    Attributes:
        type: Message type (e.g., 'observation', 'insight', 'alert')
        sender: Agent ID that created the message
        data: Message payload
        timestamp: When message was created
        metadata: Additional context
    """
    type: str
    sender: str
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            'type': self.type,
            'sender': self.sender,
            'data': self.data,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        """Create message from dictionary."""
        return cls(
            type=data['type'],
            sender=data['sender'],
            data=data['data'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            metadata=data.get('metadata', {})
        )


class MessageBus:
    """
    Central message bus for agent communication.
    
    Implements publish-subscribe pattern for event-driven architecture.
    Agents publish messages, other agents subscribe to message types.
    """
    
    def __init__(self):
        self.subscribers: Dict[str, List[callable]] = {}
        self.message_history: List[Message] = []
        
    def subscribe(self, message_type: str, handler: callable):
        """Subscribe to a message type."""
        if message_type not in self.subscribers:
            self.subscribers[message_type] = []
        self.subscribers[message_type].append(handler)
        logger.debug(f"Subscribed to {message_type}")
    
    def publish(self, message: Message):
        """Publish a message to all subscribers."""
        self.message_history.append(message)
        
        if message.type in self.subscribers:
            for handler in self.subscribers[message.type]:
                try:
                    handler(message)
                except Exception as e:
                    logger.error(f"Handler error for {message.type}: {e}")
        
        logger.debug(f"Published {message.type} from {message.sender}")
    
    def get_history(self, message_type: Optional[str] = None, limit: int = 100) -> List[Message]:
        """Get message history, optionally filtered by type."""
        if message_type:
            messages = [m for m in self.message_history if m.type == message_type]
        else:
            messages = self.message_history
        return messages[-limit:]


class Agent(ABC):
    """
    Base class for all agents in the cognitive system.
    
    Each agent has:
    - Unique ID and role
    - Access to message bus for communication
    - Ability to process messages and make decisions
    - State management
    """
    
    def __init__(self, agent_id: str, message_bus: MessageBus):
        self.agent_id = agent_id
        self.message_bus = message_bus
        self.state: Dict[str, Any] = {}
        self._setup_subscriptions()
        logger.info(f"Agent {self.agent_id} initialized")
    
    @abstractmethod
    def _setup_subscriptions(self):
        """Setup which message types this agent subscribes to."""
        pass
    
    @abstractmethod
    def process(self, message: Message) -> Optional[Message]:
        """
        Process an incoming message and optionally return a response.
        
        This is the core intelligence of each agent.
        """
        pass
    
    def publish(self, message_type: str, data: Dict[str, Any], metadata: Optional[Dict] = None):
        """Publish a message to the bus."""
        message = Message(
            type=message_type,
            sender=self.agent_id,
            data=data,
            metadata=metadata or {}
        )
        self.message_bus.publish(message)
    
    def update_state(self, key: str, value: Any):
        """Update agent's internal state."""
        self.state[key] = value
        logger.debug(f"{self.agent_id} state updated: {key}")
    
    def get_state(self, key: str, default: Any = None) -> Any:
        """Get value from agent's state."""
        return self.state.get(key, default)
    
    def get_info(self) -> Dict[str, Any]:
        """Get agent information and status."""
        return {
            'agent_id': self.agent_id,
            'state': self.state,
            'subscriptions': list(self.message_bus.subscribers.keys())
        }


class AgentRegistry:
    """
    Registry for managing all agents in the system.
    
    Provides centralized access to agents and their capabilities.
    """
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
    
    def register(self, agent: Agent):
        """Register a new agent."""
        self.agents[agent.agent_id] = agent
        logger.info(f"Registered agent: {agent.agent_id}")
    
    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get agent by ID."""
        return self.agents.get(agent_id)
    
    def get_all_agents(self) -> List[Agent]:
        """Get all registered agents."""
        return list(self.agents.values())
    
    def get_agent_info(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all agents."""
        return {
            agent_id: agent.get_info()
            for agent_id, agent in self.agents.items()
        }
