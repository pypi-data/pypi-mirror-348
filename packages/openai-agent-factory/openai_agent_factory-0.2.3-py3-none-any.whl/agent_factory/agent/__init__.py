"""
Agent components for OpenAI integration.

Provides factory classes and configurations for creating and managing OpenAI agents.
"""

from .config import AgentConfig, AgentFactoryConfig, AzureOpenAIConfig, ModelSettings
from .factory import AgentFactory
from .service_factory import AgentServiceFactory
from agents import set_tracing_disabled

__all__ = [
    # Factories
    "AgentFactory",
    "AgentServiceFactory",
    # Configuration
    "AgentConfig",
    "AgentFactoryConfig",
    "AzureOpenAIConfig",
    "ModelSettings",
    # Tracing utilities
    "disable_tracing",
    "enable_tracing",
]


def disable_tracing():
    """Disables model tracing to optimize performance."""
    set_tracing_disabled(True)


def enable_tracing():
    """Enables model tracing for debugging and monitoring."""
    set_tracing_disabled(False)


# Default to disabled tracing for performance
disable_tracing()
