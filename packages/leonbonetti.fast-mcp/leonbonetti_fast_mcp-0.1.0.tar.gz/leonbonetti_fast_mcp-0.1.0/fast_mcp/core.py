from fast_mcp.structures.llm_config import OpenAIModelConfig
from fast_mcp.chat import Chat
from fast_mcp.structures.context import Context
from fast_mcp.utils import load_context_from_folder
from typing import List
from fast_mcp.ai.inference import generate_post_execution_message, no_context_inference, empty_context_inference, full_extractor_inference, ask_for_missing_fields, generate_confirmation_message, check_context_confirmation

class FastMCP:
    def __init__(self,
                # Configuration parameters 
                model: str,
                base_url: str,
                api_key: str,
                max_tokens: int,
                temperature: float = 0.0,
                timeout: int = None,
                max_retries: int = 2,
                encoder_name: str = "gpt-4o",
                # Chat Paramaters
                chat: Chat = None,
                # Context Parameters
                context_folder_path: str = None,
                contexts: List[Context] = None,
                max_requires_per_ask: int = 3
            ):
        self.max_requires_per_ask = max_requires_per_ask
        self.model_config = OpenAIModelConfig(
            model=model,
            base_url=base_url,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout,
            max_retries=max_retries,
            encoder_name=encoder_name,
        )
        
        self.contexts = contexts if contexts else []
        if context_folder_path:
            self.contexts.extend(load_context_from_folder(context_folder_path))
        
        if chat:
            self.chat = chat
            self.chat.model_config = self.model_config
            self.chat.available_contexts = self.contexts
        else:
            self.chat = Chat(model_config=self.model_config, contexts=self.contexts)
    
    def find_context(self, context_id: str) -> Context:
        """Find a context by its ID."""
        for context in self.contexts:
            if context.id == context_id:
                return context
        return None
    
    def add_user_message(self, message: str):
        """Add a user message to the chat history."""
        message = self.chat.add_message(message, role="user")
        context_id = self.chat.memory.context_id

        if not context_id:
            response = no_context_inference(self.model_config, self.chat)
            return self.chat.add_message(response, role="assistant", context_id=context_id)

        context = self.find_context(context_id)
        if not context:
            raise ValueError(f"Context with ID {context_id} not found.")

        # Case: No requirements
        if not context.requirements:
            if not context.executor:
                response = empty_context_inference(self.model_config, self.chat, context)
                return self.chat.add_message(response, role="assistant", context_id=context_id)

        # Initialize field memory if necessary
        if context_id not in self.chat.memory.fields:
            self.chat.memory.fields[context_id] = {}

        filled_fields = self.chat.memory.fields[context_id]
        filled_keys = list(filled_fields.keys())
        missing_requirements = [
            req for req in context.requirements if req.id not in filled_keys
        ]

        # Try to extract missing fields from current conversation
        if missing_requirements:
            extracted = full_extractor_inference(self.model_config, self.chat, context)
            for k, v in extracted:
                if v is not None:
                    for req in context.requirements:
                        if req.id == k:
                            filled_fields[k] = v
                            break

            # Recalculate missing after extraction
            missing_requirements = [
                req for req in context.requirements if req.id not in filled_fields
            ]

            if missing_requirements:
                response = ask_for_missing_fields(
                    self.model_config, self.chat, missing_requirements[:self.max_requires_per_ask]
                )
                return self.chat.add_message(response, role="assistant", context_id=context_id)
            else:
                 if context.require_confirmation:
                    response = generate_confirmation_message(self.model_config, self.chat, context)
                    return self.chat.add_message(response, role="assistant", context_id=context_id)

        # If all requirements are now filled
        if context.require_confirmation:
            confirmed = check_context_confirmation(self.model_config, self.chat)
            if not confirmed:
                # Force another pass by simulating a missing requirement
                response = generate_confirmation_message(self.model_config, self.chat, context)
                return self.chat.add_message(response, role="assistant", context_id=context_id)

        if context.executor:
            result = context.executor(**filled_fields)
            response = generate_post_execution_message(self.model_config, self.chat, context, result)
        else:
            response = empty_context_inference(self.model_config, self.chat, context)

        self.chat.clean_context_memory(context_id)
        return self.chat.add_message(response, role="assistant", context_id=context_id)