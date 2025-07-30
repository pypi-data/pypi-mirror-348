from typing import Optional, List

import requests

from ....domain.reasoning.llm_chat_repository import LlmChatRepository
from ....infrastructure.llm.llm_response_cleaner import clean_llm_response
from ....infrastructure.llm.ollama.models.ollama_chat_message import OllamaChatMessage
from ....infrastructure.llm.ollama.models.ollama_chat_session import OllamaChatSession


class OllamaChatRepository(LlmChatRepository):

    def __init__(self, api_url: str, model_name: str, system_prompts: list[str] = None, temperature: float = None, seed: int = None):
        self.api_url = api_url
        self.model_name = model_name
        self.temperature = temperature
        self.seed = seed
        self.system_prompts = system_prompts

    def chat(self, user_message: str, session_id: str) -> Optional[str]:

        messages = [OllamaChatMessage("user", user_message)]
        for system_prompt in self.system_prompts:
            messages.append(OllamaChatMessage("system", system_prompt))
        session = OllamaChatSession(session_id, messages)

        return self._call_ollama_api(session.messages)

    def _call_ollama_api(self, messages: List[OllamaChatMessage]) -> Optional[str]:
        url = f"{self.api_url}/chat"
        formatted_messages = [message.to_dict() for message in messages]
        payload = {
            "model": self.model_name,
            "messages": formatted_messages,
            "stream": False,
            "temperature": "0.6"
        }
        if self.temperature:
            payload["temperature"] = self.temperature
        if self.seed:
            payload["seed"] = self.seed

        try:
            print(payload)
            response = requests.post(url, json=payload)
            response.raise_for_status()
            full_response = response.json()["message"]["content"]
            print(full_response)
            return clean_llm_response(full_response)

        except requests.exceptions.RequestException as e:
            print(f"Error occurred during API call: {e}")
            return None



