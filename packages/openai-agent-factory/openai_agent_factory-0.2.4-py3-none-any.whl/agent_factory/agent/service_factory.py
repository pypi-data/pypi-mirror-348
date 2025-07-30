"""
Agent service implementation for HTTP API exposure.

Provides components to expose agents as web endpoints through FastAPI.
"""

import logging
from contextlib import AsyncExitStack

from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse, StreamingResponse

from agents import Runner
from openai.types.responses import ResponseTextDeltaEvent

from .factory import AgentFactory
from .config import AgentFactoryConfig

logger = logging.getLogger(__name__)


class AgentServiceFactory:
    """Exposes agents as HTTP endpoints in a FastAPI application.

    Creates routers with chat and streaming endpoints for each agent
    and manages their lifecycle within a web service.

    Example:
        service_factory = AgentServiceFactory(config)
        await service_factory.initialize()
        service_factory.mount_all(app)  # Add endpoints to FastAPI app
        await service_factory.shutdown()

    Or with context manager:
        async with AgentServiceFactory(config) as service_factory:
            service_factory.mount_all(app)
    """

    def __init__(self, config: AgentFactoryConfig):
        """Initialize the A2A service factory.

        Args:
            config: Configuration for creating A2A services.
        """
        self._config = config
        self._exit_stack = AsyncExitStack()
        self._agent_factory: AgentFactory | None = None
        self._app = FastAPI(title="Agent Service API", version="1.0.0")
        self._router = APIRouter()

    async def initialize(self) -> None:
        """Initialize the A2A service factory.

        This method must be called before using the factory.
        It creates the internal AgentFactory instance and initializes it.
        """
        # Create and initialize the agent factory
        self._agent_factory = await self._exit_stack.enter_async_context(AgentFactory(self._config))

        # Set up base API routes
        self._setup_routes()

        # Set up agent-specific routes
        self._setup_agent_routes()

        # Mount the router to the app
        self._app.include_router(self._router)

    async def shutdown(self) -> None:
        """Shutdown the A2A service factory.

        This method must be called when done using the factory.
        """
        if self._exit_stack:
            await self._exit_stack.aclose()

    async def __aenter__(self):
        """Enter the async context manager."""
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the async context manager."""
        await self.shutdown()

    def _setup_routes(self):
        """Set up the base API routes for agent information."""

        @self._router.get("/", response_class=JSONResponse)
        async def get_root():
            """Get API information."""
            return {
                "name": "Agent Service API",
                "version": "1.0.0",
                "agents": [
                    {
                        "name": agent_config.name,
                        "endpoint": f"/{agent_config.name}",
                        "description": agent_config.metadata.get("description", "No description"),
                    }
                    for agent_config in self._config.agents
                ],
            }

        @self._router.get("/agents", response_class=JSONResponse)
        async def get_agents():
            """Get all available agents."""
            return {
                "agents": [
                    {
                        "name": agent_config.name,
                        "description": agent_config.metadata.get("description", "No description"),
                        "model": agent_config.model,
                        "metadata": agent_config.metadata,
                        "model_settings": (
                            agent_config.model_settings.model_dump()
                            if agent_config.model_settings
                            else None
                        ),
                    }
                    for agent_config in self._config.agents
                ]
            }

    def _setup_agent_routes(self):
        """Set up routes for each agent based on configuration."""
        for agent_config in self._config.agents:
            agent_name = agent_config.name
            agent_router = APIRouter(prefix=f"/agents/{agent_name}")

            # Agent information endpoint
            @agent_router.get("/", response_class=JSONResponse)
            async def get_agent_info(agent_name=agent_name):
                if self._agent_factory is None:
                    raise RuntimeError("Agent factory not initialized. Call initialize() first.")
                agent = self._agent_factory.get_agent(agent_name)
                return {
                    "name": agent_name,
                    "instructions": agent_config.instructions,
                    "model": agent_config.model,
                    "metadata": agent_config.metadata,
                    "model_settings": (
                        agent_config.model_settings.model_dump()
                        if agent_config.model_settings
                        else None
                    ),
                }

            # Stream API endpoint for SSE
            @agent_router.post("/chat/stream")
            async def stream_chat_with_agent(request: Request, agent_name=agent_name):
                if self._agent_factory is None:
                    raise RuntimeError("Agent factory not initialized. Call initialize() first.")
                agent = self._agent_factory.get_agent(agent_name)
                body = await request.body()
                body_str = body.decode("utf-8")

                async def event_generator():
                    async for event in Runner.run_streamed(agent, body_str).stream_events():
                        if event.type == "raw_response_event" and isinstance(
                            event.data, ResponseTextDeltaEvent
                        ):
                            yield event.data.delta

                return StreamingResponse(event_generator(), media_type="text/event-stream")

            # Mount the agent router to the main router
            self._router.include_router(agent_router)

    def mount_to(self, app: FastAPI, prefix: str = "") -> None:
        """Mount this service to a FastAPI application.

        Args:
            app: FastAPI application to mount this service to.
            prefix: Optional URL prefix for all endpoints.
        """
        app.mount(prefix, self._app)

    def get_app(self) -> FastAPI:
        """Get the FastAPI application.

        Returns:
            FastAPI application that can be run or mounted.
        """
        return self._app
