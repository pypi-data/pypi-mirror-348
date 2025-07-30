from abc import ABC, abstractmethod
from typing import List

from ...domain.reasoning.tool_message import ToolMessage


class LlmToolRepository(ABC):
    @abstractmethod
    def find_tools_in_message(self, message: str) -> List[ToolMessage] | None:
        ...

    @abstractmethod
    def build_tool_response_prompt(self, question: str, tool_results: list[str])-> str|None:
        ...
