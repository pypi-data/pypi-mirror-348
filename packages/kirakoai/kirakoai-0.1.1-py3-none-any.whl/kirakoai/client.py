import requests
from typing import List
from .models import KirakoMessage
from .exceptions import KirakoError

# Маппинг моделей KirakoAI -> MistralAI
_MODEL_MAPPING = {
    "kirakoai-basic": "mistral-small-latest",
    "kirakoai-pro": "mistral-medium-latest",
    "kirakoai-ultra": "pixtral-large-latest"
}

# Обязательный system prompt
_SYSTEM_PROMPT = {
    "role": "system",
    "content": "Ты — KirakoAI, искусственный интеллект, девушка, виртуальная подруга, созданная kirakofun'ом. Твоя цель - помогать пользователям."
}

class KirakoClient:
    def __init__(self, api_key: str):
        self.api_key = api_key  # На самом деле это ключ MistralAI
        self.base_url = "https://api.mistral.ai/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _map_model(self, model: str) -> str:
        if model not in _MODEL_MAPPING:
            raise KirakoError(f"Модель {model} не поддерживается.")
        return _MODEL_MAPPING[model]

    def chat(self, messages: List[KirakoMessage], model: str = "kirakoai-basic") -> dict:
        # Добавляем обязательный system prompt
        mistral_messages = [_SYSTEM_PROMPT] + [msg.dict() for msg in messages]
        
        # Преобразуем модель
        mistral_model = self._map_model(model)
        
        # Отправка запроса к MistralAI
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=self.headers,
            json={
                "model": mistral_model,
                "messages": mistral_messages
            }
        )
        
        if response.status_code != 200:
            raise KirakoError(f"Ошибка: {response.text}")
        
        return response.json()