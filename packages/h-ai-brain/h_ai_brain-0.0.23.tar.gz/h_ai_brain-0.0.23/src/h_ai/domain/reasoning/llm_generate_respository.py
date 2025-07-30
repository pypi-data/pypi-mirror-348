from typing import Protocol


class LlmGenerateRepository(Protocol):
    def generate(self, user_prompt: str, system_prompt: str, session_id: str = None) -> str:
        ...