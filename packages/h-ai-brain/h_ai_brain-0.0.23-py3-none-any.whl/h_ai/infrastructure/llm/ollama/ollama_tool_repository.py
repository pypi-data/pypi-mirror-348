import json
from typing import Dict, Any

import requests

from ..prompt_helper import replace_placeholders
from ....domain.reasoning.llm_tool_repository import LlmToolRepository
from ....domain.reasoning.tool_message import ToolMessage


class OllamaToolRepository(LlmToolRepository):

    def __init__(self, api_url: str, model_name: str, tools: list, tool_prompt: str, tool_response_prompt: str, temperature: float = None, seed: int = None):
        self.model_name = model_name
        self.api_url = api_url
        self.tools = tools
        self.tool_prompt = tool_prompt
        self.tool_response_prompt = tool_response_prompt
        self.temperature = temperature
        self.seed = seed

    def find_tools_in_message(self, message: str) -> list[ToolMessage] | None:
        url = f"{self.api_url}/generate"

        placeholders = {
            "$available_tools_placeholder": {json.dumps(self.tools, indent=2)},
        }
        system_message_tools = replace_placeholders(self.tool_prompt, placeholders)

        payload = {
            "model": self.model_name,
            "prompt": message,
            "stream": False,
            "system": system_message_tools,
            "num_ctx": "2500",
            "temperature": "0.6"
        }

        if self.seed:
            payload["seed"] = self.seed
        if self.temperature:
            payload["temperature"] = self.temperature

        try:
            print(payload)
            response = requests.post(url, json=payload)
            response.raise_for_status()

            print(response.json())

            found_tool_definitions = self._process_tool_response(response.json())
            if found_tool_definitions:
                tool_messages = []
                for tool_definition in found_tool_definitions:
                    tool_message = ToolMessage()
                    tool_message.method_name = tool_definition.get("tool")
                    tool_message.method_params = tool_definition.get("parameters",{})
                    tool_messages.append(tool_message)

                return tool_messages
            else:
                return None

        except requests.exceptions.RequestException as e:
            print(f"Error occurred during API call: {e}")
            return None

    def build_tool_response_prompt(self, question:str, tool_results: list[str]):
        placeholders = {
            "$tools_question_placeholder": question,
            "$tools_response_context_placeholder": tool_results,
        }
        return replace_placeholders(self.tool_response_prompt, placeholders)

    def _process_tool_response(self, response: Dict[str, Any]) -> list[dict] | None:
        try:
            text = response.get('response', '')

            tool_calls = self._parse_json_string(text)

            if isinstance(tool_calls, dict):
                tool_calls = [tool_calls]

            if isinstance(tool_calls, list):
                valid_calls = [
                    call for call in tool_calls
                    if isinstance(call, dict) and 'tool' in call
                ]
                return valid_calls if valid_calls else None

        except json.JSONDecodeError:
            return None

        return None

    def _parse_json_string(self, input_str: str) -> list[dict] | None:
        if not input_str or not input_str.strip():
            return None

        try:
            return json.loads(input_str)
        except json.JSONDecodeError:
            cleaned = self._clean_json_string(input_str)
            if not cleaned:
                return None

            json_objects = []
            current_pos = 0

            while True:
                try:
                    start = cleaned.find('{', current_pos)
                    if start == -1:
                        break

                    decoder = json.JSONDecoder()
                    obj, end = decoder.raw_decode(cleaned[start:])
                    json_objects.append(obj)
                    current_pos = start + end
                except json.JSONDecodeError:
                    current_pos += 1
                    continue
                except Exception:
                    break

            if not json_objects:
                return None
            return json_objects

    @staticmethod
    def _clean_json_string(input_str: str) -> str:
        cleaned = input_str.replace('```json', '').replace('```', '')
        cleaned = cleaned.strip("'").strip('"')
        cleaned = cleaned.strip()
        return cleaned



