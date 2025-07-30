"""Configuration models for agents, factories, and API integrations."""

from typing import Dict, List, Union, Optional, Callable, Any
from pathlib import Path
import json
import yaml
from pydantic import BaseModel, Field, HttpUrl, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from ..mcp_server.config import MCPServerConfig


class AzureOpenAIConfig(BaseSettings):
    """Azure OpenAI API connection and model configuration."""

    api_key: Optional[str] = Field(default=None, description="Azure OpenAI API key")
    api_version: Optional[str] = Field(
        default="2023-12-01-preview",
        description="Azure OpenAI API version",
        json_schema_extra={"env_names": ["OPENAI_API_VERSION", "AZURE_OPENAI_API_VERSION"]},
    )
    endpoint: Optional[HttpUrl] = Field(default=None, description="Azure OpenAI endpoint URL")
    model: str = Field(description="Azure OpenAI deployment name")

    model_config = SettingsConfigDict(
        env_prefix="AZURE_OPENAI_",
        env_file=".env",
        extra="ignore",
    )


class AgentDependency(BaseModel):
    """Configuration for an agent dependency."""

    agent_name: str = Field(description="The name of the dependent agent")
    description: str = Field(description="Description of how this dependency is used")


class ModelSettings(BaseModel):
    """Configuration for model settings."""

    temperature: float = Field(
        default=1.0, description="The temperature to use when calling the model"
    )
    top_p: Optional[float] = Field(
        default=None, description="The top_p to use when calling the model"
    )
    frequency_penalty: Optional[float] = Field(
        default=None, description="The frequency penalty to use when calling the model"
    )
    presence_penalty: Optional[float] = Field(
        default=None, description="The presence penalty to use when calling the model"
    )
    truncation: Optional[str] = Field(default=None, description="The truncation strategy to use")
    max_tokens: Optional[int] = Field(
        default=None, description="The maximum number of output tokens to generate"
    )
    store: Optional[bool] = Field(
        default=None, description="Whether to store the generated model response"
    )
    metadata: Optional[Dict[str, str]] = Field(
        default=None, description="Metadata to include with model response"
    )


class AgentConfig(BaseModel):
    """Defines a single agent's behavior, capabilities, and requirements."""

    name: str = Field(description="Unique identifier for the agent")
    instructions: str = Field(description="System prompt defining agent behavior")
    mcp_servers: List[str] = Field(default_factory=list)
    model: Optional[str] = Field(default=None)
    model_settings: Optional[ModelSettings] = Field(
        default=None, description="LLM generation parameters"
    )
    dependencies: List[AgentDependency] = Field(default_factory=list)
    metadata: Dict[str, Union[str, int, float, bool, List[Any]]] = Field(default_factory=dict)


class FactoryConfigBase(BaseSettings):
    """Base configuration with common settings for factory implementations."""

    mcp_servers: Dict[str, MCPServerConfig] = Field(default_factory=dict)
    openai_models: List[AzureOpenAIConfig] = Field(default_factory=list)

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        extra="ignore",
    )

    @classmethod
    def from_file(cls, file_path: str | Path):
        """Loads and parses configuration from YAML/JSON with environment variable support.

        Environment variables will automatically override values from the file.
        """
        path = Path(file_path)

        with open(path, "r") as f:
            if path.suffix.lower() in [".yaml", ".yml"]:
                config_dict = yaml.safe_load(f)
            elif path.suffix.lower() == ".json":
                config_dict = json.load(f)
            else:
                raise ValueError(
                    f"Unsupported file format: {path.suffix}. Use .yaml, .yml, or .json"
                )

        # Create instance with the actual calling class, environment variables will automatically override values
        return cls.model_validate(config_dict)

    def check_mcp_servers(self, configs: List, get_server_names: Callable) -> None:
        """Ensures all referenced MCP servers exist in the configuration."""
        available_servers = set(self.mcp_servers.keys())
        for config in configs:
            for server_name in get_server_names(config):
                if server_name not in available_servers:
                    raise ValueError(f"Undefined MCP server '{server_name}'")


class AgentFactoryConfig(FactoryConfigBase):
    """Complete configuration for creating and managing multiple agents."""

    agents: List[AgentConfig]

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_prefix="AGENT_FACTORY_",
        env_file=".env",
        extra="ignore",
    )

    @model_validator(mode="after")
    def validate_mcp_servers(self) -> "AgentFactoryConfig":
        self.check_mcp_servers(self.agents, lambda agent: agent.mcp_servers)
        return self
