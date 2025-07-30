"""Configuration models for Model Context Protocol (MCP) server connections."""

from typing import Dict, Optional, Literal, Any, cast
from pydantic import BaseModel, Field, model_validator, ConfigDict

from agents.mcp.server import MCPServerSseParams, MCPServerStdioParams


class MCPServerConfig(BaseModel):
    """Connection configuration for a single MCP server instance."""

    type: Optional[Literal["sse", "stdio"]] = None

    config_fields: Dict[str, Any] = Field(default_factory=dict, exclude=True)

    @model_validator(mode="before")
    @classmethod
    def collect_all_fields(cls, data):
        if isinstance(data, dict):
            config_fields = {}
            for k, v in data.items():
                if k != "type":
                    config_fields[k] = v
            data["config_fields"] = config_fields
        return data

    @property
    def sse_params(self) -> MCPServerSseParams:
        return cast(MCPServerSseParams, self.config_fields)

    @property
    def stdio_params(self) -> MCPServerStdioParams:
        return cast(MCPServerStdioParams, self.config_fields)

    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)
