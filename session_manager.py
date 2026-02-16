"""
Maiten AI - Learn better
Session Manager

Gestiona sesiones de estudio y contexto de conversación.
"""

import logging
from datetime import datetime
from typing import Optional, List, Dict

from ..data.database import get_db_manager
from ..data.models import Session, Message

logger = logging.getLogger(__name__)


class SessionManager:
    """
    Gestor de sesiones de estudio
    """
    
    def __init__(self, user_id: int):
        """
        Inicializa el gestor de sesiones.
        
        Args:
            user_id: ID del usuario
        """
        self.user_id = user_id
        self.db = get_db_manager()
        self.current_session: Optional[Session] = None
        self.session_start_time: Optional[datetime] = None
        
        logger.info(f"Session Manager initialized for user {user_id}")
    
    def start_session(self, subject: str) -> int:
        """
        Inicia una nueva sesión de estudio.
        
        Args:
            subject: Materia de estudio
            
        Returns:
            int: ID de la sesión creada
        """
        # Finalizar sesión anterior si existe
        if self.current_session:
            self.end_session()
        
        # Crear nueva sesión
        self.current_session = self.db.create_session(
            user_id=self.user_id,
            subject=subject
        )
        self.session_start_time = datetime.utcnow()
        
        logger.info(f"Session started: {self.current_session.id} - Subject: {subject}")
        
        return self.current_session.id
    
    def end_session(self) -> Optional[int]:
        """
        Finaliza la sesión actual.
        
        Returns:
            Optional[int]: Duración en minutos o None si no había sesión
        """
        if not self.current_session:
            logger.warning("No active session to end")
            return None
        
        # Calcular duración
        if self.session_start_time:
            duration = datetime.utcnow() - self.session_start_time
            duration_minutes = int(duration.total_seconds() / 60)
        else:
            duration_minutes = 0
        
        # Actualizar en base de datos
        self.db.end_session(
            session_id=self.current_session.id,
            duration_minutes=duration_minutes
        )
        
        logger.info(f"Session ended: {self.current_session.id} - Duration: {duration_minutes} min")
        
        session_id = self.current_session.id
        self.current_session = None
        self.session_start_time = None
        
        return duration_minutes
    
    def get_current_session_id(self) -> Optional[int]:
        """
        Obtiene el ID de la sesión actual.
        
        Returns:
            Optional[int]: ID de sesión o None
        """
        return self.current_session.id if self.current_session else None
    
    def add_message(
        self,
        role: str,
        content: str,
        tokens_used: int = 0,
        processing_time: float = 0.0
    ) -> Optional[Message]:
        """
        Agrega un mensaje a la sesión actual.
        
        Args:
            role: 'user' o 'assistant'
            content: Contenido del mensaje
            tokens_used: Tokens consumidos
            processing_time: Tiempo de procesamiento
            
        Returns:
            Optional[Message]: Mensaje creado o None si no hay sesión
        """
        if not self.current_session:
            logger.warning("Cannot add message: no active session")
            return None
        
        message = self.db.add_message(
            session_id=self.current_session.id,
            role=role,
            content=content,
            tokens_used=tokens_used,
            processing_time=processing_time
        )
        
        logger.debug(f"Message added to session {self.current_session.id}: {role}")
        
        return message
    
    def get_session_history(self, limit: int = 10) -> List[Dict]:
        """
        Obtiene el historial de mensajes de la sesión actual.
        
        Args:
            limit: Número máximo de mensajes
            
        Returns:
            List[Dict]: Lista de mensajes en formato dict
        """
        if not self.current_session:
            return []
        
        messages = self.db.get_session_messages(self.current_session.id)
        
        # Limitar y convertir a formato simple
        recent_messages = messages[-limit:] if len(messages) > limit else messages
        
        return [
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp
            }
            for msg in recent_messages
        ]
    
    def get_conversation_context(self, max_messages: int = 10) -> List[Dict[str, str]]:
        """
        Obtiene el contexto de conversación para la IA.
        
        Args:
            max_messages: Máximo de mensajes a incluir
            
        Returns:
            List[Dict]: Mensajes en formato [{role: str, content: str}]
        """
        if not self.current_session:
            return []
        
        messages = self.db.get_session_messages(self.current_session.id)
        recent = messages[-max_messages:] if len(messages) > max_messages else messages
        
        return [
            {"role": msg.role, "content": msg.content}
            for msg in recent
        ]
    
    def get_session_stats(self) -> Dict:
        """
        Obtiene estadísticas de la sesión actual.
        
        Returns:
            Dict: Estadísticas de la sesión
        """
        if not self.current_session:
            return {
                "active": False,
                "session_id": None
            }
        
        messages = self.db.get_session_messages(self.current_session.id)
        
        # Calcular tiempo transcurrido
        if self.session_start_time:
            elapsed = datetime.utcnow() - self.session_start_time
            elapsed_minutes = int(elapsed.total_seconds() / 60)
        else:
            elapsed_minutes = 0
        
        # Calcular tokens totales
        total_tokens = sum(msg.tokens_used for msg in messages)
        
        return {
            "active": True,
            "session_id": self.current_session.id,
            "subject": self.current_session.subject,
            "messages_count": len(messages),
            "elapsed_minutes": elapsed_minutes,
            "total_tokens": total_tokens,
            "started_at": self.session_start_time
        }
    
    def get_recent_sessions(self, limit: int = 5) -> List[Dict]:
        """
        Obtiene las sesiones recientes del usuario.
        
        Args:
            limit: Número de sesiones a obtener
            
        Returns:
            List[Dict]: Lista de sesiones recientes
        """
        sessions = self.db.get_user_sessions(self.user_id, limit)
        
        return [
            {
                "session_id": s.id,
                "subject": s.subject,
                "started_at": s.started_at,
                "ended_at": s.ended_at,
                "duration_minutes": s.duration_minutes,
                "messages_count": s.messages_count
            }
            for s in sessions
        ]
    
    def switch_subject(self, new_subject: str) -> int:
        """
        Cambia a una nueva materia (finaliza sesión actual y crea nueva).
        
        Args:
            new_subject: Nueva materia
            
        Returns:
            int: ID de la nueva sesión
        """
        logger.info(f"Switching subject to: {new_subject}")
        return self.start_session(new_subject)
    
    def get_total_study_time(self) -> int:
        """
        Obtiene el tiempo total de estudio del usuario.
        
        Returns:
            int: Minutos totales de estudio
        """
        sessions = self.db.get_user_sessions(self.user_id, limit=100)
        
        total_minutes = sum(
            s.duration_minutes for s in sessions 
            if s.duration_minutes is not None
        )
        
        return total_minutes


# Singleton instances por usuario
_session_managers: Dict[int, SessionManager] = {}


def get_session_manager(user_id: int) -> SessionManager:
    """
    Obtiene el gestor de sesiones para un usuario.
    
    Args:
        user_id: ID del usuario
        
    Returns:
        SessionManager: Instancia del gestor
    """
    global _session_managers
    
    if user_id not in _session_managers:
        _session_managers[user_id] = SessionManager(user_id)
    
    return _session_managers[user_id]
