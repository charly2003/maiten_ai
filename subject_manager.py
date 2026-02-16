"""
Maiten AI - Learn better
Subject Manager

Gestiona contenido curricular y temas por materia.
"""

import logging
from typing import Optional, List, Dict

from ..data.content_loader import get_content_loader
from ..data.database import get_db_manager

logger = logging.getLogger(__name__)


class SubjectManager:
    """
    Gestor de materias y contenido curricular
    """
    
    def __init__(self, user_id: int):
        """
        Inicializa el gestor de materias.
        
        Args:
            user_id: ID del usuario
        """
        self.user_id = user_id
        self.content_loader = get_content_loader()
        self.db = get_db_manager()
        self.current_subject: Optional[str] = None
        self.current_topic: Optional[str] = None
        
        logger.info(f"Subject Manager initialized for user {user_id}")
    
    def get_available_subjects(self) -> List[Dict]:
        """
        Obtiene todas las materias disponibles.
        
        Returns:
            List[Dict]: Lista de materias con su información
        """
        subjects = self.content_loader.get_all_subjects()
        
        subjects_info = []
        for subject in subjects:
            info = self.content_loader.get_subject_info(subject)
            if info:
                # Agregar progreso del usuario
                progress = self.get_subject_progress(subject)
                info['progress'] = progress
                subjects_info.append(info)
        
        return subjects_info
    
    def set_current_subject(self, subject: str, topic: Optional[str] = None):
        """
        Establece la materia y tema actual.
        
        Args:
            subject: Nombre de la materia
            topic: ID del tema (opcional)
        """
        self.current_subject = subject
        self.current_topic = topic
        logger.info(f"Current subject set to: {subject}, topic: {topic}")
    
    def get_subject_topics(self, subject: Optional[str] = None) -> List[Dict]:
        """
        Obtiene los temas de una materia.
        
        Args:
            subject: Nombre de la materia (usa current_subject si no se especifica)
            
        Returns:
            List[Dict]: Lista de temas
        """
        subject = subject or self.current_subject
        
        if not subject:
            logger.warning("No subject specified")
            return []
        
        topics = self.content_loader.get_topics(subject)
        
        # Enriquecer con información de progreso
        for topic in topics:
            topic_id = topic.get('id')
            if topic_id:
                progress = self.db.get_user_progress(
                    user_id=self.user_id,
                    subject=subject
                )
                
                # Buscar progreso específico del tema
                topic_progress = next(
                    (p for p in progress if p.topic == topic.get('title')),
                    None
                )
                
                if topic_progress:
                    topic['mastery_level'] = topic_progress.mastery_level
                    topic['times_practiced'] = topic_progress.times_practiced
                else:
                    topic['mastery_level'] = 0.0
                    topic['times_practiced'] = 0
        
        return topics
    
    def get_topic_details(self, topic_id: str, subject: Optional[str] = None) -> Optional[Dict]:
        """
        Obtiene los detalles de un tema específico.
        
        Args:
            topic_id: ID del tema
            subject: Nombre de la materia
            
        Returns:
            Optional[Dict]: Información del tema
        """
        subject = subject or self.current_subject
        
        if not subject:
            return None
        
        return self.content_loader.get_topic_by_id(subject, topic_id)
    
    def get_topic_exercises(self, topic_id: str, subject: Optional[str] = None) -> List[Dict]:
        """
        Obtiene los ejercicios de un tema.
        
        Args:
            topic_id: ID del tema
            subject: Nombre de la materia
            
        Returns:
            List[Dict]: Lista de ejercicios
        """
        subject = subject or self.current_subject
        
        if not subject:
            return []
        
        return self.content_loader.get_exercises(subject, topic_id)
    
    def search_topics(self, query: str, subject: Optional[str] = None) -> List[Dict]:
        """
        Busca temas por palabras clave.
        
        Args:
            query: Término de búsqueda
            subject: Materia donde buscar (todas si no se especifica)
            
        Returns:
            List[Dict]: Temas que coinciden
        """
        if subject:
            subjects_to_search = [subject]
        else:
            subjects_to_search = self.content_loader.get_all_subjects()
        
        results = []
        for subj in subjects_to_search:
            matches = self.content_loader.search_content(subj, query)
            for match in matches:
                match['subject'] = subj
                results.append(match)
        
        return results
    
    def get_subject_progress(self, subject: str) -> Dict:
        """
        Obtiene el progreso general en una materia.
        
        Args:
            subject: Nombre de la materia
            
        Returns:
            Dict: Estadísticas de progreso
        """
        progress_records = self.db.get_user_progress(
            user_id=self.user_id,
            subject=subject
        )
        
        if not progress_records:
            return {
                "topics_studied": 0,
                "average_mastery": 0.0,
                "total_practice_time": 0
            }
        
        topics_studied = len(progress_records)
        average_mastery = sum(p.mastery_level for p in progress_records) / topics_studied
        total_practices = sum(p.times_practiced for p in progress_records)
        
        return {
            "topics_studied": topics_studied,
            "average_mastery": round(average_mastery, 2),
            "total_practices": total_practices,
            "topics_mastered": sum(1 for p in progress_records if p.mastery_level >= 0.8)
        }
    
    def update_topic_progress(
        self,
        topic: str,
        correct: Optional[bool] = None,
        mastery_delta: float = 0.0
    ):
        """
        Actualiza el progreso en un tema.
        
        Args:
            topic: Nombre del tema
            correct: Si la respuesta fue correcta
            mastery_delta: Cambio en nivel de maestría
        """
        if not self.current_subject:
            logger.warning("Cannot update progress: no current subject")
            return
        
        self.db.update_progress(
            user_id=self.user_id,
            subject=self.current_subject,
            topic=topic,
            correct=correct,
            mastery_delta=mastery_delta
        )
        
        logger.info(f"Progress updated for {self.current_subject} - {topic}")
    
    def get_recommended_topics(self, subject: Optional[str] = None) -> List[Dict]:
        """
        Recomienda temas según el progreso del usuario.
        
        Args:
            subject: Materia (usa current_subject si no se especifica)
            
        Returns:
            List[Dict]: Temas recomendados
        """
        subject = subject or self.current_subject
        
        if not subject:
            return []
        
        topics = self.get_subject_topics(subject)
        
        # Priorizar temas no estudiados o con baja maestría
        not_studied = [t for t in topics if t.get('mastery_level', 0) == 0]
        low_mastery = [t for t in topics if 0 < t.get('mastery_level', 0) < 0.5]
        
        recommendations = not_studied[:3] + low_mastery[:2]
        
        return recommendations[:5]
    
    def get_mastery_summary(self) -> Dict:
        """
        Obtiene un resumen del dominio del usuario en todas las materias.
        
        Returns:
            Dict: Resumen de maestría
        """
        subjects = self.content_loader.get_all_subjects()
        summary = {}
        
        for subject in subjects:
            progress = self.get_subject_progress(subject)
            summary[subject] = progress
        
        # Calcular promedio general
        if summary:
            total_mastery = sum(p['average_mastery'] for p in summary.values())
            overall_mastery = total_mastery / len(summary)
        else:
            overall_mastery = 0.0
        
        return {
            "subjects": summary,
            "overall_mastery": round(overall_mastery, 2)
        }
    
    def get_next_concept(self, topic_id: str) -> Optional[str]:
        """
        Obtiene el siguiente concepto a aprender en un tema.
        
        Args:
            topic_id: ID del tema
            
        Returns:
            Optional[str]: Descripción del siguiente concepto
        """
        if not self.current_subject:
            return None
        
        topic = self.get_topic_details(topic_id, self.current_subject)
        
        if not topic:
            return None
        
        concepts = topic.get('concepts', [])
        
        if not concepts:
            return None
        
        # Por ahora devuelve el primer concepto
        # En producción, esto debería ser más inteligente basado en progreso
        return concepts[0] if concepts else None


# Singleton instances por usuario
_subject_managers: Dict[int, SubjectManager] = {}


def get_subject_manager(user_id: int) -> SubjectManager:
    """
    Obtiene el gestor de materias para un usuario.
    
    Args:
        user_id: ID del usuario
        
    Returns:
        SubjectManager: Instancia del gestor
    """
    global _subject_managers
    
    if user_id not in _subject_managers:
        _subject_managers[user_id] = SubjectManager(user_id)
    
    return _subject_managers[user_id]
