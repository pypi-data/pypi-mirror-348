from abc import ABC, abstractmethod
from typing import List

from ...domain.reasoning.tool_message import ToolMessage


class LlmToolRepository(ABC):
    """
    Repository for tool interactions with an LLM.
    """

    @abstractmethod
    def find_tools_in_message(self, message: str) -> List[ToolMessage] | None:
        """
        Extract tool calls from a message.

        Args:
            message: The message to extract tool calls from.

        Returns:
            List[ToolMessage] | None: A list of tool messages, or None if no tools were found.
        """
        ...

    @abstractmethod
    def build_tool_response_prompt(self, question: str, tool_results: list[str]) -> str | None:
        """
        Build a prompt for the LLM to respond to tool results.

        Args:
            question: The original question that triggered the tool calls.
            tool_results: The results from executing the tools.

        Returns:
            str | None: The prompt for the LLM, or None if the prompt could not be built.
        """
        ...
