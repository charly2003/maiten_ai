"""
Maiten AI - Learn better
Text-to-Speech Service

Servicio de conversión de texto a voz.
"""

import os
import logging
import threading
from typing import Optional, Callable
import pyttsx3

logger = logging.getLogger(__name__)


class TTSService:
    """
    Servicio de Text-to-Speech usando pyttsx3
    """
    
    def __init__(self):
        """Inicializa el servicio TTS"""
        self.enabled = os.getenv("TTS_ENABLED", "True").lower() == "true"
        self.engine: Optional[pyttsx3.Engine] = None
        self.is_speaking = False
        self._lock = threading.Lock()
        
        if self.enabled:
            self._initialize_engine()
    
    def _initialize_engine(self):
        """Inicializa el motor de TTS"""
        try:
            self.engine = pyttsx3.init()
            
            # Configurar propiedades
            rate = int(os.getenv("TTS_RATE", "150"))
            volume = float(os.getenv("TTS_VOLUME", "0.9"))
            
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volume)
            
            # Intentar establecer voz en español
            voices = self.engine.getProperty('voices')
            spanish_voice = None
            
            for voice in voices:
                # Buscar voces en español
                if 'spanish' in voice.name.lower() or 'español' in voice.name.lower():
                    spanish_voice = voice.id
                    break
                # Alternativa: buscar voces femeninas en español
                elif 'es' in voice.languages or 'es-ES' in voice.id.lower():
                    spanish_voice = voice.id
                    break
            
            if spanish_voice:
                self.engine.setProperty('voice', spanish_voice)
                logger.info(f"Spanish voice set: {spanish_voice}")
            else:
                logger.warning("No Spanish voice found, using default")
            
            logger.info(f"TTS Service initialized - Rate: {rate}, Volume: {volume}")
            
        except Exception as e:
            logger.error(f"Error initializing TTS engine: {e}")
            self.enabled = False
    
    def speak(self, text: str, blocking: bool = False, on_finish: Optional[Callable] = None):
        """
        Convierte texto a voz.
        
        Args:
            text: Texto a convertir
            blocking: Si True, bloquea hasta terminar de hablar
            on_finish: Callback a ejecutar al terminar
        """
        if not self.enabled or not self.engine:
            logger.warning("TTS is disabled or not initialized")
            if on_finish:
                on_finish()
            return
        
        if not text:
            logger.warning("Empty text provided to TTS")
            if on_finish:
                on_finish()
            return
        
        with self._lock:
            if self.is_speaking:
                self.stop()
        
        try:
            # Limpiar texto (remover markdown, emojis excesivos, etc.)
            clean_text = self._clean_text(text)
            
            if blocking:
                self.is_speaking = True
                self.engine.say(clean_text)
                self.engine.runAndWait()
                self.is_speaking = False
                if on_finish:
                    on_finish()
            else:
                # Ejecutar en thread separado
                thread = threading.Thread(
                    target=self._speak_async,
                    args=(clean_text, on_finish)
                )
                thread.daemon = True
                thread.start()
            
            logger.debug(f"Speaking: {clean_text[:50]}...")
            
        except Exception as e:
            logger.error(f"Error in TTS speak: {e}")
            self.is_speaking = False
            if on_finish:
                on_finish()
    
    def _speak_async(self, text: str, on_finish: Optional[Callable] = None):
        """Habla de forma asíncrona"""
        try:
            self.is_speaking = True
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"Error in async speak: {e}")
        finally:
            self.is_speaking = False
            if on_finish:
                try:
                    on_finish()
                except Exception as e:
                    logger.error(f"Error in on_finish callback: {e}")
    
    def stop(self):
        """Detiene la reproducción actual"""
        if not self.enabled or not self.engine:
            return
        
        try:
            if self.is_speaking:
                self.engine.stop()
                self.is_speaking = False
                logger.debug("TTS stopped")
        except Exception as e:
            logger.error(f"Error stopping TTS: {e}")
    
    def is_busy(self) -> bool:
        """
        Verifica si está hablando actualmente.
        
        Returns:
            bool: True si está hablando
        """
        return self.is_speaking
    
    def set_rate(self, rate: int):
        """
        Establece la velocidad de habla.
        
        Args:
            rate: Palabras por minuto (100-300, típico: 150-200)
        """
        if not self.enabled or not self.engine:
            return
        
        try:
            self.engine.setProperty('rate', rate)
            logger.info(f"TTS rate set to: {rate}")
        except Exception as e:
            logger.error(f"Error setting TTS rate: {e}")
    
    def set_volume(self, volume: float):
        """
        Establece el volumen.
        
        Args:
            volume: Volumen (0.0 a 1.0)
        """
        if not self.enabled or not self.engine:
            return
        
        try:
            volume = max(0.0, min(1.0, volume))  # Clamp entre 0 y 1
            self.engine.setProperty('volume', volume)
            logger.info(f"TTS volume set to: {volume}")
        except Exception as e:
            logger.error(f"Error setting TTS volume: {e}")
    
    def get_available_voices(self) -> list:
        """
        Obtiene las voces disponibles.
        
        Returns:
            list: Lista de voces disponibles
        """
        if not self.enabled or not self.engine:
            return []
        
        try:
            voices = self.engine.getProperty('voices')
            return [
                {
                    'id': voice.id,
                    'name': voice.name,
                    'languages': voice.languages,
                    'gender': getattr(voice, 'gender', 'unknown')
                }
                for voice in voices
            ]
        except Exception as e:
            logger.error(f"Error getting voices: {e}")
            return []
    
    def set_voice(self, voice_id: str):
        """
        Establece la voz a usar.
        
        Args:
            voice_id: ID de la voz
        """
        if not self.enabled or not self.engine:
            return
        
        try:
            self.engine.setProperty('voice', voice_id)
            logger.info(f"Voice set to: {voice_id}")
        except Exception as e:
            logger.error(f"Error setting voice: {e}")
    
    def _clean_text(self, text: str) -> str:
        """
        Limpia el texto para TTS.
        
        Args:
            text: Texto original
            
        Returns:
            str: Texto limpio
        """
        # Remover markdown
        import re
        
        # Remover asteriscos (bold/italic)
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'\*(.+?)\*', r'\1', text)
        
        # Remover enlaces markdown
        text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
        
        # Remover emojis excesivos (dejar solo algunos)
        # Los emojis no se leen bien en TTS
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE
        )
        text = emoji_pattern.sub('', text)
        
        # Limpiar espacios múltiples
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def save_to_file(self, text: str, filename: str):
        """
        Guarda el audio en un archivo.
        
        Args:
            text: Texto a convertir
            filename: Ruta del archivo de salida
        """
        if not self.enabled or not self.engine:
            logger.warning("TTS is disabled or not initialized")
            return
        
        try:
            clean_text = self._clean_text(text)
            self.engine.save_to_file(clean_text, filename)
            self.engine.runAndWait()
            logger.info(f"Audio saved to: {filename}")
        except Exception as e:
            logger.error(f"Error saving TTS to file: {e}")


# Singleton instance
_tts_service: Optional[TTSService] = None


def get_tts_service() -> TTSService:
    """
    Obtiene la instancia singleton del servicio TTS.
    
    Returns:
        TTSService: Instancia del servicio
    """
    global _tts_service
    
    if _tts_service is None:
        _tts_service = TTSService()
    
    return _tts_service


# Para testing
if __name__ == "__main__":
    import time
    
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    tts = get_tts_service()
    
    print("Testing TTS Service...")
    
    # Test 1: Hablar texto simple
    print("\n1. Speaking simple text...")
    tts.speak("Hola, soy Maiten AI. Estoy aquí para ayudarte a aprender mejor.")
    time.sleep(3)
    
    # Test 2: Listar voces disponibles
    print("\n2. Available voices:")
    voices = tts.get_available_voices()
    for i, voice in enumerate(voices[:5], 1):  # Mostrar solo las primeras 5
        print(f"   {i}. {voice['name']} - {voice.get('languages', 'unknown')}")
    
    # Test 3: Hablar con callback
    print("\n3. Speaking with callback...")
    
    def on_finish():
        print("   ✓ Finished speaking!")
    
    tts.speak("Este es un mensaje de prueba con callback.", on_finish=on_finish)
    time.sleep(3)
    
    print("\nTTS Service test completed!")
