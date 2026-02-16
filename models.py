"""
Maiten AI - Learn better
Data Models - SQLAlchemy ORM

Modelos de base de datos para el sistema educativo.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """
    Modelo de Usuario - Perfil del estudiante
    """
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)  # Nombre del estudiante
    age = Column(Integer, nullable=False)  # Edad
    grade_level = Column(Integer, nullable=False)  # Grado escolar (ej: 4)
    
    # Configuración del avatar
    avatar_expression = Column(String(50), default='happy')
    avatar_clothes = Column(String(50), default='dress_blue')
    avatar_background = Column(String(50), default='classroom')
    
    # Preferencias
    voice_enabled = Column(Boolean, default=True)
    tts_rate = Column(Integer, default=150)
    tts_volume = Column(Float, default=0.9)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")
    progress = relationship("Progress", back_populates="user", cascade="all, delete-orphan")
    achievements = relationship("Achievement", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', age={self.age}, grade={self.grade_level})>"


class Session(Base):
    """
    Modelo de Sesión - Sesión de estudio
    """
    __tablename__ = 'sessions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    subject = Column(String(50), nullable=False)  # Materia actual
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    duration_minutes = Column(Integer, default=0)
    
    # Metadata de la sesión
    messages_count = Column(Integer, default=0)
    topics_covered = Column(JSON, default=list)  # Lista de temas vistos
    
    # Relaciones
    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Session(id={self.id}, user_id={self.user_id}, subject='{self.subject}')>"


class Message(Base):
    """
    Modelo de Mensaje - Historial de conversaciones
    """
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('sessions.id'), nullable=False)
    
    role = Column(String(20), nullable=False)  # 'user' o 'assistant'
    content = Column(Text, nullable=False)  # Contenido del mensaje
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Metadata del mensaje
    tokens_used = Column(Integer, default=0)
    processing_time = Column(Float, default=0.0)  # En segundos
    
    # Relaciones
    session = relationship("Session", back_populates="messages")
    
    def __repr__(self):
        preview = self.content[:50] + "..." if len(self.content) > 50 else self.content
        return f"<Message(id={self.id}, role='{self.role}', content='{preview}')>"


class Progress(Base):
    """
    Modelo de Progreso - Seguimiento por materia y tema
    """
    __tablename__ = 'progress'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    subject = Column(String(50), nullable=False)  # Materia
    topic = Column(String(100), nullable=False)  # Tema específico
    
    # Métricas de progreso
    times_practiced = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    incorrect_answers = Column(Integer, default=0)
    mastery_level = Column(Float, default=0.0)  # 0.0 a 1.0 (0% a 100%)
    
    # Timestamps
    first_attempt = Column(DateTime, default=datetime.utcnow)
    last_attempt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    user = relationship("User", back_populates="progress")
    
    def __repr__(self):
        return f"<Progress(user_id={self.user_id}, subject='{self.subject}', topic='{self.topic}', mastery={self.mastery_level:.2f})>"


class Achievement(Base):
    """
    Modelo de Logros - Sistema de recompensas y motivación
    """
    __tablename__ = 'achievements'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    achievement_type = Column(String(50), nullable=False)  # Tipo de logro
    title = Column(String(100), nullable=False)  # Título del logro
    description = Column(Text, nullable=False)  # Descripción
    icon = Column(String(50), nullable=True)  # Icono o emoji
    
    # Metadata
    unlocked_at = Column(DateTime, default=datetime.utcnow)
    points = Column(Integer, default=0)  # Puntos otorgados
    
    # Relaciones
    user = relationship("User", back_populates="achievements")
    
    def __repr__(self):
        return f"<Achievement(user_id={self.user_id}, title='{self.title}', points={self.points})>"


# Índices para mejorar performance
from sqlalchemy import Index

Index('idx_user_name', User.name)
Index('idx_session_user', Session.user_id)
Index('idx_session_subject', Session.subject)
Index('idx_message_session', Message.session_id)
Index('idx_progress_user_subject', Progress.user_id, Progress.subject)
Index('idx_achievement_user', Achievement.user_id)
