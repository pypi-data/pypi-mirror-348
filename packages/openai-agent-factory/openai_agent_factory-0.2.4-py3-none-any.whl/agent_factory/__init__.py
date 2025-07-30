"""
Agent Factory SDK

A toolkit for creating and managing OpenAI Agents.
"""

# Core classes needed for basic functionality
from .agent.factory import AgentFactory
from .agent.config import AgentFactoryConfig, AgentConfig, AzureOpenAIConfig, ModelSettings

# Users need to import more specialized components from subpackages

__all__ = [
    # Primary entry points and their required configuration classes
    "AgentFactory",
    "AgentFactoryConfig",
    "AgentConfig",
    "AzureOpenAIConfig",
    "ModelSettings",
]

__version__ = "0.2.4"
