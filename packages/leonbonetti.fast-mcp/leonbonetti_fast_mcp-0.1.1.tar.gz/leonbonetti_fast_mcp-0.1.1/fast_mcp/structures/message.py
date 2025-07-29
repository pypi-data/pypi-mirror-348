from typing import Literal, Optional
from datetime import datetime
import uuid
from pydantic import BaseModel

class Message(BaseModel):
    content: str
    role: Literal['user', 'assistant']
    context_id: Optional[str] = None
    message_id: str = uuid.uuid4().hex
    created_at: datetime = datetime.now()
    previous_message_id: Optional[str] = None
    chat_id: Optional[str] = None
