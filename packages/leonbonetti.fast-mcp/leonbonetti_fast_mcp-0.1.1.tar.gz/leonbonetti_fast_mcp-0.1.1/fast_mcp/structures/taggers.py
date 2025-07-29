from pydantic import BaseModel, Field
from pydantic import create_model
from typing import List, Dict, Optional
from fast_mcp.structures.context import Requirement

def create_dynamic_output_model(requirements: Optional[List[Requirement]]):
    fields: Dict[str, tuple] = {}

    if requirements:
        for req in requirements:
            fields[req.id] = (Optional[str], None)

    fields['llm_response'] = (str, ...)
    
    return create_model("DynamicContextFillingOutput", **fields)

def create_dynamic_output_model_without_response(requirements: Optional[List[Requirement]]):
    fields: Dict[str, tuple] = {}

    if requirements:
        for req in requirements:
            fields[req.id] = (Optional[str], None)
    
    return create_model("DynamicContextFillingOutput", **fields)

class ContextClassification(BaseModel):
    context_id: str = Field(
        description="The context ID for the classifier."
    )

class ContextConfirmation(BaseModel):
    confirmed: bool = Field(
        description="a boolean (true if the user confirmed, false otherwise)."
    )
