"""
Maiten AI - Learn better
Prompt Engine

Genera prompts educativos adaptados para niños de 9 años.
"""

import logging
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)


class PromptEngine:
    """
    Motor de generación de prompts educativos para Maiten AI
    """
    
    def __init__(self, student_name: str = "Maitena", student_age: int = 9, grade_level: int = 4):
        """
        Inicializa el motor de prompts.
        
        Args:
            student_name: Nombre del estudiante
            student_age: Edad del estudiante
            grade_level: Grado escolar
        """
        self.student_name = student_name
        self.student_age = student_age
        self.grade_level = grade_level
    
    def get_base_system_prompt(self) -> str:
        """
        Obtiene el prompt base del sistema para Maiten AI.
        
        Returns:
            str: System prompt base
        """
        return f"""Eres Maiten AI, un asistente educativo amigable y paciente. Tu lema es "Learn better" (Aprende mejor).

INFORMACIÓN DEL ESTUDIANTE:
- Nombre: {self.student_name}
- Edad: {self.student_age} años
- Grado: {self.grade_level}° grado de primaria

TU PERSONALIDAD:
- Eres alegre, motivadora y siempre positiva
- Celebras cada logro, por pequeño que sea
- Eres paciente y nunca te frustras
- Usas ejemplos de la vida cotidiana que un niño de {self.student_age} años puede entender
- Haces que aprender sea divertido y entretenido

REGLAS IMPORTANTES:
1. Usa un lenguaje simple y claro, apropiado para {self.student_age} años
2. Divide conceptos complejos en pasos pequeños y fáciles
3. Usa ejemplos concretos: comida, juguetes, animales, deportes
4. Incluye emojis ocasionalmente para hacer la conversación más amigable 😊
5. Pregunta si entendió antes de avanzar a conceptos más difíciles
6. Si el estudiante se equivoca, explica el error con amabilidad
7. Celebra los aciertos con entusiasmo: "¡Excelente!", "¡Muy bien!", "¡Correcto!"
8. Mantén las explicaciones cortas (máximo 3-4 párrafos)
9. Usa analogías y comparaciones que un niño pueda visualizar
10. Nunca des respuestas directas a ejercicios; guía con pistas y preguntas

CONTENIDO SEGURO:
- Todo el contenido debe ser apropiado para menores
- No compartas información personal sensible
- Mantén el foco en temas educativos
- Si te preguntan algo inapropiado, redirige gentilmente al estudio

ESTILO DE ENSEÑANZA:
- Método socrático: haz preguntas que guíen al razonamiento
- Aprendizaje activo: propón que el estudiante participe
- Refuerzo positivo: elogia el esfuerzo, no solo el resultado
- Paciencia infinita: nunca muestres frustración

Recuerda: Tu objetivo es que {self.student_name} aprenda mejor (Learn better) y disfrute el proceso."""
    
    def get_subject_context(self, subject: str, topic: Optional[str] = None) -> str:
        """
        Obtiene contexto adicional para una materia específica.
        
        Args:
            subject: Nombre de la materia
            topic: Tema específico (opcional)
            
        Returns:
            str: Contexto adicional
        """
        subject_contexts = {
            "matematicas": f"""CONTEXTO DE MATEMÁTICAS:
Estamos trabajando en matemáticas de {self.grade_level}° grado.
Enfócate en:
- Usar objetos concretos para explicar conceptos abstractos
- Dibujar con palabras (describe imágenes mentales)
- Relacionar con situaciones cotidianas (ir de compras, cocinar, jugar)
- Enseñar trucos mnemotécnicos y atajos
- Verificar respuestas con métodos alternativos""",
            
            "lengua": f"""CONTEXTO DE LENGUA:
Estamos trabajando en lengua y literatura de {self.grade_level}° grado.
Enfócate en:
- Gramática con ejemplos de conversaciones reales
- Lectura comprensiva con textos apropiados para la edad
- Escritura creativa con temas que le interesen
- Ortografía con trucos para recordar reglas
- Vocabulario con palabras del día a día""",
            
            "ciencias": f"""CONTEXTO DE CIENCIAS NATURALES:
Estamos trabajando en ciencias de {self.grade_level}° grado.
Enfócate en:
- Explicaciones con fenómenos que puede observar
- Experimentos simples que puede hacer en casa (con supervisión)
- Curiosidades y datos fascinantes
- Conexión con la naturaleza y el mundo real
- Método científico: observar, preguntar, experimentar""",
            
            "sociales": f"""CONTEXTO DE CIENCIAS SOCIALES:
Estamos trabajando en sociales de {self.grade_level}° grado.
Enfócate en:
- Historia con anécdotas y personajes interesantes
- Geografía con referencias a lugares que conoce
- Cultura y diversidad con respeto y curiosidad
- Conexión con su vida y su comunidad
- Mapas, imágenes y descripciones visuales"""
        }
        
        context = subject_contexts.get(subject, "")
        
        if topic:
            context += f"\n\nTEMA ACTUAL: {topic}\nAsegúrate de enfocarte específicamente en este tema."
        
        return context
    
    def create_teaching_prompt(
        self, 
        subject: str, 
        topic: Optional[str] = None,
        student_question: Optional[str] = None,
        context: Optional[Dict] = None
    ) -> str:
        """
        Crea un prompt completo para enseñanza.
        
        Args:
            subject: Materia
            topic: Tema específico
            student_question: Pregunta del estudiante
            context: Contexto adicional (progreso, errores previos, etc.)
            
        Returns:
            str: System prompt completo
        """
        base = self.get_base_system_prompt()
        subject_ctx = self.get_subject_context(subject, topic)
        
        prompt_parts = [base, subject_ctx]
        
        if context:
            # Agregar información de progreso si está disponible
            if context.get("mastery_level"):
                mastery = context["mastery_level"]
                prompt_parts.append(f"\nNIVEL DE DOMINIO DEL TEMA: {mastery*100:.0f}%")
                
                if mastery < 0.3:
                    prompt_parts.append("El estudiante es principiante en este tema. Usa explicaciones muy básicas.")
                elif mastery < 0.7:
                    prompt_parts.append("El estudiante tiene conocimiento intermedio. Puedes profundizar un poco más.")
                else:
                    prompt_parts.append("El estudiante domina bien este tema. Puedes plantear desafíos más complejos.")
            
            # Agregar errores comunes si existen
            if context.get("common_mistakes"):
                mistakes = context["common_mistakes"]
                prompt_parts.append(f"\nERRORES PREVIOS: {', '.join(mistakes)}\nAyuda a evitar estos errores.")
        
        if student_question:
            prompt_parts.append(f"\n\nPREGUNTA ACTUAL DEL ESTUDIANTE:\n{student_question}")
        
        return "\n".join(prompt_parts)
    
    def create_exercise_prompt(
        self,
        subject: str,
        topic: str,
        difficulty: str = "medium",
        exercise_type: str = "practice"
    ) -> str:
        """
        Crea un prompt para generar ejercicios.
        
        Args:
            subject: Materia
            topic: Tema
            difficulty: Nivel de dificultad (easy, medium, hard)
            exercise_type: Tipo de ejercicio (practice, word_problem, concept, drill)
            
        Returns:
            str: Prompt para generar ejercicios
        """
        difficulty_levels = {
            "easy": "muy fácil, para principiantes",
            "medium": "de dificultad media",
            "hard": "desafiante pero apropiado para la edad"
        }
        
        exercise_types_es = {
            "practice": "ejercicio de práctica",
            "word_problem": "problema con palabras (situación de la vida real)",
            "concept": "pregunta conceptual para verificar comprensión",
            "drill": "ejercicio de repetición para memorización"
        }
        
        return f"""Genera un {exercise_types_es.get(exercise_type, 'ejercicio')} sobre {topic} en {subject}.

Requisitos:
- Dificultad: {difficulty_levels.get(difficulty, 'media')}
- Apropiado para {self.student_age} años ({self.grade_level}° grado)
- Contexto interesante y relevante
- Incluye una pista útil (sin dar la respuesta completa)

Formato:
1. Pregunta clara y específica
2. Pista que guíe el razonamiento
3. Respuesta correcta (para validación interna)

Haz que sea entretenido y educativo."""
    
    def create_explanation_prompt(self, concept: str, subject: str) -> str:
        """
        Crea un prompt para explicar un concepto.
        
        Args:
            concept: Concepto a explicar
            subject: Materia
            
        Returns:
            str: Prompt para explicación
        """
        return f"""Explica el concepto "{concept}" en {subject} de manera que {self.student_name} ({self.student_age} años) lo entienda perfectamente.

Estructura tu explicación así:
1. **¿Qué es?** - Definición simple en una frase
2. **Ejemplo de la vida real** - Algo que puede ver/tocar/experimentar
3. **¿Cómo funciona?** - Explicación paso a paso
4. **Practiquemos** - Un mini ejercicio para verificar comprensión

Usa:
- Lenguaje simple y claro
- Ejemplos concretos (comida, juegos, animales)
- Comparaciones que pueda visualizar
- Emojis ocasionales 😊

Mantén cada sección en 2-3 frases. Total máximo: 4 párrafos cortos."""
    
    def create_encouragement_prompt(self, situation: str) -> str:
        """
        Crea un prompt para mensajes de motivación.
        
        Args:
            situation: Situación (correct_answer, wrong_answer, struggling, achievement)
            
        Returns:
            str: Mensaje motivacional
        """
        situations = {
            "correct_answer": "¡El estudiante respondió correctamente! Celebra su éxito con entusiasmo.",
            "wrong_answer": "El estudiante cometió un error. Sé comprensivo, explica qué salió mal y anímalo a intentarlo de nuevo.",
            "struggling": "El estudiante está teniendo dificultades. Sé extra paciente, divide el problema en pasos más pequeños.",
            "achievement": "¡El estudiante alcanzó un logro! Celebra su progreso y esfuerzo."
        }
        
        return f"""Genera un mensaje motivacional apropiado:

Situación: {situations.get(situation, situation)}

El mensaje debe:
- Ser breve (1-2 frases)
- Ser genuino y cálido
- Incluir un emoji apropiado
- Enfocarse en el esfuerzo, no solo el resultado
- Motivar a seguir aprendiendo

Recuerda: Eres Maiten AI y tu lema es "Learn better"."""


# Singleton instance
_prompt_engine: Optional[PromptEngine] = None


def get_prompt_engine(
    student_name: str = "Maitena",
    student_age: int = 9,
    grade_level: int = 4
) -> PromptEngine:
    """
    Obtiene la instancia singleton del PromptEngine.
    
    Returns:
        PromptEngine: Instancia del motor de prompts
    """
    global _prompt_engine
    
    if _prompt_engine is None:
        _prompt_engine = PromptEngine(student_name, student_age, grade_level)
    
    return _prompt_engine
