"""
MCP Server provider interface.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class MCPServerProvider(ABC):
    """Interface for components that provide MCP server instances."""

    @abstractmethod
    async def __aenter__(self) -> "MCPServerProvider":
        """Initialize the MCP server provider."""
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Clean up the MCP server provider."""
        pass

    @abstractmethod
    def get_servers(self) -> List[Any]:
        """Get all available MCP servers."""
        pass

    @abstractmethod
    def get_server(self, name: str) -> Any:
        """Get a specific MCP server by name."""
        pass

    @abstractmethod
    def get_servers_by_names(self, names: List[str]) -> List[Any]:
        """Get multiple MCP servers by their names."""
        pass
