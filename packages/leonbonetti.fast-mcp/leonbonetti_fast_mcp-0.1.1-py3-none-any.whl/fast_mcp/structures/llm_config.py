from pydantic import BaseModel
from typing import Optional

class OpenAIModelConfig(BaseModel):
    model: str
    base_url: str
    api_key: Optional[str] = None
    temperature: float = 0.0
    max_tokens: int = None
    timeout: Optional[int] = None
    max_retries: int = 2
    encoder_name: str = "gpt-4o"