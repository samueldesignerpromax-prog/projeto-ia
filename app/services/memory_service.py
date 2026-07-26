from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.memory import Memory
import logging

logger = logging.getLogger(__name__)

class MemoryService:
    def __init__(self, db: Session):
        self.db = db
    
    def save_memory(
        self, 
        user_id: str, 
        user_message: str, 
        assistant_response: str,
        context: Optional[str] = None
    ) -> Memory:
        try:
            memory = Memory(
                user_id=user_id,
                user_message=user_message,
                assistant_response=assistant_response,
                context=context
            )
            self.db.add(memory)
            self.db.commit()
            self.db.refresh(memory)
            logger.info(f"Memória salva para usuário {user_id} (ID: {memory.id})")
            return memory
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao salvar memória: {e}")
            raise
    
    def get_user_memories(self, user_id: str, limit: int = 10, offset: int = 0) -> List[Memory]:
        try:
            return self.db.query(Memory)\
                .filter(Memory.user_id == user_id)\
                .order_by(Memory.created_at.desc())\
                .offset(offset)\
                .limit(limit)\
                .all()
        except Exception as e:
            logger.error(f"Erro ao buscar memórias: {e}")
            return []
    
    def get_relevant_context(self, user_id: str, current_message: str) -> str:
        try:
            recent = self.get_user_memories(user_id, limit=5)
            if not recent:
                return ""
            parts = []
            for mem in reversed(recent):
                parts.append(f"Usuário disse: {mem.user_message}")
                parts.append(f"Jarvis respondeu: {mem.assistant_response}")
            return "\n".join(parts)
        except Exception as e:
            logger.error(f"Erro ao buscar contexto: {e}")
            return ""
