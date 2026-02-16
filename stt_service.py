"""
Maiten AI - Learn better
Speech-to-Text Service

Servicio de conversión de voz a texto.
"""

import os
import logging
from typing import Optional
import speech_recognition as sr

logger = logging.getLogger(__name__)


class STTService:
    """
    Servicio de Speech-to-Text usando SpeechRecognition
    """
    
    def __init__(self):
        """Inicializa el servicio STT"""
        self.enabled = os.getenv("STT_ENABLED", "True").lower() == "true"
        self.language = os.getenv("STT_LANGUAGE", "es-ES")
        self.recognizer = sr.Recognizer()
        
        # Configurar parámetros del reconocedor
        self.recognizer.energy_threshold = 4000  # Ajustar según ambiente
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8  # Segundos de silencio para considerar fin
        
        logger.info(f"STT Service initialized - Language: {self.language}")
    
    def listen_from_microphone(
        self,
        timeout: Optional[int] = None,
        phrase_time_limit: Optional[int] = None
    ) -> Optional[str]:
        """
        Escucha desde el micrófono y convierte a texto.
        
        Args:
            timeout: Segundos máximo para esperar inicio del habla
            phrase_time_limit: Segundos máximo para una frase
            
        Returns:
            Optional[str]: Texto reconocido o None si falla
        """
        if not self.enabled:
            logger.warning("STT is disabled")
            return None
        
        try:
            with sr.Microphone() as source:
                logger.info("Listening... Speak now!")
                
                # Ajustar ruido ambiente
                logger.debug("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Escuchar
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                
                logger.debug("Processing audio...")
                
                # Reconocer con Google Speech Recognition (gratis)
                text = self.recognizer.recognize_google(
                    audio,
                    language=self.language
                )
                
                logger.info(f"Recognized: {text}")
                return text
                
        except sr.WaitTimeoutError:
            logger.warning("Listening timed out - no speech detected")
            return None
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Could not request results from speech recognition service: {e}")
            return None
        except Exception as e:
            logger.error(f"Error in STT listen: {e}")
            return None
    
    def recognize_from_file(self, audio_file_path: str) -> Optional[str]:
        """
        Reconoce texto desde un archivo de audio.
        
        Args:
            audio_file_path: Ruta al archivo de audio
            
        Returns:
            Optional[str]: Texto reconocido o None si falla
        """
        if not self.enabled:
            logger.warning("STT is disabled")
            return None
        
        try:
            with sr.AudioFile(audio_file_path) as source:
                logger.debug(f"Loading audio file: {audio_file_path}")
                audio = self.recognizer.record(source)
                
                # Reconocer
                text = self.recognizer.recognize_google(
                    audio,
                    language=self.language
                )
                
                logger.info(f"Recognized from file: {text}")
                return text
                
        except sr.UnknownValueError:
            logger.warning("Could not understand audio from file")
            return None
        except sr.RequestError as e:
            logger.error(f"API request error: {e}")
            return None
        except Exception as e:
            logger.error(f"Error recognizing from file: {e}")
            return None
    
    def test_microphone(self) -> bool:
        """
        Prueba si el micrófono está funcionando.
        
        Returns:
            bool: True si el micrófono funciona
        """
        try:
            with sr.Microphone() as source:
                logger.info("Testing microphone...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                logger.info("Microphone is working!")
                return True
        except Exception as e:
            logger.error(f"Microphone test failed: {e}")
            return False
    
    def get_available_microphones(self) -> list:
        """
        Obtiene la lista de micrófonos disponibles.
        
        Returns:
            list: Lista de micrófonos
        """
        try:
            mics = sr.Microphone.list_microphone_names()
            return [
                {"index": i, "name": name}
                for i, name in enumerate(mics)
            ]
        except Exception as e:
            logger.error(f"Error getting microphones: {e}")
            return []
    
    def set_microphone(self, device_index: int):
        """
        Establece el micrófono a usar.
        
        Args:
            device_index: Índice del dispositivo de micrófono
        """
        try:
            # Verificar que el dispositivo existe
            with sr.Microphone(device_index=device_index) as source:
                logger.info(f"Microphone set to device index: {device_index}")
        except Exception as e:
            logger.error(f"Error setting microphone: {e}")
    
    def set_language(self, language_code: str):
        """
        Establece el idioma para reconocimiento.
        
        Args:
            language_code: Código de idioma (ej: 'es-ES', 'en-US')
        """
        self.language = language_code
        logger.info(f"STT language set to: {language_code}")
    
    def set_energy_threshold(self, threshold: int):
        """
        Establece el umbral de energía para detección de voz.
        
        Args:
            threshold: Umbral de energía (típico: 300-4000)
        """
        self.recognizer.energy_threshold = threshold
        logger.info(f"Energy threshold set to: {threshold}")
    
    def listen_continuous(
        self,
        callback,
        stop_event,
        timeout: int = 5,
        phrase_time_limit: int = 10
    ):
        """
        Escucha continuamente y llama al callback con cada frase reconocida.
        
        Args:
            callback: Función a llamar con el texto reconocido
            stop_event: threading.Event para detener la escucha
            timeout: Timeout para cada frase
            phrase_time_limit: Límite de tiempo por frase
        """
        if not self.enabled:
            logger.warning("STT is disabled")
            return
        
        try:
            with sr.Microphone() as source:
                logger.info("Starting continuous listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                while not stop_event.is_set():
                    try:
                        audio = self.recognizer.listen(
                            source,
                            timeout=timeout,
                            phrase_time_limit=phrase_time_limit
                        )
                        
                        # Reconocer en thread separado para no bloquear
                        text = self.recognizer.recognize_google(
                            audio,
                            language=self.language
                        )
                        
                        if text and callback:
                            callback(text)
                            
                    except sr.WaitTimeoutError:
                        continue
                    except sr.UnknownValueError:
                        logger.debug("Could not understand audio")
                        continue
                    except Exception as e:
                        logger.error(f"Error in continuous listening: {e}")
                        break
                        
        except Exception as e:
            logger.error(f"Fatal error in continuous listening: {e}")


# Singleton instance
_stt_service: Optional[STTService] = None


def get_stt_service() -> STTService:
    """
    Obtiene la instancia singleton del servicio STT.
    
    Returns:
        STTService: Instancia del servicio
    """
    global _stt_service
    
    if _stt_service is None:
        _stt_service = STTService()
    
    return _stt_service


# Para testing
if __name__ == "__main__":
    import time
    
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    stt = get_stt_service()
    
    print("Testing STT Service...")
    
    # Test 1: Verificar micrófono
    print("\n1. Testing microphone...")
    if stt.test_microphone():
        print("   ✓ Microphone is working!")
    else:
        print("   ✗ Microphone test failed!")
    
    # Test 2: Listar micrófonos
    print("\n2. Available microphones:")
    mics = stt.get_available_microphones()
    for mic in mics[:5]:  # Mostrar primeros 5
        print(f"   {mic['index']}. {mic['name']}")
    
    # Test 3: Escuchar
    print("\n3. Say something in Spanish (you have 5 seconds)...")
    print("   Listening...")
    
    text = stt.listen_from_microphone(timeout=5, phrase_time_limit=5)
    
    if text:
        print(f"   You said: '{text}'")
    else:
        print("   No speech detected or error occurred")
    
    print("\nSTT Service test completed!")
