"""
Maiten AI - Learn better
Voice Manager

Coordina servicios de Text-to-Speech y Speech-to-Text.
"""

import logging
import threading
from typing import Optional, Callable

from ..services.tts_service import get_tts_service
from ..services.stt_service import get_stt_service

logger = logging.getLogger(__name__)


class VoiceManager:
    """
    Gestor de servicios de voz (TTS y STT)
    """
    
    def __init__(self):
        """Inicializa el gestor de voz"""
        self.tts = get_tts_service()
        self.stt = get_stt_service()
        self.is_listening = False
        self.continuous_listening = False
        self._stop_listening_event = threading.Event()
        
        logger.info("Voice Manager initialized")
    
    def speak(self, text: str, blocking: bool = False, on_finish: Optional[Callable] = None):
        """
        Convierte texto a voz.
        
        Args:
            text: Texto a pronunciar
            blocking: Si True, espera a que termine de hablar
            on_finish: Callback al terminar
        """
        self.tts.speak(text, blocking=blocking, on_finish=on_finish)
    
    def stop_speaking(self):
        """Detiene la voz actual"""
        self.tts.stop()
    
    def is_speaking(self) -> bool:
        """
        Verifica si está hablando.
        
        Returns:
            bool: True si está hablando
        """
        return self.tts.is_busy()
    
    def listen(
        self,
        timeout: Optional[int] = 5,
        phrase_time_limit: Optional[int] = 10
    ) -> Optional[str]:
        """
        Escucha desde el micrófono.
        
        Args:
            timeout: Tiempo máximo de espera en segundos
            phrase_time_limit: Duración máxima de la frase
            
        Returns:
            Optional[str]: Texto reconocido o None
        """
        if self.is_listening:
            logger.warning("Already listening")
            return None
        
        self.is_listening = True
        
        try:
            text = self.stt.listen_from_microphone(
                timeout=timeout,
                phrase_time_limit=phrase_time_limit
            )
            return text
        finally:
            self.is_listening = False
    
    def listen_and_speak_result(
        self,
        timeout: int = 5,
        on_result: Optional[Callable[[str], None]] = None
    ):
        """
        Escucha y pronuncia lo que escuchó.
        
        Args:
            timeout: Tiempo máximo de espera
            on_result: Callback con el texto reconocido
        """
        text = self.listen(timeout=timeout)
        
        if text:
            logger.info(f"Heard: {text}")
            self.speak(f"Escuché: {text}")
            
            if on_result:
                on_result(text)
        else:
            self.speak("No pude escucharte. ¿Puedes repetir?")
    
    def start_continuous_listening(
        self,
        on_text_callback: Callable[[str], None],
        timeout: int = 5
    ):
        """
        Inicia escucha continua en background.
        
        Args:
            on_text_callback: Función a llamar con cada texto reconocido
            timeout: Timeout para cada escucha
        """
        if self.continuous_listening:
            logger.warning("Continuous listening already active")
            return
        
        self.continuous_listening = True
        self._stop_listening_event.clear()
        
        # Iniciar en thread separado
        thread = threading.Thread(
            target=self._continuous_listen_loop,
            args=(on_text_callback, timeout)
        )
        thread.daemon = True
        thread.start()
        
        logger.info("Continuous listening started")
    
    def stop_continuous_listening(self):
        """Detiene la escucha continua"""
        if not self.continuous_listening:
            return
        
        self._stop_listening_event.set()
        self.continuous_listening = False
        logger.info("Continuous listening stopped")
    
    def _continuous_listen_loop(self, callback: Callable[[str], None], timeout: int):
        """Loop de escucha continua"""
        self.stt.listen_continuous(
            callback=callback,
            stop_event=self._stop_listening_event,
            timeout=timeout
        )
    
    def configure_tts(self, rate: Optional[int] = None, volume: Optional[float] = None):
        """
        Configura parámetros de TTS.
        
        Args:
            rate: Velocidad de habla (100-300)
            volume: Volumen (0.0-1.0)
        """
        if rate is not None:
            self.tts.set_rate(rate)
        
        if volume is not None:
            self.tts.set_volume(volume)
    
    def configure_stt(self, language: Optional[str] = None, energy_threshold: Optional[int] = None):
        """
        Configura parámetros de STT.
        
        Args:
            language: Código de idioma (ej: 'es-ES')
            energy_threshold: Umbral de energía
        """
        if language is not None:
            self.stt.set_language(language)
        
        if energy_threshold is not None:
            self.stt.set_energy_threshold(energy_threshold)
    
    def get_tts_voices(self) -> list:
        """Obtiene voces disponibles para TTS"""
        return self.tts.get_available_voices()
    
    def set_tts_voice(self, voice_id: str):
        """Establece la voz de TTS"""
        self.tts.set_voice(voice_id)
    
    def get_microphones(self) -> list:
        """Obtiene micrófonos disponibles"""
        return self.stt.get_available_microphones()
    
    def set_microphone(self, device_index: int):
        """Establece el micrófono a usar"""
        self.stt.set_microphone(device_index)
    
    def test_voice_system(self) -> dict:
        """
        Prueba el sistema de voz completo.
        
        Returns:
            dict: Resultados de las pruebas
        """
        results = {
            "tts_available": self.tts.enabled,
            "stt_available": self.stt.enabled,
            "microphone_working": False,
            "voices_count": 0
        }
        
        # Probar micrófono
        if self.stt.enabled:
            results["microphone_working"] = self.stt.test_microphone()
        
        # Contar voces
        if self.tts.enabled:
            voices = self.tts.get_available_voices()
            results["voices_count"] = len(voices)
        
        return results
    
    def conversation_mode(
        self,
        on_user_speech: Callable[[str], str],
        greeting: str = "¡Hola! Estoy lista para escucharte."
    ):
        """
        Modo de conversación interactivo.
        
        Args:
            on_user_speech: Función que recibe texto del usuario y retorna respuesta
            greeting: Mensaje de bienvenida
        """
        # Saludar
        self.speak(greeting, blocking=True)
        
        logger.info("Entering conversation mode")
        
        try:
            while True:
                # Escuchar
                self.speak("Te escucho...", blocking=True)
                user_text = self.listen(timeout=10, phrase_time_limit=15)
                
                if not user_text:
                    self.speak("No pude escucharte. ¿Continuamos?")
                    continue
                
                # Verificar si quiere salir
                if any(word in user_text.lower() for word in ["adiós", "salir", "terminar", "chao"]):
                    self.speak("¡Hasta pronto! Fue un placer ayudarte.")
                    break
                
                # Procesar con callback
                response = on_user_speech(user_text)
                
                # Responder
                if response:
                    self.speak(response, blocking=True)
                    
        except KeyboardInterrupt:
            self.speak("Hasta pronto!")
        except Exception as e:
            logger.error(f"Error in conversation mode: {e}")
            self.speak("Hubo un error. Terminando la conversación.")


# Singleton instance
_voice_manager: Optional[VoiceManager] = None


def get_voice_manager() -> VoiceManager:
    """
    Obtiene la instancia singleton del VoiceManager.
    
    Returns:
        VoiceManager: Instancia del gestor
    """
    global _voice_manager
    
    if _voice_manager is None:
        _voice_manager = VoiceManager()
    
    return _voice_manager


# Para testing
if __name__ == "__main__":
    import time
    
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    vm = get_voice_manager()
    
    print("Testing Voice Manager...")
    
    # Test 1: Sistema de voz
    print("\n1. Testing voice system...")
    results = vm.test_voice_system()
    print(f"   TTS Available: {results['tts_available']}")
    print(f"   STT Available: {results['stt_available']}")
    print(f"   Microphone Working: {results['microphone_working']}")
    print(f"   Voices Available: {results['voices_count']}")
    
    # Test 2: Hablar
    print("\n2. Testing TTS...")
    vm.speak("Hola, soy Maiten AI. Aprende mejor conmigo.", blocking=True)
    
    # Test 3: Escuchar (comentar si no hay micrófono)
    print("\n3. Testing STT (say something in 5 seconds)...")
    text = vm.listen(timeout=5)
    if text:
        print(f"   You said: '{text}'")
        vm.speak(f"Escuché: {text}", blocking=True)
    
    print("\nVoice Manager test completed!")
