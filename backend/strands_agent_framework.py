"""
Strands Agent Framework - Python Backend Utilities
Provides context management for Strands Agents framework
"""

import json
import logging
from typing import Any, Dict, Optional
from dataclasses import dataclass, field


logger = logging.getLogger(__name__)


# ============================================================================
# Data Classes for Agent Context Management
# ============================================================================

@dataclass
class AgentContext:
    """
    AgentContext stores and manages data that agents can access during orchestration.
    
    Attributes:
        data: Dictionary storing key-value pairs accessible by all agents
        metadata: Optional metadata about the context
    """
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Optional[Dict[str, Any]] = None

    def get(self, key: str, default: Any = None) -> Any:
        """Get value from context by key."""
        return self.data.get(key, default)

    def get_json(self, key: str) -> Optional[Dict]:
        """Get value as JSON-serializable dict."""
        value = self.data.get(key)
        return json.loads(value) if isinstance(value, str) and value.startswith('{') else None

    def put(self, key: str, value: Any) -> None:
        """Set value in context."""
        self.data[key] = value
        logger.debug(f"Context updated: {key} = {value}")

    def set_json(self, key: str, value: Dict) -> None:
        """Set a value as JSON string."""
        self.data[key] = json.dumps(value)

    def clear(self) -> None:
        """Clear all context data."""
        self.data.clear()
        logger.info("Context cleared")


# ============================================================================
# Utility Functions for Agent Context
# ============================================================================

class ContextUtil:
    """Utility class for agent context operations."""
    
    @staticmethod
    def create_context() -> AgentContext:
        """Create a new empty context."""
        logger.debug("Creating new context")
        return AgentContext()

    @staticmethod
    def get_or_create(context: Optional[AgentContext], key: str) -> Any:
        """Get or create value in context."""
        if context is None:
            context = AgentContext()
        
        value = context.get(key, "NOT_SET")
        
        # Create default value if not set
        if value == "NOT_SET":
            context.put(key, {})
        
        return context.get(key, None)

    @staticmethod
    def merge(context: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
        """Merge two context dictionaries."""
        result = context.copy()
        result.update(update)
        return result

    @staticmethod
    def validate_context(context: Dict[str, Any], required_keys: list) -> bool:
        """Validate that context has required keys."""
        missing = [k for k in required_keys if k not in context]
        if missing:
            logger.warning(f"Context missing required keys: {missing}")
            return False
        return True


# ============================================================================
# Agent Orchestrator Context Manager
# ============================================================================

class AgentContextManager:
    """
    Manages agent context throughout an orchestration run.
    
    Attributes:
        context: The main agent context
        metadata: Metadata about the orchestration run
        history: History of context changes
    """
    
    def __init__(self, metadata: Optional[Dict] = None):
        self.context = AgentContext()
        self.metadata = metadata or {
            "orchestrator": "Strands Agents",
            "version": "1.0.0",
        }
        self.history = []
    
    @staticmethod
    def with_context(f):
        """Decorator to create a new context for a function."""
        def wrapper(*args, **kwargs):
            context = AgentContext()
            try:
                return f(*args, context=context, **kwargs)
            except Exception as e:
                logger.error(f"Context error: {e}")
                raise
        return wrapper

    def save_context_state(self) -> Dict[str, Any]:
        """Save current context state."""
        state = {
            "data": self.context.data.copy(),
            "metadata": self.metadata,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        }
        self.history.append(state)
        return state


# ============================================================================
# JSON Utilities for Agent Communication
# ============================================================================

class JSONSerializer:
    """Serialize/deserialize agent messages."""
    
    @staticmethod
    def serialize(agent_message: Dict[str, Any]) -> str:
        """Serialize agent message to JSON."""
        message = {
            "type": agent_message.get("type", "message"),
            "content": agent_message.get("content"),
            "timestamp": __import__('datetime').datetime.now().isoformat(),
            "metadata": agent_message.get("metadata", {})
        }
        return json.dumps(message, default=str)

    @staticmethod
    def deserialize(json_str: str) -> Dict[str, Any]:
        """Deserialize JSON string back to dict."""
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {e}")
            return {}


# ============================================================================
# Context Persistence
# ============================================================================

class ContextPersistence:
    """Handle context persistence to storage."""
    
    def __init__(self, storage_backend: str = "memory"):
        self.storage_backend = storage_backend
        self.storage = None
    
    def initialize_storage(self):
        """Initialize storage backend."""
        if self.storage_backend == "memory":
            self.storage = {}
            logger.info("Using in-memory storage")
        elif self.storage_backend == "sqlite":
            try:
                import sqlite3
                self.storage = sqlite3.connect('agents_context.db')
                logger.info("Using SQLite storage")
            except Exception as e:
                logger.error(f"SQLite connection failed: {e}")
                self.storage_backend = "memory"
        else:
            logger.warning(f"Unknown storage backend: {self.storage_backend}")
            self.storage_backend = "memory"
    
    def save_context(self, context: AgentContext) -> bool:
        """Save context to storage."""
        if not self.storage:
            self.initialize_storage()
        
        if hasattr(self.storage, '__setitem__'):
            self.storage['context'] = context.data.copy()
            return True
        return True
    
    def load_context(self) -> Optional[AgentContext]:
        """Load context from storage."""
        if not self.storage:
            return AgentContext()
        
        if 'context' in self.storage:
            data = self.storage['context']
            return AgentContext(data=data.copy())
        return AgentContext()