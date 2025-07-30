"""
Agent factory implementation.

Creates and manages OpenAI agents with configured models and MCP server integrations.
"""

from __future__ import annotations

import logging
from contextlib import AsyncExitStack
from typing import Dict
from typing_extensions import Self

from openai import AsyncAzureOpenAI
from agents import Agent, ModelSettings, OpenAIChatCompletionsModel

from ..mcp_server import MCPServerManager
from .config import AgentConfig, AgentFactoryConfig, AzureOpenAIConfig


logger = logging.getLogger(__name__)


class AgentFactory:
    """Factory for creating and managing OpenAI agents.

    Creates agent instances from AgentFactoryConfig, resolves dependencies between
    agents and MCP servers, and manages the lifecycle of all components.

    Supports both async context manager pattern and explicit initialization:

    # Context manager approach
    async with AgentFactory(config) as factory:
        agent = factory.get_agent("agent_name")

    # Explicit initialization
    factory = AgentFactory(config)
    await factory.initialize()
    agent = factory.get_agent("agent_name")
    await factory.shutdown()
    """

    def __init__(self, config: AgentFactoryConfig):
        """Initialize the agent factory.

        Args:
            config: Configuration for the agent factory including MCP servers and agent definitions
        """
        self._config = config
        self._exit_stack = AsyncExitStack()
        self._mcp_server_manager: MCPServerManager | None = None
        self._agents: Dict[str, Agent] = {}
        self._models: Dict[str, OpenAIChatCompletionsModel] = {}

    async def _create_agent(self, config: AgentConfig) -> Agent:
        """Create an agent based on its configuration.

        This is an internal method used during initialization to create agents.

        Args:
            config: Agent configuration

        Returns:
            Initialized Agent instance

        Raises:
            RuntimeError: If MCP server manager is not properly initialized
            KeyError: If a required MCP server is not available
            ValueError: If there are no models configured or initialized
        """
        # Ensure we're initialized with MCP servers
        if self._mcp_server_manager is None:
            raise RuntimeError("MCP server manager not initialized")

        # Get MCP servers that this agent needs
        mcp_servers = self._mcp_server_manager.get_servers_by_names(config.mcp_servers)

        # Determine which model to use
        model = None
        if config.model:
            if config.model in self._models:
                # Use the specified model
                model = self._models[config.model]
            else:
                # Throw an exception if the specified model is not found
                raise ValueError(f"Model '{config.model}' not found in configured models")
        elif self._models:
            # If no model is specified but models are available, use the first one
            model = next(iter(self._models.values()))

        # Create agent with specific model and model settings
        model_settings_kwargs = {}

        # Use model_settings if provided, otherwise use default values
        if config.model_settings:
            for field_name, value in config.model_settings.model_dump(exclude_unset=True).items():
                if value is not None:
                    model_settings_kwargs[field_name] = value

        # Create ModelSettings from the kwargs
        model_settings = ModelSettings(**model_settings_kwargs)

        # Log the model settings for debugging
        logger.debug(
            f"Creating agent '{config.name}' with model settings: {model_settings.to_json_dict()}"
        )

        agent = Agent(
            name=config.name,
            instructions=config.instructions,
            mcp_servers=mcp_servers,
            model=model,
            model_settings=model_settings,
        )

        # Store the agent for later reference
        self._agents[config.name] = agent

        logger.info(f"Created agent: {config.name}")
        return agent

    def get_agent(self, name: str) -> Agent:
        """Get an existing agent by name.

        Args:
            name: Agent name

        Returns:
            Agent instance

        Raises:
            KeyError: If the agent does not exist
        """
        if name not in self._agents:
            raise KeyError(f"Agent not found: {name}")
        return self._agents[name]

    def get_all_agents(self) -> Dict[str, Agent]:
        """Get all created agents.

        Returns:
            Dictionary mapping agent names to agent instances
        """
        return self._agents

    # TODO: Implement multi-agent collaboration with handoff mechanism
    # This will be implemented in a future version to support agent dependencies

    async def __aenter__(self) -> Self:
        """Enter async context manager.

        Initializes the MCP server manager and other resources.

        Returns:
            Self instance
        """
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit async context manager and clean up resources.

        This ensures proper cleanup of all resources, especially the MCP servers.
        """
        await self.shutdown()

    async def initialize(self) -> Self:
        """Initialize the agent factory with the provided configuration.

        This explicit initialization method is an alternative to using the async context manager.
        During initialization, all agents defined in the config are created and made available
        through the get_agent and get_all_agents methods.

        Returns:
            Self instance
        """
        # Skip if already initialized
        if self._mcp_server_manager is not None:
            return self

        # Validate config by calling check_mcp_servers directly
        # The validate_mcp_servers is a model validator and not meant to be called directly
        self._config.check_mcp_servers(self._config.agents, lambda agent: agent.mcp_servers)

        # Initialize MCP server manager
        self._mcp_server_manager = await self._exit_stack.enter_async_context(
            MCPServerManager(self._config.mcp_servers)
        )

        # Initialize OpenAI models if any are configured
        if self._config.openai_models:
            self._models = self._initialize_models()

        # Create all agents defined in the config
        for agent_config in self._config.agents:
            await self._create_agent(agent_config)

        return self

    async def shutdown(self) -> None:
        """Shutdown all components and clean up resources.

        This method provides an alternative to the async context manager pattern.
        """
        # This will properly close all resources registered with the exit stack
        await self._exit_stack.aclose()
        self._mcp_server_manager = None
        self._models = {}

    def _create_azure_openai_client(self, config: AzureOpenAIConfig) -> AsyncAzureOpenAI:
        """Create an Azure OpenAI client from configuration.

        Args:
            config: Azure OpenAI configuration

        Returns:
            Configured AsyncAzureOpenAI client
        """
        deployment = config.model

        return AsyncAzureOpenAI(
            api_key=config.api_key,
            api_version=config.api_version,
            azure_endpoint=str(config.endpoint),
            azure_deployment=deployment,
        )

    def _initialize_models(self) -> Dict[str, OpenAIChatCompletionsModel]:
        """Initialize models based on the configurations in AgentFactoryConfig.

        Returns:
            Dictionary mapping model names to initialized OpenAIChatCompletionsModel instances

        Raises:
            ValueError: If the model configuration is of an unsupported type
        """
        models = {}

        for model_config in self._config.openai_models:
            if isinstance(model_config, AzureOpenAIConfig):
                client = self._create_azure_openai_client(model_config)

                # Create the model without temperature (we'll pass it to Agent instead)
                # Ensure model is not None before using it as a key or parameter
                if model_config.model is not None:
                    models[model_config.model] = OpenAIChatCompletionsModel(
                        model=model_config.model, openai_client=client
                    )
                else:
                    # Use a default model name if none is provided
                    default_model = "gpt-4"
                    models[default_model] = OpenAIChatCompletionsModel(
                        model=default_model, openai_client=client
                    )
            else:
                raise ValueError(f"Unsupported model configuration type: {type(model_config)}")

        return models
