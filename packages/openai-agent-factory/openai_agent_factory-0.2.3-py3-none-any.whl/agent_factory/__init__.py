"""
Agent Factory SDK

A toolkit for creating and managing OpenAI Agents.
"""

from .mcp_server import (
    MCPServerManager,
    MCPServerProvider,
    MCPServerProviderImpl,
    MCPServerConfig,
)
from .agent import (
    AgentConfig,
    AgentFactory,
    AgentFactoryConfig,
    AzureOpenAIConfig,
    AgentServiceFactory,
    ModelSettings,
)

__all__ = [
    # Core components
    "MCPServerManager",
    "MCPServerProvider",
    "MCPServerProviderImpl",
    "MCPServerConfig",
    "AgentConfig",
    "AgentFactoryConfig",
    "AzureOpenAIConfig",
    "AgentFactory",
    "AgentServiceFactory",
    "ModelSettings",
]

__version__ = "0.2.3"
