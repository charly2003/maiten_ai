"""
Maiten AI - Learn better
Content Adapter

Adapta el contenido de IA al nivel educativo del estudiante.
"""

import re
import logging

logger = logging.getLogger(__name__)


class ContentAdapter:
    """
    Adaptador de contenido para nivel educativo de 4to grado
    """
    
    def __init__(self, student_age: int = 9, grade_level: int = 4):
        """
        Inicializa el adaptador.
        
        Args:
            student_age: Edad del estudiante
            grade_level: Grado escolar
        """
        self.student_age = student_age
        self.grade_level = grade_level
        
        # Palabras complejas y sus equivalentes simples
        self.word_simplifications = {
            "utilizar": "usar",
            "realizar": "hacer",
            "efectuar": "hacer",
            "obtener": "conseguir",
            "adquirir": "obtener",
            "incrementar": "aumentar",
            "decrementar": "disminuir",
            "posteriormente": "después",
            "previamente": "antes",
            "aproximadamente": "más o menos",
            "específicamente": "en especial",
            "consecuentemente": "por eso",
            "adicionalmente": "además"
        }
    
    def adapt_response(self, text: str) -> str:
        """
        Adapta una respuesta al nivel del estudiante.
        
        Args:
            text: Texto original
            
        Returns:
            str: Texto adaptado
        """
        if not text:
            return text
        
        # 1. Simplificar palabras complejas
        adapted_text = self._simplify_vocabulary(text)
        
        # 2. Acortar oraciones muy largas
        adapted_text = self._shorten_long_sentences(adapted_text)
        
        # 3. Verificar que no sea demasiado largo
        adapted_text = self._limit_length(adapted_text)
        
        return adapted_text
    
    def _simplify_vocabulary(self, text: str) -> str:
        """Simplifica vocabulario complejo"""
        for complex_word, simple_word in self.word_simplifications.items():
            # Reemplazo case-insensitive con regex
            pattern = re.compile(re.escape(complex_word), re.IGNORECASE)
            text = pattern.sub(simple_word, text)
        
        return text
    
    def _shorten_long_sentences(self, text: str) -> str:
        """
        Divide oraciones muy largas en oraciones más cortas.
        Considera "larga" una oración de más de 20 palabras.
        """
        sentences = text.split('.')
        shortened_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            words = sentence.split()
            
            # Si la oración tiene más de 20 palabras, intentar dividirla
            if len(words) > 20:
                # Buscar conjunciones para dividir
                conjunctions = [' y ', ' o ', ', ']
                best_split = None
                best_distance = float('inf')
                
                for conj in conjunctions:
                    if conj in sentence:
                        # Encontrar la posición más cercana al medio
                        mid_point = len(sentence) // 2
                        positions = [m.start() for m in re.finditer(re.escape(conj), sentence)]
                        
                        for pos in positions:
                            distance = abs(pos - mid_point)
                            if distance < best_distance:
                                best_distance = distance
                                best_split = pos
                
                if best_split:
                    # Dividir en dos oraciones
                    part1 = sentence[:best_split].strip()
                    part2 = sentence[best_split:].strip()
                    
                    if part2.startswith(', '):
                        part2 = part2[2:].capitalize()
                    elif part2.startswith(' y '):
                        part2 = part2[3:].capitalize()
                    elif part2.startswith(' o '):
                        part2 = part2[3:].capitalize()
                    
                    shortened_sentences.append(part1)
                    shortened_sentences.append(part2)
                else:
                    shortened_sentences.append(sentence)
            else:
                shortened_sentences.append(sentence)
        
        return '. '.join(shortened_sentences) + ('.' if not text.endswith('.') else '')
    
    def _limit_length(self, text: str, max_words: int = 200) -> str:
        """
        Limita la longitud del texto.
        
        Args:
            text: Texto original
            max_words: Máximo de palabras permitidas
            
        Returns:
            str: Texto limitado
        """
        words = text.split()
        
        if len(words) <= max_words:
            return text
        
        # Si es muy largo, cortar y agregar indicador
        truncated = ' '.join(words[:max_words])
        
        # Intentar terminar en un punto
        last_period = truncated.rfind('.')
        if last_period > len(truncated) * 0.7:  # Si hay un punto en el último 30%
            truncated = truncated[:last_period + 1]
        else:
            truncated += "..."
        
        logger.warning(f"Response truncated from {len(words)} to {max_words} words")
        
        return truncated
    
    def check_reading_level(self, text: str) -> Dict[str, any]:
        """
        Verifica el nivel de lectura del texto.
        
        Args:
            text: Texto a analizar
            
        Returns:
            Dict con métricas de legibilidad
        """
        words = text.split()
        sentences = [s for s in text.split('.') if s.strip()]
        
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        
        # Estimación simple de nivel de grado (fórmula simplificada)
        # Basada en longitud promedio de palabras y oraciones
        grade_estimate = 0.4 * avg_sentence_length + 0.1 * avg_word_length
        
        return {
            "total_words": len(words),
            "total_sentences": len(sentences),
            "avg_word_length": round(avg_word_length, 1),
            "avg_sentence_length": round(avg_sentence_length, 1),
            "estimated_grade": round(grade_estimate, 1),
            "appropriate": grade_estimate <= self.grade_level + 2
        }


# Para testing
if __name__ == "__main__":
    adapter = ContentAdapter()
    
    test_text = """Es fundamental que utilices correctamente los procedimientos matemáticos 
    para obtener resultados precisos, ya que esto te permitirá incrementar tu comprensión 
    de conceptos más complejos posteriormente, y consecuentemente, mejorar tu desempeño académico."""
    
    print("Original:", test_text)
    print("\nAdaptado:", adapter.adapt_response(test_text))
    print("\nNivel de lectura:", adapter.check_reading_level(test_text))
