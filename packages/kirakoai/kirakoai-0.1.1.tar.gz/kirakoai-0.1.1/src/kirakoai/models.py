from pydantic import BaseModel

class KirakoMessage(BaseModel):
    role: str  # "user", "assistant"
    content: str