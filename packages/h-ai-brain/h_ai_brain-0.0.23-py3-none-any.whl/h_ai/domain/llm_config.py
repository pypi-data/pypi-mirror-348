class LLMConfig:
    def __init__(self, url: str, model_name: str, temperature: float = 0.6, max_tokens: int = 2500, api_token: str = None):
        self.url = url
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_token = api_token