from pydantic import BaseModel
from typing import List, Optional, Callable, Any

class PossibleValue(BaseModel):
    id: str
    description: str

class Requirement(BaseModel):
    id: str
    description: str
    possible_values: Optional[List[PossibleValue]] = None
    
class Context(BaseModel):
    id: str
    description: str
    requirements: Optional[List[Requirement]] = None
    executor: Optional[Callable[[], Any]] = None
    require_confirmation: Optional[bool] = False