from abc import ABC, abstractmethod
from typing import Optional


class LlmChatRepository(ABC):

    @abstractmethod
    def chat(self, user_message: str, session_id: str) -> Optional[str]:
        ...
