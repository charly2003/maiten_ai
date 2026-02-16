"""
Maiten AI - Learn better
Content Loader

Carga y gestiona el contenido curricular desde archivos JSON.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class ContentLoader:
    """
    Cargador de contenido curricular educativo
    """
    
    def __init__(self, curriculum_dir: str = "data/curriculum"):
        """
        Inicializa el cargador de contenido.
        
        Args:
            curriculum_dir: Directorio que contiene los archivos JSON de curriculum
        """
        self.curriculum_dir = Path(curriculum_dir)
        self._content_cache: Dict[str, dict] = {}
        
        # Crear directorio si no existe
        self.curriculum_dir.mkdir(parents=True, exist_ok=True)
    
    def load_subject(self, subject: str) -> Optional[dict]:
        """
        Carga el contenido de una materia específica.
        
        Args:
            subject: Nombre de la materia (matematicas, lengua, ciencias, etc.)
            
        Returns:
            dict: Contenido de la materia o None si no existe
        """
        # Verificar cache
        if subject in self._content_cache:
            return self._content_cache[subject]
        
        # Cargar desde archivo
        file_path = self.curriculum_dir / f"{subject}.json"
        
        if not file_path.exists():
            logger.warning(f"Curriculum file not found: {file_path}")
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = json.load(f)
                self._content_cache[subject] = content
                logger.info(f"Loaded curriculum for: {subject}")
                return content
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON for {subject}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error loading curriculum for {subject}: {e}")
            return None
    
    def get_topics(self, subject: str) -> List[dict]:
        """
        Obtiene la lista de temas de una materia.
        
        Args:
            subject: Nombre de la materia
            
        Returns:
            List[dict]: Lista de temas con sus detalles
        """
        content = self.load_subject(subject)
        
        if not content:
            return []
        
        return content.get('topics', [])
    
    def get_topic_by_id(self, subject: str, topic_id: str) -> Optional[dict]:
        """
        Obtiene un tema específico por su ID.
        
        Args:
            subject: Nombre de la materia
            topic_id: ID del tema
            
        Returns:
            dict: Información del tema o None si no existe
        """
        topics = self.get_topics(subject)
        
        for topic in topics:
            if topic.get('id') == topic_id:
                return topic
        
        return None
    
    def get_exercises(self, subject: str, topic_id: str) -> List[dict]:
        """
        Obtiene los ejercicios de un tema específico.
        
        Args:
            subject: Nombre de la materia
            topic_id: ID del tema
            
        Returns:
            List[dict]: Lista de ejercicios
        """
        topic = self.get_topic_by_id(subject, topic_id)
        
        if not topic:
            return []
        
        return topic.get('exercises', [])
    
    def get_subject_info(self, subject: str) -> Optional[dict]:
        """
        Obtiene la información general de una materia.
        
        Args:
            subject: Nombre de la materia
            
        Returns:
            dict: Información de la materia (nombre, descripción, grado, etc.)
        """
        content = self.load_subject(subject)
        
        if not content:
            return None
        
        return {
            'name': content.get('name'),
            'description': content.get('description'),
            'grade_level': content.get('grade_level'),
            'icon': content.get('icon'),
            'topics_count': len(content.get('topics', []))
        }
    
    def get_all_subjects(self) -> List[str]:
        """
        Obtiene la lista de todas las materias disponibles.
        
        Returns:
            List[str]: Lista de nombres de materias
        """
        subjects = []
        
        for file_path in self.curriculum_dir.glob('*.json'):
            subject_name = file_path.stem
            subjects.append(subject_name)
        
        return subjects
    
    def search_content(self, subject: str, query: str) -> List[dict]:
        """
        Busca contenido dentro de una materia por palabras clave.
        
        Args:
            subject: Nombre de la materia
            query: Término de búsqueda
            
        Returns:
            List[dict]: Lista de temas que coinciden con la búsqueda
        """
        topics = self.get_topics(subject)
        results = []
        
        query_lower = query.lower()
        
        for topic in topics:
            # Buscar en título y descripción
            title = topic.get('title', '').lower()
            description = topic.get('description', '').lower()
            keywords = [k.lower() for k in topic.get('keywords', [])]
            
            if (query_lower in title or 
                query_lower in description or 
                any(query_lower in kw for kw in keywords)):
                results.append(topic)
        
        return results
    
    def reload_subject(self, subject: str):
        """
        Recarga el contenido de una materia desde el archivo.
        
        Args:
            subject: Nombre de la materia
        """
        if subject in self._content_cache:
            del self._content_cache[subject]
        
        self.load_subject(subject)
        logger.info(f"Reloaded curriculum for: {subject}")
    
    def clear_cache(self):
        """Limpia el cache de contenido"""
        self._content_cache.clear()
        logger.info("Content cache cleared")


# Singleton instance
_content_loader: Optional[ContentLoader] = None


def get_content_loader(curriculum_dir: str = "data/curriculum") -> ContentLoader:
    """
    Obtiene la instancia singleton del ContentLoader.
    
    Args:
        curriculum_dir: Directorio de curriculum
        
    Returns:
        ContentLoader: Instancia del cargador de contenido
    """
    global _content_loader
    
    if _content_loader is None:
        _content_loader = ContentLoader(curriculum_dir)
    
    return _content_loader
