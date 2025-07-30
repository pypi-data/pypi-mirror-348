#!/usr/bin/env python3
"""
Command-line interface for agent interaction.

Provides a CLI tool for creating and interacting with multiple agents
through a console-based chat interface.
"""

import argparse
import asyncio
import logging
import os
import sys
from typing import Any, Dict, Optional, List, cast

from agents import Runner
from dotenv import load_dotenv

from agent_factory import AgentFactoryConfig, AgentFactory

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentCLI:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.factory: Optional[AgentFactory] = None

    async def initialize(self):
        try:
            logger.debug("Starting initialization of AgentCLI")
            config = self._load_config()
            logger.debug("Creating AgentFactory instance")
            self.factory = AgentFactory(config)
            logger.debug("Initializing AgentFactory")
            await self.factory.initialize()
            logger.debug("AgentFactory initialization completed successfully")
            return self.factory
        except Exception as e:
            logger.error(f"Failed to initialize AgentFactory: {e}", exc_info=True)
            raise

    def _load_config(self) -> AgentFactoryConfig:
        try:
            # Use the from_file method to load configuration directly
            logger.debug(f"Loading configuration from file: {self.config_path}")
            config: AgentFactoryConfig = AgentFactoryConfig.from_file(self.config_path)

            logger.debug(f"Configuration loaded successfully: {config}")
            logger.debug(f"Config agents: {config.agents}")
            logger.debug(f"Config MCP servers: {config.mcp_servers}")
            logger.debug(f"Config OpenAI models: {config.openai_models}")

            for i, agent in enumerate(config.agents):
                logger.debug(f"Agent {i+1}: {agent.name}")
                logger.debug(f"  - Model: {agent.model}")
                logger.debug(f"  - MCP Servers: {agent.mcp_servers}")
                logger.debug(f"  - Metadata: {agent.metadata}")

            for i, model in enumerate(config.openai_models):
                logger.debug(f"OpenAI Model {i+1}: {model.model}")
                logger.debug(f"  - API Key present: {'Yes' if model.api_key else 'No'}")
                logger.debug(f"  - Endpoint present: {'Yes' if model.endpoint else 'No'}")
                logger.debug(f"  - API Version: {model.api_version}")

            return config
        except Exception as e:
            logger.error(f"Failed to load configuration from {self.config_path}: {e}")
            raise

    async def shutdown(self):
        if self.factory:
            try:
                await self.factory.shutdown()
            except Exception as e:
                logger.error(f"Error during shutdown: {e}")
            finally:
                self.factory = None

    def list_agents(self) -> List[str]:
        if not self.factory:
            return []

        return list(self.factory.get_all_agents().keys())

    def get_agent(self, name: str):
        if not self.factory:
            logger.error("Attempted to get agent but factory is not initialized")
            raise RuntimeError("Factory not initialized")

        logger.debug(f"Getting agent: {name}")
        try:
            agent = self.factory.get_agent(name)
            logger.debug(f"Successfully retrieved agent: {name}")
            return agent
        except Exception as e:
            logger.error(f"Failed to get agent '{name}': {e}", exc_info=True)
            raise


def trim_history(history, max_messages, max_token_limit):
    """
    Intelligently trim conversation history based on both message count and token size.

    Args:
        history (list): List of message dictionaries with 'role' and 'content' keys
        max_messages (int): Maximum number of messages to keep
        max_token_limit (int): Maximum number of tokens to keep

    Returns:
        list: Trimmed history
        bool: Whether history was trimmed
    """
    if not history:
        return history, False

    # Function to estimate tokens in text (approximation: ~4 chars per token for English text)
    def estimate_tokens(text):
        # This is a simple approximation - actual token count depends on the tokenizer
        return len(text) // 4

    # Calculate total estimated tokens in history
    total_tokens = sum(estimate_tokens(msg["content"]) for msg in history)

    # Determine if we need to trim based on either message count or token count
    needs_trimming = len(history) > max_messages or total_tokens > max_token_limit

    if needs_trimming:
        # Start removing messages from the oldest until we're under both limits
        while history and (
            len(history) > max_messages
            or sum(estimate_tokens(msg["content"]) for msg in history) > max_token_limit
        ):
            # Remove 2 messages at a time (a complete turn) to maintain conversation integrity
            if len(history) >= 2:
                history = history[2:]
            else:
                # If only one message left (unusual case), just clear it
                history = []

        # Ensure first message is a user message for consistency
        if history and history[0]["role"] != "user":
            # If first message isn't from user, remove it and the next message
            history = history[2:] if len(history) > 2 else []

        current_tokens = sum(estimate_tokens(msg["content"]) for msg in history)
        logger.debug(f"Trimmed history to {len(history)} messages, ~{current_tokens} tokens")

        return history, True

    return history, False


async def interactive_console(
    agent_cli: AgentCLI,
    agent_name: str,
    max_history: Optional[int] = None,
    max_tokens: Optional[int] = None,
):
    try:
        logger.debug(f"Starting interactive console for agent: {agent_name}")
        agent = agent_cli.get_agent(agent_name)
    except KeyError:
        logger.error(
            f"Agent '{agent_name}' not found. Available agents: {', '.join(agent_cli.list_agents())}"
        )
        print(
            f"\nError: Agent '{agent_name}' not found. Available agents: {', '.join(agent_cli.list_agents())}"
        )
        return

    # Default to a size that works well with GPT-4.1's context window
    # GPT-4.1 supports about 128K tokens, so 500 turns is a reasonable default
    # (assuming average 200-400 tokens per message pair)
    DEFAULT_MAX_HISTORY = 500
    DEFAULT_MAX_TOKENS = 100000  # 100K tokens, leaving room for system instructions and response

    # Use command line args if provided, otherwise use defaults
    history_limit = max_history if max_history is not None else DEFAULT_MAX_HISTORY
    token_limit = max_tokens if max_tokens is not None else DEFAULT_MAX_TOKENS

    print(f"\n{'=' * 50}")
    print(f"Interacting with agent: {agent_name}")
    print(f"{'=' * 50}")
    print("Type 'exit' to quit")
    print("Type 'help' for assistance")
    print("Type 'clear' to start a new conversation")

    # Show history size and token limit info with sources
    history_source = "command line" if max_history is not None else "default"
    token_source = "command line" if max_tokens is not None else "default"
    print(f"History size limit: {history_limit} conversation turns (from {history_source})")
    print(f"Token limit: {token_limit} tokens (from {token_source})")

    print(f"{'=' * 50}\n")

    history: List[Dict[str, str]] = []

    while True:
        try:
            user_input = input("\033[1m> \033[0m")  # Bold prompt

            # Handle special commands
            if user_input.lower() in ("exit", "quit"):
                print("\nGoodbye!")
                break

            if user_input.lower() == "help":
                print("\nCommands:")
                print("  exit/quit - Exit the interactive console")
                print("  clear     - Clear the conversation history")
                print("  help      - Show this help message")
                continue

            if user_input.lower() == "clear":
                history = []
                print("\nConversation cleared.")
                continue

            if not user_input.strip():
                continue

            # Track input in history
            history.append({"role": "user", "content": user_input})

            # Intelligently trim history based on both message count and estimated token size
            max_messages = (
                history_limit * 2
            )  # Each turn consists of a user message and an assistant response

            # Trim history if necessary
            history, was_trimmed = trim_history(history, max_messages, token_limit)

            # If we've completely emptied history, add the current user message back
            if was_trimmed and not history:
                history.append({"role": "user", "content": user_input})

            print("\n\033[3mProcessing...\033[0m")  # Italic processing message

            try:
                logger.debug(f"Running agent with input: {user_input}")
                response = await Runner.run(
                    agent,
                    # the cast is to bypass mypy error
                    cast(List[Any], history),
                )
                logger.debug(
                    f"Agent response received: {response.final_output[:100]}..."
                )  # Log first 100 chars
                history.append({"role": "assistant", "content": response.final_output})

                # Print the response with some formatting
                print(
                    f"\n\033[34m{agent_name}:\033[0m {response.final_output}\n"
                )  # Blue agent name

            except Exception as e:
                logger.error(f"Error running agent: {e}", exc_info=True)
                print(f"\n\033[31mError: {e}\033[0m")  # Red error message

        except KeyboardInterrupt:
            print("\n\nExiting due to user interrupt...")
            break
        except EOFError:
            print("\n\nEnd of input. Exiting...")
            break
        except Exception as e:
            logger.error(f"Unexpected error in interactive console: {e}")
            print(f"\n\033[31mUnexpected error: {e}\033[0m")


async def main():
    parser = argparse.ArgumentParser(
        description="Agent Factory CLI - Interactive tool for working with AI agents"
    )
    parser.add_argument(
        "-c",
        "--config",
        required=True,
        help="Path to the agent configuration YAML file",
    )
    parser.add_argument("-l", "--list", action="store_true", help="List all available agents")
    parser.add_argument("-a", "--agent", help="Name of the agent to interact with")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument(
        "--max-history",
        type=int,
        help="Maximum number of conversation turns to keep in history (default: 500, optimized for GPT-4.1's context window)",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        help="Maximum token limit for conversation history (default: 100000, leaving ~28K tokens for system instructions and response with GPT-4.1)",
    )

    args = parser.parse_args()

    # Configure logging based on verbosity
    if args.verbose:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        logger.setLevel(logging.DEBUG)

        logging.getLogger("agent_factory").setLevel(logging.DEBUG)
        logging.getLogger("agents").setLevel(logging.DEBUG)
    else:
        logging.basicConfig(
            level=logging.WARNING,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        logging.getLogger("openai.agents").setLevel(logging.WARNING)
        logging.getLogger("agent_factory").setLevel(logging.WARNING)
        logging.getLogger("httpx").setLevel(logging.WARNING)

    # Check if config file exists
    if not os.path.exists(args.config):
        print(f"\033[31mError: Configuration file not found: {args.config}\033[0m")
        return 1

    print(f"\n\033[1mAgent Factory CLI\033[0m")
    print(f"Loading configuration from: {args.config}")

    agent_cli = AgentCLI(args.config)

    try:
        # Initialize the agent factory
        print("Initializing agent factory...")
        logger.debug("Starting initialization process for agent factory...")
        await agent_cli.initialize()
        logger.debug("Agent factory initialization completed")

        agents = agent_cli.list_agents()
        logger.debug(f"Available agents: {agents}")

        # List agents if requested or if no agent is specified
        if args.list or not args.agent:
            if not agents:
                print("\033[33mNo agents available in the configuration\033[0m")
            else:
                print(f"\n\033[1mAvailable agents ({len(agents)}):\033[0m")
                for i, name in enumerate(agents, 1):
                    print(f"  {i}. \033[34m{name}\033[0m")
            print()

        # Interact with specified agent or prompt to select one
        if args.agent:
            if args.agent not in agents:
                print(f"\033[31mError: Agent '{args.agent}' not found\033[0m")
                print(f"Available agents: {', '.join(agents)}")
                return 1

            await interactive_console(agent_cli, args.agent, args.max_history, args.max_tokens)
        elif agents and not args.list:
            # Interactive agent selection if no specific agent was requested
            while True:
                try:
                    selection = input("\033[1mSelect an agent number (or 'exit' to quit): \033[0m")
                    if selection.lower() in ("exit", "quit"):
                        break

                    try:
                        idx = int(selection) - 1
                        if 0 <= idx < len(agents):
                            await interactive_console(
                                agent_cli,
                                agents[idx],
                                args.max_history,
                                args.max_tokens,
                            )

                            # After returning from interactive console, ask if user wants to select another agent
                            another = input("\nSelect another agent? (y/n): ")
                            if another.lower() != "y":
                                break
                        else:
                            print(
                                f"\033[33mInvalid selection. Please enter a number between 1 and {len(agents)}.\033[0m"
                            )
                    except ValueError:
                        print("\033[33mPlease enter a valid number or 'exit'.\033[0m")
                except KeyboardInterrupt:
                    print("\n\nExiting due to user interrupt...")
                    break

    except KeyboardInterrupt:
        print("\n\nExiting due to user interrupt...")
        return 0
    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True if args.verbose else False)
        print(f"\n\033[31mError: {e}\033[0m")
        return 1
    finally:
        print("\nShutting down agent factory...")
        await agent_cli.shutdown()

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))


def entry_point():
    sys.exit(asyncio.run(main()))
