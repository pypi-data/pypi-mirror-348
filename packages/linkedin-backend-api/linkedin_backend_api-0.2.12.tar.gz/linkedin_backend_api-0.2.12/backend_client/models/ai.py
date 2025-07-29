from typing import Dict, Optional, Any
from pydantic import BaseModel

class UsageMetadata(BaseModel):
    candidatesTokensDetails: int
    promptTokensDetails: int

class PromptInput(BaseModel):
    prompt: str

class OutputJson(BaseModel):
    text: Optional[Dict[str, Any]] = None
    usageMetadata: Optional[UsageMetadata] = None

class RelevanceInput(BaseModel):
    user_requirements: str
    vacancy_text: str
    additional_info: str = ""
class RelevanceOutput(BaseModel):
    score: int
    usageMetadata: Optional[UsageMetadata] = None 