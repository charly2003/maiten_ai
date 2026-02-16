"""
Maiten AI - Learn better
Database Manager

Gestor de conexión y operaciones de base de datos SQLite.
"""

import os
import logging
from pathlib import Path
from contextlib import contextmanager
from typing import Optional, List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from .models import Base, User, Session as SessionModel, Message, Progress, Achievement

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Gestor de base de datos SQLite para Maiten AI
    """
    
    def __init__(self, db_path: str = "data/user_profile.db"):
        """
        Inicializa el gestor de base de datos.
        
        Args:
            db_path: Ruta al archivo de base de datos SQLite
        """
        self.db_path = db_path
        self._engine = None
        self._session_factory = None
        
        # Crear directorio si no existe
        db_dir = Path(db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
        
        self._initialize_engine()
    
    def _initialize_engine(self):
        """Inicializa el motor de SQLAlchemy"""
        database_url = f"sqlite:///{self.db_path}"
        
        self._engine = create_engine(
            database_url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            echo=False  # Cambiar a True para debug SQL
        )
        
        self._session_factory = sessionmaker(
            bind=self._engine,
            autocommit=False,
            autoflush=False
        )
        
        logger.info(f"Database engine initialized: {database_url}")
    
    def create_tables(self):
        """Crea todas las tablas en la base de datos"""
        Base.metadata.create_all(bind=self._engine)
        logger.info("Database tables created successfully")
    
    def drop_tables(self):
        """Elimina todas las tablas (usar con precaución)"""
        Base.metadata.drop_all(bind=self._engine)
        logger.warning("All database tables dropped")
    
    @contextmanager
    def get_session(self) -> Session:
        """
        Context manager para obtener una sesión de base de datos.
        
        Usage:
            with db_manager.get_session() as session:
                user = session.query(User).first()
        """
        session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()
    
    # ==================== User Operations ====================
    
    def create_user(self, name: str, age: int, grade_level: int) -> User:
        """
        Crea un nuevo usuario.
        
        Args:
            name: Nombre del estudiante
            age: Edad
            grade_level: Grado escolar
            
        Returns:
            User: Usuario creado
        """
        with self.get_session() as session:
            user = User(name=name, age=age, grade_level=grade_level)
            session.add(user)
            session.flush()
            session.refresh(user)
            logger.info(f"User created: {user}")
            return user
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Obtiene un usuario por ID"""
        with self.get_session() as session:
            return session.query(User).filter(User.id == user_id).first()
    
    def get_user_by_name(self, name: str) -> Optional[User]:
        """Obtiene un usuario por nombre"""
        with self.get_session() as session:
            return session.query(User).filter(User.name == name).first()
    
    def get_all_users(self) -> List[User]:
        """Obtiene todos los usuarios"""
        with self.get_session() as session:
            return session.query(User).all()
    
    def update_user_avatar(self, user_id: int, expression: str = None, 
                          clothes: str = None, background: str = None):
        """Actualiza la configuración del avatar del usuario"""
        with self.get_session() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                if expression:
                    user.avatar_expression = expression
                if clothes:
                    user.avatar_clothes = clothes
                if background:
                    user.avatar_background = background
                logger.info(f"Avatar updated for user {user_id}")
    
    # ==================== Session Operations ====================
    
    def create_session(self, user_id: int, subject: str) -> SessionModel:
        """Crea una nueva sesión de estudio"""
        with self.get_session() as session:
            study_session = SessionModel(user_id=user_id, subject=subject)
            session.add(study_session)
            session.flush()
            session.refresh(study_session)
            logger.info(f"Session created: {study_session}")
            return study_session
    
    def end_session(self, session_id: int, duration_minutes: int):
        """Finaliza una sesión de estudio"""
        from datetime import datetime
        
        with self.get_session() as session:
            study_session = session.query(SessionModel).filter(
                SessionModel.id == session_id
            ).first()
            
            if study_session:
                study_session.ended_at = datetime.utcnow()
                study_session.duration_minutes = duration_minutes
                logger.info(f"Session {session_id} ended. Duration: {duration_minutes} min")
    
    def get_user_sessions(self, user_id: int, limit: int = 10) -> List[SessionModel]:
        """Obtiene las últimas sesiones de un usuario"""
        with self.get_session() as session:
            return session.query(SessionModel).filter(
                SessionModel.user_id == user_id
            ).order_by(SessionModel.started_at.desc()).limit(limit).all()
    
    # ==================== Message Operations ====================
    
    def add_message(self, session_id: int, role: str, content: str, 
                   tokens_used: int = 0, processing_time: float = 0.0) -> Message:
        """Agrega un mensaje al historial de conversación"""
        with self.get_session() as session:
            message = Message(
                session_id=session_id,
                role=role,
                content=content,
                tokens_used=tokens_used,
                processing_time=processing_time
            )
            session.add(message)
            
            # Actualizar contador de mensajes en la sesión
            study_session = session.query(SessionModel).filter(
                SessionModel.id == session_id
            ).first()
            if study_session:
                study_session.messages_count += 1
            
            session.flush()
            session.refresh(message)
            return message
    
    def get_session_messages(self, session_id: int) -> List[Message]:
        """Obtiene todos los mensajes de una sesión"""
        with self.get_session() as session:
            return session.query(Message).filter(
                Message.session_id == session_id
            ).order_by(Message.timestamp).all()
    
    # ==================== Progress Operations ====================
    
    def update_progress(self, user_id: int, subject: str, topic: str,
                       correct: bool = None, mastery_delta: float = 0.0):
        """Actualiza el progreso del usuario en un tema"""
        with self.get_session() as session:
            progress = session.query(Progress).filter(
                Progress.user_id == user_id,
                Progress.subject == subject,
                Progress.topic == topic
            ).first()
            
            if not progress:
                # Crear nuevo registro de progreso
                progress = Progress(
                    user_id=user_id,
                    subject=subject,
                    topic=topic
                )
                session.add(progress)
            
            # Actualizar métricas
            progress.times_practiced += 1
            
            if correct is not None:
                if correct:
                    progress.correct_answers += 1
                else:
                    progress.incorrect_answers += 1
            
            # Actualizar nivel de maestría (0.0 a 1.0)
            progress.mastery_level = min(1.0, max(0.0, progress.mastery_level + mastery_delta))
            
            logger.info(f"Progress updated: {progress}")
    
    def get_user_progress(self, user_id: int, subject: str = None) -> List[Progress]:
        """Obtiene el progreso del usuario"""
        with self.get_session() as session:
            query = session.query(Progress).filter(Progress.user_id == user_id)
            
            if subject:
                query = query.filter(Progress.subject == subject)
            
            return query.all()
    
    # ==================== Achievement Operations ====================
    
    def unlock_achievement(self, user_id: int, achievement_type: str,
                          title: str, description: str, 
                          icon: str = "🏆", points: int = 10) -> Achievement:
        """Desbloquea un logro para el usuario"""
        with self.get_session() as session:
            # Verificar que no esté ya desbloqueado
            existing = session.query(Achievement).filter(
                Achievement.user_id == user_id,
                Achievement.achievement_type == achievement_type
            ).first()
            
            if existing:
                logger.info(f"Achievement already unlocked: {achievement_type}")
                return existing
            
            achievement = Achievement(
                user_id=user_id,
                achievement_type=achievement_type,
                title=title,
                description=description,
                icon=icon,
                points=points
            )
            session.add(achievement)
            session.flush()
            session.refresh(achievement)
            
            logger.info(f"Achievement unlocked: {achievement}")
            return achievement
    
    def get_user_achievements(self, user_id: int) -> List[Achievement]:
        """Obtiene todos los logros del usuario"""
        with self.get_session() as session:
            return session.query(Achievement).filter(
                Achievement.user_id == user_id
            ).order_by(Achievement.unlocked_at.desc()).all()
    
    def get_total_points(self, user_id: int) -> int:
        """Obtiene el total de puntos del usuario"""
        with self.get_session() as session:
            achievements = session.query(Achievement).filter(
                Achievement.user_id == user_id
            ).all()
            return sum(a.points for a in achievements)


# Singleton instance
_db_manager: Optional[DatabaseManager] = None


def get_db_manager(db_path: str = "data/user_profile.db") -> DatabaseManager:
    """
    Obtiene la instancia singleton del DatabaseManager.
    
    Args:
        db_path: Ruta al archivo de base de datos
        
    Returns:
        DatabaseManager: Instancia del gestor de base de datos
    """
    global _db_manager
    
    if _db_manager is None:
        _db_manager = DatabaseManager(db_path)
        _db_manager.create_tables()
    
    return _db_manager
