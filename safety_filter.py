"""
Maiten AI - Learn better
Safety Filter

Filtro de seguridad para contenido apropiado para menores.
"""

import re
import logging
from typing import List

logger = logging.getLogger(__name__)


class SafetyFilter:
    """
    Filtro de seguridad para contenido educativo infantil
    """
    
    def __init__(self):
        """Inicializa el filtro de seguridad"""
        
        # Palabras prohibidas (contenido inapropiado)
        self.blocked_words = [
            # Esta lista sería más extensa en producción
            # Se incluyen ejemplos generales de categorías prohibidas
        ]
        
        # Temas inapropiados para detectar
        self.inappropriate_topics = [
            "violencia",
            "drogas",
            "alcohol",
            "contenido adulto",
            "política controversial"
        ]
        
        # Patrones de información personal a detectar
        self.personal_info_patterns = [
            r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',  # Teléfonos
            r'\b\d{1,5}\s+\w+\s+(street|st|avenue|ave|road|rd)\b',  # Direcciones
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Emails
        ]
    
    def is_safe_input(self, text: str) -> bool:
        """
        Verifica si el input del usuario es seguro.
        
        Args:
            text: Texto del usuario
            
        Returns:
            bool: True si es seguro
        """
        if not text:
            return True
        
        text_lower = text.lower()
        
        # 1. Verificar palabras bloqueadas
        for word in self.blocked_words:
            if word in text_lower:
                logger.warning(f"Blocked word detected in input: {word}")
                return False
        
        # 2. Verificar que no esté compartiendo información personal
        for pattern in self.personal_info_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                logger.warning("Personal information pattern detected in input")
                return False
        
        # 3. Verificar longitud razonable (evitar spam)
        if len(text) > 500:
            logger.warning("Input too long")
            return False
        
        return True
    
    def is_safe_output(self, text: str) -> bool:
        """
        Verifica si el output de la IA es seguro.
        
        Args:
            text: Texto generado por la IA
            
        Returns:
            bool: True si es seguro
        """
        if not text:
            return True
        
        text_lower = text.lower()
        
        # 1. Verificar palabras bloqueadas
        for word in self.blocked_words:
            if word in text_lower:
                logger.warning(f"Blocked word in AI output: {word}")
                return False
        
        # 2. Verificar temas inapropiados
        for topic in self.inappropriate_topics:
            if topic in text_lower:
                logger.warning(f"Inappropriate topic in output: {topic}")
                return False
        
        # 3. Verificar que no contenga URLs sospechosas
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, text)
        
        if urls:
            # En producción, aquí se verificaría contra una whitelist de dominios educativos
            logger.info(f"URLs found in output: {urls}")
        
        return True
    
    def sanitize_response(self, text: str) -> str:
        """
        Sanitiza una respuesta removiendo contenido potencialmente inseguro.
        
        Args:
            text: Texto a sanitizar
            
        Returns:
            str: Texto sanitizado
        """
        # Remover URLs no whitelisted
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        text = re.sub(url_pattern, '[enlace removido]', text)
        
        # Remover emails
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        text = re.sub(email_pattern, '[email removido]', text)
        
        # Remover teléfonos
        phone_pattern = r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'
        text = re.sub(phone_pattern, '[teléfono removido]', text)
        
        return text
    
    def is_educational_content(self, text: str) -> bool:
        """
        Verifica si el contenido es educativo.
        
        Args:
            text: Texto a verificar
            
        Returns:
            bool: True si parece contenido educativo
        """
        text_lower = text.lower()
        
        # Palabras clave educativas
        educational_keywords = [
            "aprender", "estudiar", "práctica", "ejercicio", "tarea",
            "matemáticas", "lengua", "ciencias", "leer", "escribir",
            "explicar", "entender", "comprender", "resolver"
        ]
        
        # Contar cuántas palabras clave educativas aparecen
        keyword_count = sum(1 for keyword in educational_keywords if keyword in text_lower)
        
        # Si tiene al menos 2 palabras clave educativas, probablemente es educativo
        return keyword_count >= 2
    
    def check_age_appropriateness(self, text: str, target_age: int = 9) -> bool:
        """
        Verifica si el contenido es apropiado para la edad.
        
        Args:
            text: Texto a verificar
            target_age: Edad objetivo
            
        Returns:
            bool: True si es apropiado
        """
        text_lower = text.lower()
        
        # Temas no apropiados para menores de 10 años
        young_inappropriate = [
            "muerte", "violencia", "miedo", "terror",
            "adulto", "sexo", "droga", "alcohol"
        ]
        
        for topic in young_inappropriate:
            if topic in text_lower:
                # Excepciones educativas (ej: "muerte de dinosaurios")
                educational_context = ["historia", "ciencia", "naturaleza", "dinosaurio"]
                
                has_educational_context = any(ctx in text_lower for ctx in educational_context)
                
                if not has_educational_context:
                    logger.warning(f"Age-inappropriate topic found: {topic}")
                    return False
        
        return True
    
    def get_safety_report(self, text: str) -> dict:
        """
        Genera un reporte completo de seguridad.
        
        Args:
            text: Texto a analizar
            
        Returns:
            dict: Reporte de seguridad
        """
        return {
            "is_safe_input": self.is_safe_input(text),
            "is_safe_output": self.is_safe_output(text),
            "is_educational": self.is_educational_content(text),
            "is_age_appropriate": self.check_age_appropriateness(text),
            "text_length": len(text),
            "overall_safe": all([
                self.is_safe_input(text),
                self.is_safe_output(text),
                self.check_age_appropriateness(text)
            ])
        }


# Para testing
if __name__ == "__main__":
    filter = SafetyFilter()
    
    # Test 1: Contenido educativo seguro
    safe_text = "¿Puedes ayudarme a aprender sobre fracciones en matemáticas?"
    print("Test 1 (Educativo):", filter.get_safety_report(safe_text))
    
    # Test 2: Intentando compartir información personal
    unsafe_text = "Mi teléfono es 555-123-4567"
    print("\nTest 2 (Info Personal):", filter.get_safety_report(unsafe_text))
    
    # Test 3: Contenido no educativo pero seguro
    offtopic_text = "¿Cuál es tu color favorito?"
    print("\nTest 3 (Off-topic):", filter.get_safety_report(offtopic_text))
