from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import logging

from app.schemas.chat import ChatRequest, ChatResponse, MemoryResponse
from app.services.gemini_service import GeminiService
from app.services.memory_service import MemoryService
from app.database.connection import get_db
from app.models.memory import Memory

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/chat", tags=["chat"])

gemini_service = GeminiService()

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        logger.info(f"Recebida mensagem de {request.user_id}: {request.message[:50]}...")
        
        memory_service = MemoryService(db)
        context = memory_service.get_relevant_context(request.user_id, request.message)
        
        full_context = request.context or ""
        if context:
            full_context = f"{full_context}\n\nHistórico da conversa:\n{context}"
        
        assistant_response = gemini_service.generate_response(request.message, full_context)
        
        memory_service.save_memory(
            user_id=request.user_id,
            user_message=request.message,
            assistant_response=assistant_response,
            context=request.context
        )
        
        last_memory = db.query(Memory)\
            .filter(Memory.user_id == request.user_id)\
            .order_by(Memory.created_at.desc())\
            .first()
        
        return ChatResponse(
            user_id=request.user_id,
            user_message=request.message,
            assistant_response=assistant_response,
            timestamp=last_memory.created_at if last_memory else None,
            memory_saved=True
        )
        
    except Exception as e:
        logger.error(f"Erro no chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/memories/{user_id}", response_model=List[MemoryResponse])
async def get_user_memories(
    user_id: str,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    try:
        memory_service = MemoryService(db)
        return memory_service.get_user_memories(user_id, limit, offset)
    except Exception as e:
        logger.error(f"Erro ao buscar memórias: {e}")
        raise HTTPException(status_code=500, detail=str(e))
