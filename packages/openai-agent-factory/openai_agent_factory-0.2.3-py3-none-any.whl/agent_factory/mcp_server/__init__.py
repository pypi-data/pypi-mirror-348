"""
Model Context Protocol (MCP) server integration.

Provides components for configuring and managing connections to MCP servers.
"""

from .config import MCPServerConfig
from .provider import MCPServerProvider
from .manager import MCPServerManager

# Implementation details not exposed in public API

__all__ = [
    # Manager
    "MCPServerManager",
    # Configuration
    "MCPServerConfig",
    # Provider interface
    "MCPServerProvider",
]
