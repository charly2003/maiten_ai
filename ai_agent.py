"""
Maiten AI - Learn better
AI Agent

Agente educativo principal que coordina la IA con el estudiante.
"""

import logging
import time
from typing import List, Dict, Optional

from ..services.api_client import get_api_client
from .prompt_engine import get_prompt_engine
from .content_adapter import ContentAdapter
from .safety_filter import SafetyFilter

logger = logging.getLogger(__name__)


class EducationalAgent:
    """
    Agente educativo inteligente basado en Claude API
    """
    
    def __init__(
        self,
        student_name: str = "Maitena",
        student_age: int = 9,
        grade_level: int = 4
    ):
        """
        Inicializa el agente educativo.
        
        Args:
            student_name: Nombre del estudiante
            student_age: Edad del estudiante
            grade_level: Grado escolar
        """
        self.student_name = student_name
        self.student_age = student_age
        self.grade_level = grade_level
        
        # Inicializar componentes
        self.api_client = get_api_client()
        self.prompt_engine = get_prompt_engine(student_name, student_age, grade_level)
        self.content_adapter = ContentAdapter(student_age, grade_level)
        self.safety_filter = SafetyFilter()
        
        # Estado de conversación
        self.conversation_history: List[Dict[str, str]] = []
        self.current_subject: Optional[str] = None
        self.current_topic: Optional[str] = None
        
        logger.info(f"Educational Agent initialized for {student_name}")
    
    def set_subject(self, subject: str, topic: Optional[str] = None):
        """
        Establece la materia y tema actual.
        
        Args:
            subject: Nombre de la materia
            topic: Tema específico (opcional)
        """
        self.current_subject = subject
        self.current_topic = topic
        logger.info(f"Subject set to: {subject}, Topic: {topic}")
    
    def add_to_history(self, role: str, content: str):
        """
        Agrega un mensaje al historial de conversación.
        
        Args:
            role: 'user' o 'assistant'
            content: Contenido del mensaje
        """
        self.conversation_history.append({
            "role": role,
            "content": content
        })
        
        # Limitar historial a últimos 10 mensajes para no exceder límites
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
    
    def clear_history(self):
        """Limpia el historial de conversación"""
        self.conversation_history = []
        logger.info("Conversation history cleared")
    
    def chat(
        self,
        user_message: str,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Procesa un mensaje del estudiante y genera una respuesta.
        
        Args:
            user_message: Mensaje del estudiante
            context: Contexto adicional (progreso, etc.)
            
        Returns:
            Dict con la respuesta y metadata
        """
        start_time = time.time()
        
        try:
            # 1. Filtro de seguridad en el input
            if not self.safety_filter.is_safe_input(user_message):
                logger.warning(f"Unsafe input detected: {user_message[:50]}...")
                return {
                    "response": "Hmm, esa pregunta no está relacionada con lo que estamos estudiando. ¿Tienes alguna pregunta sobre el tema? 😊",
                    "is_safe": False,
                    "tokens_used": 0,
                    "processing_time": time.time() - start_time
                }
            
            # 2. Agregar mensaje del usuario al historial
            self.add_to_history("user", user_message)
            
            # 3. Crear system prompt
            system_prompt = self.prompt_engine.create_teaching_prompt(
                subject=self.current_subject or "general",
                topic=self.current_topic,
                student_question=user_message,
                context=context
            )
            
            # 4. Llamar a Claude API
            response = self.api_client.create_message(
                messages=self.conversation_history,
                system_prompt=system_prompt
            )
            
            assistant_message = response["content"]
            
            # 5. Adaptar contenido para la edad
            adapted_message = self.content_adapter.adapt_response(assistant_message)
            
            # 6. Filtro de seguridad en el output
            if not self.safety_filter.is_safe_output(adapted_message):
                logger.warning("Unsafe output detected from AI")
                adapted_message = "Lo siento, tuve un problema generando la respuesta. ¿Podrías reformular tu pregunta? 😊"
            
            # 7. Agregar respuesta al historial
            self.add_to_history("assistant", adapted_message)
            
            processing_time = time.time() - start_time
            
            logger.info(f"Chat response generated in {processing_time:.2f}s, tokens: {response['usage']['input_tokens'] + response['usage']['output_tokens']}")
            
            return {
                "response": adapted_message,
                "is_safe": True,
                "tokens_used": response["usage"]["input_tokens"] + response["usage"]["output_tokens"],
                "processing_time": processing_time,
                "model": response["model"]
            }
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return {
                "response": "¡Ups! Tuve un pequeño problema. ¿Podrías intentar de nuevo? 😊",
                "is_safe": True,
                "tokens_used": 0,
                "processing_time": time.time() - start_time,
                "error": str(e)
            }
    
    def explain_concept(self, concept: str, subject: str) -> str:
        """
        Explica un concepto específico.
        
        Args:
            concept: Concepto a explicar
            subject: Materia
            
        Returns:
            str: Explicación adaptada
        """
        system_prompt = self.prompt_engine.create_explanation_prompt(concept, subject)
        
        try:
            response = self.api_client.create_message(
                messages=[{
                    "role": "user",
                    "content": f"Explícame: {concept}"
                }],
                system_prompt=system_prompt
            )
            
            explanation = self.content_adapter.adapt_response(response["content"])
            
            return explanation
            
        except Exception as e:
            logger.error(f"Error explaining concept: {e}")
            return f"Lo siento, tuve un problema explicando {concept}. ¿Podrías ser más específico? 😊"
    
    def generate_exercise(
        self,
        subject: str,
        topic: str,
        difficulty: str = "medium"
    ) -> Dict:
        """
        Genera un ejercicio de práctica.
        
        Args:
            subject: Materia
            topic: Tema
            difficulty: Nivel de dificultad
            
        Returns:
            Dict con el ejercicio
        """
        system_prompt = self.prompt_engine.create_exercise_prompt(
            subject=subject,
            topic=topic,
            difficulty=difficulty
        )
        
        try:
            response = self.api_client.create_message(
                messages=[{
                    "role": "user",
                    "content": "Genera un ejercicio de práctica"
                }],
                system_prompt=system_prompt
            )
            
            exercise_text = response["content"]
            
            return {
                "exercise": exercise_text,
                "subject": subject,
                "topic": topic,
                "difficulty": difficulty
            }
            
        except Exception as e:
            logger.error(f"Error generating exercise: {e}")
            return {
                "exercise": "No pude generar un ejercicio en este momento. ¿Quieres intentar con otro tema?",
                "error": str(e)
            }
    
    def provide_feedback(
        self,
        student_answer: str,
        correct_answer: str,
        is_correct: bool
    ) -> str:
        """
        Proporciona retroalimentación sobre una respuesta.
        
        Args:
            student_answer: Respuesta del estudiante
            correct_answer: Respuesta correcta
            is_correct: Si la respuesta es correcta
            
        Returns:
            str: Mensaje de retroalimentación
        """
        if is_correct:
            situation = "correct_answer"
        else:
            situation = "wrong_answer"
        
        system_prompt = self.prompt_engine.create_encouragement_prompt(situation)
        
        message = f"""Respuesta del estudiante: {student_answer}
Respuesta correcta: {correct_answer}
¿Es correcta? {'Sí' if is_correct else 'No'}"""
        
        try:
            response = self.api_client.create_message(
                messages=[{"role": "user", "content": message}],
                system_prompt=system_prompt
            )
            
            return response["content"]
            
        except Exception as e:
            logger.error(f"Error providing feedback: {e}")
            
            if is_correct:
                return "¡Excelente trabajo! 🎉"
            else:
                return f"No exactamente. La respuesta correcta es: {correct_answer}. ¡Sigue intentando! 💪"
    
    def get_conversation_summary(self) -> str:
        """
        Genera un resumen de la conversación actual.
        
        Returns:
            str: Resumen de lo aprendido
        """
        if not self.conversation_history:
            return "Aún no hemos conversado sobre ningún tema."
        
        system_prompt = f"""Resume brevemente lo que {self.student_name} aprendió en esta conversación.

Incluye:
- Tema(s) principal(es) discutidos
- Conceptos clave comprendidos
- Áreas que necesitan más práctica (si las hay)

Mantén el resumen en 3-4 frases máximo. Usa un tono positivo y motivador."""
        
        try:
            # Crear una versión condensada del historial
            summary_messages = [
                {"role": "user", "content": "Resume lo que aprendimos en esta sesión"}
            ]
            
            response = self.api_client.create_message(
                messages=summary_messages,
                system_prompt=system_prompt
            )
            
            return response["content"]
            
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return "Tuvimos una gran sesión de estudio. ¡Sigue así! 📚"


# Singleton instance
_educational_agent: Optional[EducationalAgent] = None


def get_educational_agent(
    student_name: str = "Maitena",
    student_age: int = 9,
    grade_level: int = 4
) -> EducationalAgent:
    """
    Obtiene la instancia singleton del EducationalAgent.
    
    Returns:
        EducationalAgent: Instancia del agente
    """
    global _educational_agent
    
    if _educational_agent is None:
        _educational_agent = EducationalAgent(student_name, student_age, grade_level)
    
    return _educational_agent
