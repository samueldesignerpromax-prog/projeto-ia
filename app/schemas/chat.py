from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ChatRequest(BaseModel):
    user_id: str = Field(..., description="ID do usuário")
    message: str = Field(..., description="Mensagem do usuário")
    context: Optional[str] = Field(None, description="Contexto adicional")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "usuario_123",
                "message": "Olá, quem é você?",
                "context": "Conversa sobre IA"
            }
        }

class ChatResponse(BaseModel):
    user_id: str
    user_message: str
    assistant_response: str
    timestamp: datetime
    memory_saved: bool = True
    
    class Config:
        from_attributes = True

class MemoryResponse(BaseModel):
    id: int
    user_id: str
    user_message: str
    assistant_response: str
    created_at: datetime
    relevance_score: float
    
    class Config:
        from_attributes = True
