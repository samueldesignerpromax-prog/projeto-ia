import google.generativeai as genai
from typing import Optional
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(
                settings.GEMINI_MODEL,
                generation_config={
                    "temperature": settings.TEMPERATURE,
                    "max_output_tokens": settings.MAX_TOKENS,
                }
            )
            logger.info(f"Gemini configurado com modelo: {settings.GEMINI_MODEL}")
        except Exception as e:
            logger.error(f"Erro ao configurar Gemini: {e}")
            raise
    
    def generate_response(self, user_message: str, context: Optional[str] = None) -> str:
        try:
            prompt = self._build_prompt(user_message, context)
            response = self.model.generate_content(prompt)
            
            if response.text:
                return response.text
            else:
                logger.warning("Resposta vazia do Gemini")
                return "Desculpe, não consegui gerar uma resposta."
                
        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {e}")
            return f"Ocorreu um erro ao processar sua mensagem: {str(e)}"
    
    def _build_prompt(self, user_message: str, context: Optional[str] = None) -> str:
        system_prompt = """
        Você é o Jarvis, um assistente de inteligência artificial.
        Você é útil, amigável e informativo.
        Responda de forma clara e concisa.
        """
        
        if context:
            system_prompt += f"\n\nContexto da conversa: {context}"
        
        prompt = f"{system_prompt}\n\nUsuário: {user_message}\n\nJarvis:"
        return prompt
