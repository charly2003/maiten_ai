"""
Maiten AI - Learn better
App Controller

Controlador principal que orquesta toda la aplicación.
"""

import logging
from typing import Optional, Dict, List

from ..ai.ai_agent import get_educational_agent
from ..data.database import get_db_manager
from .session_manager import get_session_manager
from .subject_manager import get_subject_manager

logger = logging.getLogger(__name__)


class AppController:
    """
    Controlador principal de Maiten AI
    Coordina la interacción entre UI, IA, Datos y Lógica
    """
    
    def __init__(self, user_id: int):
        """
        Inicializa el controlador de aplicación.
        
        Args:
            user_id: ID del usuario
        """
        self.user_id = user_id
        
        # Inicializar gestores
        self.db = get_db_manager()
        self.session_mgr = get_session_manager(user_id)
        self.subject_mgr = get_subject_manager(user_id)
        self.ai_agent = get_educational_agent()
        
        # Cargar información del usuario
        self.user = self.db.get_user(user_id)
        
        if not self.user:
            raise ValueError(f"User {user_id} not found")
        
        logger.info(f"App Controller initialized for {self.user.name}")
    
    def start_study_session(self, subject: str) -> Dict:
        """
        Inicia una nueva sesión de estudio.
        
        Args:
            subject: Materia a estudiar
            
        Returns:
            Dict: Información de la sesión iniciada
        """
        # Iniciar sesión
        session_id = self.session_mgr.start_session(subject)
        
        # Establecer materia actual
        self.subject_mgr.set_current_subject(subject)
        self.ai_agent.set_subject(subject)
        
        # Obtener información de la materia
        subject_info = self.subject_mgr.get_available_subjects()
        current_subject = next((s for s in subject_info if s['name'].lower() == subject.lower()), None)
        
        # Obtener temas recomendados
        recommended_topics = self.subject_mgr.get_recommended_topics(subject)
        
        logger.info(f"Study session started: {session_id} - {subject}")
        
        return {
            "session_id": session_id,
            "subject": subject,
            "subject_info": current_subject,
            "recommended_topics": recommended_topics,
            "greeting": f"¡Hola {self.user.name}! 😊 ¿Listo para aprender {subject}? ¡Vamos a aprender mejor!"
        }
    
    def end_study_session(self) -> Dict:
        """
        Finaliza la sesión de estudio actual.
        
        Returns:
            Dict: Resumen de la sesión
        """
        # Obtener resumen de IA
        summary = self.ai_agent.get_conversation_summary()
        
        # Obtener estadísticas
        stats = self.session_mgr.get_session_stats()
        
        # Finalizar sesión
        duration = self.session_mgr.end_session()
        
        # Limpiar historial del agente
        self.ai_agent.clear_history()
        
        logger.info(f"Study session ended. Duration: {duration} min")
        
        return {
            "duration_minutes": duration,
            "messages_count": stats.get("messages_count", 0),
            "total_tokens": stats.get("total_tokens", 0),
            "summary": summary,
            "farewell": f"¡Excelente trabajo, {self.user.name}! 🌟 Estudiaste {duration} minutos. ¡Sigue así!"
        }
    
    def send_message(self, message: str) -> Dict:
        """
        Procesa un mensaje del estudiante.
        
        Args:
            message: Mensaje del estudiante
            
        Returns:
            Dict: Respuesta del asistente
        """
        if not self.session_mgr.get_current_session_id():
            return {
                "response": "No hay una sesión activa. Por favor, inicia una sesión primero.",
                "error": "no_active_session"
            }
        
        # Obtener contexto de progreso
        current_subject = self.subject_mgr.current_subject
        current_topic = self.subject_mgr.current_topic
        
        context = {}
        if current_topic:
            # Obtener nivel de maestría del tema
            progress = self.db.get_user_progress(self.user_id, current_subject)
            topic_progress = next(
                (p for p in progress if p.topic == current_topic),
                None
            )
            if topic_progress:
                context['mastery_level'] = topic_progress.mastery_level
        
        # Procesar con el agente de IA
        ai_response = self.ai_agent.chat(message, context=context)
        
        # Guardar en sesión
        self.session_mgr.add_message(
            role="user",
            content=message
        )
        
        self.session_mgr.add_message(
            role="assistant",
            content=ai_response["response"],
            tokens_used=ai_response.get("tokens_used", 0),
            processing_time=ai_response.get("processing_time", 0.0)
        )
        
        return ai_response
    
    def get_explanation(self, concept: str) -> str:
        """
        Solicita una explicación de un concepto.
        
        Args:
            concept: Concepto a explicar
            
        Returns:
            str: Explicación
        """
        subject = self.subject_mgr.current_subject or "general"
        return self.ai_agent.explain_concept(concept, subject)
    
    def practice_topic(self, topic_id: str, difficulty: str = "medium") -> Dict:
        """
        Genera ejercicios de práctica para un tema.
        
        Args:
            topic_id: ID del tema
            difficulty: Nivel de dificultad
            
        Returns:
            Dict: Ejercicio generado
        """
        subject = self.subject_mgr.current_subject
        
        if not subject:
            return {"error": "No subject selected"}
        
        # Obtener información del tema
        topic = self.subject_mgr.get_topic_details(topic_id)
        
        if not topic:
            return {"error": "Topic not found"}
        
        # Establecer tema actual
        self.subject_mgr.set_current_subject(subject, topic.get('title'))
        
        # Generar ejercicio
        exercise = self.ai_agent.generate_exercise(
            subject=subject,
            topic=topic.get('title'),
            difficulty=difficulty
        )
        
        return exercise
    
    def check_answer(self, student_answer: str, correct_answer: str) -> Dict:
        """
        Verifica una respuesta y proporciona retroalimentación.
        
        Args:
            student_answer: Respuesta del estudiante
            correct_answer: Respuesta correcta
            
        Returns:
            Dict: Retroalimentación
        """
        # Normalizar respuestas para comparación
        is_correct = student_answer.strip().lower() == correct_answer.strip().lower()
        
        # Obtener retroalimentación del agente
        feedback = self.ai_agent.provide_feedback(
            student_answer=student_answer,
            correct_answer=correct_answer,
            is_correct=is_correct
        )
        
        # Actualizar progreso
        if self.subject_mgr.current_topic:
            mastery_delta = 0.1 if is_correct else -0.05
            self.subject_mgr.update_topic_progress(
                topic=self.subject_mgr.current_topic,
                correct=is_correct,
                mastery_delta=mastery_delta
            )
            
            # Verificar logros
            self._check_achievements(is_correct)
        
        return {
            "is_correct": is_correct,
            "feedback": feedback,
            "mastery_delta": 0.1 if is_correct else -0.05
        }
    
    def get_dashboard_data(self) -> Dict:
        """
        Obtiene datos para el dashboard del usuario.
        
        Returns:
            Dict: Datos del dashboard
        """
        # Información del usuario
        user_data = {
            "name": self.user.name,
            "age": self.user.age,
            "grade_level": self.user.grade_level
        }
        
        # Progreso general
        mastery_summary = self.subject_mgr.get_mastery_summary()
        
        # Sesiones recientes
        recent_sessions = self.session_mgr.get_recent_sessions(5)
        
        # Tiempo total de estudio
        total_study_time = self.session_mgr.get_total_study_time()
        
        # Logros
        achievements = self.db.get_user_achievements(self.user_id)
        total_points = self.db.get_total_points(self.user_id)
        
        return {
            "user": user_data,
            "mastery_summary": mastery_summary,
            "recent_sessions": recent_sessions,
            "total_study_time": total_study_time,
            "achievements_count": len(achievements),
            "total_points": total_points
        }
    
    def get_subjects_list(self) -> List[Dict]:
        """
        Obtiene la lista de materias disponibles con progreso.
        
        Returns:
            List[Dict]: Materias disponibles
        """
        return self.subject_mgr.get_available_subjects()
    
    def get_topic_list(self, subject: str) -> List[Dict]:
        """
        Obtiene la lista de temas de una materia.
        
        Args:
            subject: Nombre de la materia
            
        Returns:
            List[Dict]: Temas de la materia
        """
        return self.subject_mgr.get_subject_topics(subject)
    
    def search_content(self, query: str) -> List[Dict]:
        """
        Busca contenido en el curriculum.
        
        Args:
            query: Término de búsqueda
            
        Returns:
            List[Dict]: Resultados de búsqueda
        """
        return self.subject_mgr.search_topics(query)
    
    def update_avatar(self, expression: str = None, clothes: str = None, background: str = None):
        """
        Actualiza la apariencia del avatar.
        
        Args:
            expression: Expresión facial
            clothes: Ropa
            background: Fondo
        """
        self.db.update_user_avatar(
            user_id=self.user_id,
            expression=expression,
            clothes=clothes,
            background=background
        )
        
        # Recargar datos del usuario
        self.user = self.db.get_user(self.user_id)
        
        logger.info(f"Avatar updated for user {self.user_id}")
    
    def _check_achievements(self, is_correct: bool):
        """
        Verifica y desbloquea logros.
        
        Args:
            is_correct: Si la respuesta fue correcta
        """
        # Logro: Primera respuesta correcta
        if is_correct:
            progress = self.db.get_user_progress(self.user_id)
            correct_count = sum(p.correct_answers for p in progress)
            
            if correct_count == 1:
                self.db.unlock_achievement(
                    user_id=self.user_id,
                    achievement_type="first_correct",
                    title="¡Primera victoria!",
                    description="Respondiste correctamente por primera vez",
                    icon="🎯",
                    points=10
                )
        
        # Logro: 10 respuestas correctas
        progress = self.db.get_user_progress(self.user_id)
        total_correct = sum(p.correct_answers for p in progress)
        
        if total_correct == 10:
            self.db.unlock_achievement(
                user_id=self.user_id,
                achievement_type="ten_correct",
                title="¡Imparable!",
                description="10 respuestas correctas",
                icon="🌟",
                points=50
            )


# Singleton instances por usuario
_app_controllers: Dict[int, AppController] = {}


def get_app_controller(user_id: int) -> AppController:
    """
    Obtiene el controlador de aplicación para un usuario.
    
    Args:
        user_id: ID del usuario
        
    Returns:
        AppController: Instancia del controlador
    """
    global _app_controllers
    
    if user_id not in _app_controllers:
        _app_controllers[user_id] = AppController(user_id)
    
    return _app_controllers[user_id]
