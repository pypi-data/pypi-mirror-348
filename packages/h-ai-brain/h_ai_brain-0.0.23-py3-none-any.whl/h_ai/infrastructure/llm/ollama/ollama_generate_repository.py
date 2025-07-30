import uuid

import requests

from ..llm_response_cleaner import clean_llm_response
from ....domain.reasoning.llm_generate_respository import LlmGenerateRepository


class OllamaGenerateRepository(LlmGenerateRepository):

    def __init__(self, api_url: str, model_name: str, system_prompt: str = None, temperature: float = None, seed: int = None, max_tokens: int = 5000, api_token: str = None):
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.api_url = api_url
        self.temperature = temperature
        self.seed = seed
        self.max_tokens = max_tokens
        self.api_token = api_token


    def generate(self, user_prompt: str, system_prompt: str = None, session_id: str = None, max_tokens: int = None) -> str|None:
        url = f"{self.api_url}/generate"
        random_guid = uuid.uuid4()
        guid_str = str(random_guid)
        system_prompt = system_prompt or self.system_prompt
        payload = {
            "model": self.model_name,
            "prompt": user_prompt,
            "system": system_prompt,
            "stream": False,
            "session": guid_str,
            "num_ctx": f"{self.max_tokens}",
            "temperature": f"{self.temperature}"
        }

        if session_id:
            payload["session"] = session_id
        if self.seed:
            payload["seed"] = f"{self.seed}"
        if self.temperature:
            payload["temperature"] = f"{self.temperature}"
        if max_tokens:
            payload["num_ctx"] = f"{max_tokens}"

        headers = {}
        if self.api_token:
            headers["Authorization"]="Bearer "+self.api_token

        try:
            #print(payload)
            response = requests.post(url, json=payload, headers=headers)

            response.raise_for_status()

            #print(response.json())

            response_content = response.json()["response"]
            return clean_llm_response(response_content)

        except requests.exceptions.RequestException as e:
            print(f"Error occurred during API call: {e}")
            return None

