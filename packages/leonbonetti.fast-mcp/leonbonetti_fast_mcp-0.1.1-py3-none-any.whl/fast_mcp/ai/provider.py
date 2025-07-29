from langchain_openai import ChatOpenAI
from fast_mcp.structures.llm_config import OpenAIModelConfig

def create_model(config: OpenAIModelConfig) -> ChatOpenAI:
    
    return ChatOpenAI(
        base_url=config.base_url,
        model=config.model,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        timeout=config.timeout,
        max_retries=config.max_retries,
        api_key=config.api_key,
    )