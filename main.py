"""
Maiten AI - Learn better
Main Entry Point

Punto de entrada principal de la aplicación.
"""

import sys
import os
import logging
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from PyQt6.QtWidgets import QApplication

from src.ui.main_window import MainWindow
from src.data.database import get_db_manager

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/maiten_ai.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def ensure_directories():
    """Asegura que existan todos los directorios necesarios"""
    directories = [
        'data',
        'data/curriculum',
        'logs',
        'assets/avatars/expressions',
        'assets/avatars/clothes',
        'assets/avatars/backgrounds',
        'assets/icons'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    logger.info("Directories verified")


def initialize_user():
    """Inicializa o carga el usuario por defecto"""
    db = get_db_manager()
    
    # Buscar usuario existente
    user = db.get_user_by_name("Maitena")
    
    if not user:
        # Crear usuario por defecto
        user = db.create_user(
            name="Maitena",
            age=9,
            grade_level=4
        )
        logger.info(f"User created: {user.name} (ID: {user.id})")
    else:
        logger.info(f"User loaded: {user.name} (ID: {user.id})")
    
    return user


def main():
    """
    Función principal de la aplicación
    """
    try:
        logger.info("="*60)
        logger.info("Starting Maiten AI - Learn better")
        logger.info("="*60)
        
        # Verificar API key
        if not os.getenv("ANTHROPIC_API_KEY"):
            logger.error("ANTHROPIC_API_KEY not found in environment variables")
            logger.error("Please set your API key in the .env file")
            sys.exit(1)
        
        # Asegurar directorios
        ensure_directories()
        
        # Inicializar usuario
        user = initialize_user()
        
        # Crear aplicación Qt
        app = QApplication(sys.argv)
        app.setApplicationName("Maiten AI")
        app.setOrganizationName("Maiten AI")
        
        # Crear y mostrar ventana principal
        window = MainWindow(user_id=user.id)
        window.show()
        
        logger.info("Application started successfully")
        
        # Ejecutar aplicación
        exit_code = app.exec()
        
        logger.info(f"Application closed with code: {exit_code}")
        return exit_code
        
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
