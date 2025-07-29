import tiktoken
from fast_mcp.structures.llm_config import OpenAIModelConfig

def estimate_tokens(model_config: OpenAIModelConfig,  text: str) -> int:
    if model_config is not None or not model_config.encoder_name:
        encoding = tiktoken.encoding_for_model(model_config.encoder_name)
    else:
        encoding = tiktoken.encoding_for_model("gpt-4o")
    return len(encoding.encode(text))