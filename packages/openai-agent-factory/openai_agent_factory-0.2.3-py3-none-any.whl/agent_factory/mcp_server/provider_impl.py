"""
Implementation of the MCP server provider using SSE transport.

This module implements both SSE and stdio transports but defaults to SSE
as specified in the requirements.
"""

from __future__ import annotations

import os
import shutil
from contextlib import AsyncExitStack
from typing import Dict, List, Optional, Union
from typing_extensions import Self

from agents.mcp import MCPServerSse, MCPServerStdio
from agents.mcp.server import MCPServerStdioParams

# Create a type alias for the server types
MCPServer = Union[MCPServerSse, MCPServerStdio]

from .config import MCPServerConfig
from .provider import MCPServerProvider


class MCPServerProviderImpl(MCPServerProvider):
    """Manages multiple MCP server instances as one async context manager.

    This provider supports both stdio and SSE transports, with SSE being the
    recommended approach for production use.

    Usage::

        config = {"kubernetes": {"type": "sse", "url": "http://localhost:3000/sse"}}
        async with MCPServerProviderImpl(config) as provider:
            k8s_server = provider.get_server("kubernetes")
    """

    def __init__(
        self, config: Dict[str, MCPServerConfig], *, include_system_env: bool = True
    ) -> None:
        """Initialize the MCP server provider.

        Args:
            config: Dictionary mapping server names to their configurations
                   Each server config should follow the MCPServerConfig schema
            include_system_env: Whether to include system environment variables
                              when executing stdio servers

        Raises:
            ValueError: If the configuration is invalid
        """
        self._config = config
        self._include_system_env = include_system_env
        self._servers: Dict[str, MCPServer] = {}
        self._stack: Optional[AsyncExitStack] = None
        self._validate()

    async def __aenter__(self) -> Self:
        """Enter the async context manager.

        This initializes all configured MCP servers.

        Returns:
            This provider instance
        """
        self._stack = AsyncExitStack()
        await self._enter_servers()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the async context manager.

        This cleans up all MCP server resources.

        Returns:
            True if exceptions were handled, False otherwise
        """
        if self._stack is None:
            return

        try:
            await self._stack.aclose()
        except Exception as eg:
            import logging
            import traceback

            logging.error(
                "Error while cleaning MCP servers – suppressed: %s",
                " ".join(traceback.format_exception(eg)),
            )

    def get_servers(self) -> List[MCPServer]:
        """Get all active MCP server instances.

        Returns:
            List of all MCP server instances
        """
        return list(self._servers.values())

    def get_server(self, name: str) -> MCPServer:
        """Get a specific MCP server by name.

        Args:
            name: Logical name of the server

        Returns:
            MCP server instance

        Raises:
            KeyError: If the server name is not found
        """
        try:
            return self._servers[name]
        except KeyError as exc:
            raise KeyError(f"Server '{name}' not found; available: {list(self._servers)}") from exc

    def get_servers_by_names(self, names: List[str]) -> List[MCPServer]:
        """Get multiple MCP server instances by their names.

        Args:
            names: List of server names to retrieve

        Returns:
            List of MCP server instances

        Raises:
            KeyError: If any of the requested server names is not found
        """
        return [self.get_server(name) for name in names]

    # Alias for convenience – allows ``provider["kubernetes"]``
    __getitem__ = get_server

    def _validate(self) -> None:
        """Validate the configuration.

        Raises:
            ValueError: If the configuration is invalid
        """
        if not isinstance(self._config, dict):
            raise ValueError(
                "Config must be a dictionary mapping server names to their configurations"
            )

    async def _enter_servers(self) -> None:
        """Initialize and enter all configured MCP servers."""
        assert self._stack is not None  # for type checkers

        for name, spec in self._config.items():
            # Determine the transport type based on spec
            transport_type = spec.type

            # Handle SSE transport type
            has_url = False
            try:
                if spec.sse_params is not None:
                    has_url = "url" in spec.sse_params and spec.sse_params["url"] is not None
            except (TypeError, AttributeError):
                has_url = False

            if transport_type == "sse" or (transport_type is None and has_url):
                if not has_url:
                    raise ValueError(f"SSE server '{name}' requires a 'url' parameter")

                # Create MCPServerSse with proper params
                server = await self._stack.enter_async_context(
                    MCPServerSse(name=name, params=spec.sse_params)
                )
                self._servers[name] = server
                continue

            # Handle stdio transport type
            has_command = False
            cmd = None
            try:
                if spec.stdio_params is not None:
                    has_command = (
                        "command" in spec.stdio_params and spec.stdio_params["command"] is not None
                    )
                    if has_command:
                        cmd = spec.stdio_params["command"]
            except (TypeError, AttributeError):
                has_command = False

            if transport_type == "stdio" or (transport_type is None and has_command):
                if not cmd:
                    raise ValueError(f"stdio server '{name}' requires a 'command' parameter")
                if shutil.which(cmd) is None:
                    raise RuntimeError(f"Executable '{cmd}' for '{name}' not found on PATH")

                # Build environment variables
                final_env: Dict[str, str] = {}
                if self._include_system_env:
                    final_env.update(os.environ)

                # Get env from stdio params if available
                if "env" in spec.stdio_params and spec.stdio_params["env"]:
                    final_env.update(spec.stdio_params["env"])

                # Create modified params dictionary with updated environment
                final_params: MCPServerStdioParams = {**spec.stdio_params}

                # Update with final environment
                if final_env:
                    final_params["env"] = final_env

                # Create MCPServerStdio with proper params
                server = await self._stack.enter_async_context(
                    MCPServerStdio(name=name, params=final_params)
                )
                self._servers[name] = server
