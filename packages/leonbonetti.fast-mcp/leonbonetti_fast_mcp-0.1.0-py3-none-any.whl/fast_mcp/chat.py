from typing import List, Dict, Any, Optional, Literal
from datetime import datetime
from fast_mcp.ai.tokenizer import estimate_tokens
from fast_mcp.structures.message import Message
import uuid
from pydantic import BaseModel
from fast_mcp.structures.context import Context
from fast_mcp.structures.llm_config import OpenAIModelConfig
from fast_mcp.ai.provider import create_model
from fast_mcp.structures.taggers import ContextClassification
from fast_mcp.constants.classifiers import CONTEXT_CLASSIFIER_TEMPLATE

class ChatMemory(BaseModel):
    context_id: str = None
    fields: Dict[str, Any] = {}

class Chat:
    def __init__(self, model_config: OpenAIModelConfig, contexts: List[Context] = [], chat_id: str = None, created_at: datetime = None):
        self.chat_id =  chat_id if chat_id else uuid.uuid4().hex
        self.created_at = created_at if created_at else datetime.now() 
        self.messages: List[Message] = []
        self.memory: ChatMemory = ChatMemory()
        self.available_contexts = contexts
        self.model_config = model_config
        
    def update_message_context(self, message_id: str, context_id: str = None):
        for message in self.messages:
            if message.message_id == message_id:
                message.context_id = context_id
                return message
        raise ValueError(f"Message with id {message_id} not found.")

    def add_message(self, content: str, role: Literal['user', 'assistant'], context_id: Optional[str] = None, previous_message_id: Optional[str] = None):
        previous_message_id = self.messages[-1].message_id if len(self.messages) > 0 else None
        message = Message(
            content=content,
            role=role,
            context_id=context_id,
            previous_message_id=previous_message_id,
            chat_id=self.chat_id
        )
        self.messages.append(message)
        if message.role == "user":
            conversation_context = self.classify_context()
            if conversation_context != "":
                message = self.update_message_context(message.message_id, conversation_context)
                self.memory.context_id = conversation_context
            else:
                self.memory.context_id = None
        return message

    def classify_context(self):
        model = create_model(self.model_config).with_structured_output(ContextClassification)
        context_header = "\n".join(f"- {ctx.id}: {ctx.description}" for ctx in self.available_contexts)
        overhead_messages = CONTEXT_CLASSIFIER_TEMPLATE.format_messages(
            input="", context_options=context_header
        )
        overhead_text = "\n".join(m.content for m in overhead_messages)
        conversation_str = self.format_and_truncate_conversation(overhead_text)

        formatted_prompt = CONTEXT_CLASSIFIER_TEMPLATE.format_messages(
            input=conversation_str,
            context_options=context_header
        )
        result = model.invoke(formatted_prompt)
        return result.context_id
    
    def format_and_truncate_conversation(self, overhead_text: str):
        formatted_messages = [f"{msg.role.capitalize()}: {msg.content}" for msg in self.messages]
        overhead_token_count = estimate_tokens(self.model_config, overhead_text)
        truncated_msgs = []
        total_tokens = overhead_token_count
        for msg in reversed(formatted_messages):
            msg_tokens = estimate_tokens(self.model_config, msg)
            if total_tokens + msg_tokens <= self.model_config.max_tokens if self.model_config else 164000:
                truncated_msgs.insert(0, msg)
                total_tokens += msg_tokens
            else:
                break
        conversation_str = "\n".join(truncated_msgs)
        return conversation_str
    
    def clean_context_memory(self, context_id):
        self.memory.context_id = None
        del self.memory.fields[context_id]