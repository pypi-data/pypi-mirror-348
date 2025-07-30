"""
Manager for MCP server connections that enables resource sharing across agents.
"""

from __future__ import annotations

from contextlib import AsyncExitStack
from typing import Dict, Any, List, Optional
from typing_extensions import Self

from .config import MCPServerConfig
from .provider import MCPServerProvider
from .provider_impl import MCPServerProviderImpl


class MCPServerManager:
    """Creates and manages MCP server connections with lifecycle control.

    Handles provider initialization, server lookup, and connection lifecycle.
    Supports both context manager pattern and explicit initialization:

    # Context manager approach
    async with MCPServerManager(config) as manager:
        servers = manager.get_servers()

    # Explicit initialization
    manager = MCPServerManager(config)
    await manager.initialize()
    servers = manager.get_servers()
    await manager.shutdown()
    """

    def __init__(self, config: Dict[str, MCPServerConfig]):
        """Initialize the manager.

        Args:
            config: Configuration dictionary mapping server names to their configurations.
                   Example: {"kubernetes": {"type": "sse", "url": "http://localhost:3000/sse"}}
                   Each value must follow the MCPServerConfig schema.
        """
        if not isinstance(config, dict):
            raise ValueError("Config must be a dictionary")

        self._exit_stack = AsyncExitStack()
        self._provider: MCPServerProvider | None = None
        self._config = config

    async def __aenter__(self) -> Self:
        """Enter the async context manager.

        Initializes the MCP server provider if not already initialized.

        Returns:
            The MCPServerManager instance
        """
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the async context manager.

        Properly cleans up all MCP server resources.

        Returns:
            True if exceptions were handled, False otherwise
        """
        await self.shutdown()

    async def initialize(self) -> Self:
        """Initialize the MCP server manager with the provided configuration.

        This explicit initialization method is an alternative to using the async context manager.

        Returns:
            The MCPServerManager instance

        Raises:
            ValueError: If the configuration is invalid
        """
        # Skip initialization if provider already exists
        if self._provider is not None:
            return self

        # Create and initialize the provider
        self._provider = await self._exit_stack.enter_async_context(
            MCPServerProviderImpl(self._config)
        )

        return self

    async def shutdown(self) -> None:
        """Shutdown the MCP server manager and clean up resources.

        This explicit cleanup method is an alternative to using the async context manager.
        """
        if self._provider is not None:
            await self._exit_stack.aclose()
            self._provider = None

    def get_provider(self) -> Optional[MCPServerProvider]:
        """Get the shared MCP server provider instance.

        Returns:
            The shared MCP server provider or None if not initialized.
        """
        return self._provider

    def get_servers_by_names(self, server_names: List[str]) -> List[Any]:
        """Get MCP servers by their names.

        Args:
            server_names: List of server names to retrieve

        Returns:
            List of MCP server instances

        Raises:
            RuntimeError: If the provider is not initialized
            KeyError: If any of the requested server names is not found
        """
        if self._provider is None:
            raise RuntimeError(
                "MCP Server Manager not initialized. Call initialize() or use async with."
            )

        return self._provider.get_servers_by_names(server_names)
