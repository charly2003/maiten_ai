"""
Maiten AI - Learn better
Main Window

Ventana principal de la aplicación.
"""

import sys
import logging
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QScrollArea, QFrame, QListWidget,
    QLineEdit, QMessageBox, QSplitter
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

from .styles import GLOBAL_STYLE, COLORS, SUBJECT_ICONS
from ..logic.app_controller import get_app_controller
from ..logic.voice_manager import get_voice_manager

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    Ventana principal de Maiten AI
    """
    
    def __init__(self, user_id: int = 1):
        super().__init__()
        
        self.user_id = user_id
        self.controller = get_app_controller(user_id)
        self.voice_manager = get_voice_manager()
        self.current_session_active = False
        
        self.init_ui()
        
        logger.info("Main Window initialized")
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        self.setWindowTitle("Maiten AI - Learn better")
        self.setGeometry(100, 100, 1200, 800)
        
        # Aplicar estilos
        self.setStyleSheet(GLOBAL_STYLE)
        
        # Widget central
        central_widget = QWidget()
        self.setCentral(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Crear secciones
        self.create_sidebar()
        self.create_chat_area()
        
        # Agregar al layout
        main_layout.addWidget(self.sidebar, 1)
        main_layout.addWidget(self.chat_container, 3)
    
    def create_sidebar(self):
        """Crea la barra lateral con materias"""
        self.sidebar = QFrame()
        self.sidebar.setStyleSheet(f"background-color: {COLORS['white']}; border-radius: 12px;")
        self.sidebar.setMaximumWidth(300)
        
        layout = QVBoxLayout()
        self.sidebar.setLayout(layout)
        
        # Logo/Título
        title = QLabel("🎓 Maiten AI")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {COLORS['primary']}; padding: 16px;")
        layout.addWidget(title)
        
        subtitle = QLabel("Learn better")
        subtitle.setStyleSheet(f"color: {COLORS['text_secondary']}; padding: 0px 16px 16px 16px;")
        layout.addWidget(subtitle)
        
        # Materias
        subjects_label = QLabel("📚 Materias")
        subjects_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        subjects_label.setStyleSheet("padding: 16px;")
        layout.addWidget(subjects_label)
        
        self.subjects_list = QListWidget()
        self.load_subjects()
        self.subjects_list.itemClicked.connect(self.on_subject_selected)
        layout.addWidget(self.subjects_list)
        
        layout.addStretch()
        
        # Botón de configuración
        settings_btn = QPushButton("⚙️ Configuración")
        settings_btn.clicked.connect(self.show_settings)
        layout.addWidget(settings_btn)
    
    def create_chat_area(self):
        """Crea el área de chat"""
        self.chat_container = QFrame()
        self.chat_container.setStyleSheet(f"background-color: {COLORS['white']}; border-radius: 12px;")
        
        layout = QVBoxLayout()
        self.chat_container.setLayout(layout)
        
        # Encabezado
        header = QFrame()
        header_layout = QHBoxLayout()
        header.setLayout(header_layout)
        
        self.subject_title = QLabel("Selecciona una materia para empezar")
        self.subject_title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        header_layout.addWidget(self.subject_title)
        
        header_layout.addStretch()
        
        # Avatar
        self.avatar_label = QLabel("😊")
        self.avatar_label.setFont(QFont("Segoe UI", 32))
        header_layout.addWidget(self.avatar_label)
        
        layout.addWidget(header)
        
        # Área de mensajes
        self.messages_scroll = QScrollArea()
        self.messages_scroll.setWidgetResizable(True)
        self.messages_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.messages_widget = QWidget()
        self.messages_layout = QVBoxLayout()
        self.messages_widget.setLayout(self.messages_layout)
        self.messages_scroll.setWidget(self.messages_widget)
        
        layout.addWidget(self.messages_scroll)
        
        # Área de input
        input_frame = QFrame()
        input_layout = QHBoxLayout()
        input_frame.setLayout(input_layout)
        
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Escribe tu mensaje aquí...")
        self.message_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.message_input)
        
        self.mic_button = QPushButton("🎤")
        self.mic_button.setMaximumWidth(50)
        self.mic_button.clicked.connect(self.toggle_voice_input)
        input_layout.addWidget(self.mic_button)
        
        self.send_button = QPushButton("Enviar")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)
        
        layout.addWidget(input_frame)
    
    def load_subjects(self):
        """Carga las materias disponibles"""
        subjects = self.controller.get_subjects_list()
        
        for subject in subjects:
            icon = SUBJECT_ICONS.get(subject['name'].lower(), "📖")
            item_text = f"{icon} {subject['name']}"
            self.subjects_list.addItem(item_text)
    
    def on_subject_selected(self, item):
        """Maneja la selección de una materia"""
        subject_text = item.text()
        # Extraer nombre de la materia (después del emoji)
        subject_name = subject_text.split(" ", 1)[1] if " " in subject_text else subject_text
        
        # Iniciar sesión
        result = self.controller.start_study_session(subject_name.lower())
        
        self.current_session_active = True
        self.subject_title.setText(f"📚 {subject_name}")
        
        # Agregar mensaje de bienvenida
        self.add_assistant_message(result['greeting'])
        
        logger.info(f"Session started for subject: {subject_name}")
    
    def send_message(self):
        """Envía un mensaje del usuario"""
        message = self.message_input.text().strip()
        
        if not message:
            return
        
        if not self.current_session_active:
            QMessageBox.warning(self, "Sin sesión", "Por favor selecciona una materia primero")
            return
        
        # Mostrar mensaje del usuario
        self.add_user_message(message)
        self.message_input.clear()
        
        # Procesar mensaje
        response = self.controller.send_message(message)
        
        # Mostrar respuesta
        self.add_assistant_message(response['response'])
        
        # Hablar respuesta si está habilitado
        if self.voice_manager.tts.enabled:
            self.voice_manager.speak(response['response'])
    
    def toggle_voice_input(self):
        """Activa/desactiva entrada por voz"""
        self.mic_button.setEnabled(False)
        self.mic_button.setText("🔴")
        
        # Escuchar en thread separado
        text = self.voice_manager.listen(timeout=10)
        
        self.mic_button.setEnabled(True)
        self.mic_button.setText("🎤")
        
        if text:
            self.message_input.setText(text)
            self.send_message()
    
    def add_user_message(self, message: str):
        """Agrega mensaje del usuario al chat"""
        bubble = QLabel(message)
        bubble.setWordWrap(True)
        bubble.setStyleSheet(f"""
            background-color: {COLORS['primary']};
            color: {COLORS['white']};
            border-radius: 16px;
            padding: 12px 16px;
            margin: 4px;
        """)
        bubble.setMaximumWidth(500)
        bubble.setAlignment(Qt.AlignmentFlag.AlignRight)
        
        container = QWidget()
        container_layout = QHBoxLayout()
        container_layout.addStretch()
        container_layout.addWidget(bubble)
        container.setLayout(container_layout)
        
        self.messages_layout.addWidget(container)
        self.scroll_to_bottom()
    
    def add_assistant_message(self, message: str):
        """Agrega mensaje del asistente al chat"""
        bubble = QLabel(message)
        bubble.setWordWrap(True)
        bubble.setStyleSheet(f"""
            background-color: {COLORS['gray_100']};
            color: {COLORS['text_primary']};
            border-radius: 16px;
            padding: 12px 16px;
            margin: 4px;
        """)
        bubble.setMaximumWidth(500)
        
        container = QWidget()
        container_layout = QHBoxLayout()
        container_layout.addWidget(bubble)
        container_layout.addStretch()
        container.setLayout(container_layout)
        
        self.messages_layout.addWidget(container)
        self.scroll_to_bottom()
    
    def scroll_to_bottom(self):
        """Hace scroll al final del chat"""
        scrollbar = self.messages_scroll.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def show_settings(self):
        """Muestra configuración"""
        QMessageBox.information(self, "Configuración", "Configuración próximamente...")
    
    def closeEvent(self, event):
        """Maneja el cierre de la ventana"""
        if self.current_session_active:
            summary = self.controller.end_study_session()
            QMessageBox.information(
                self,
                "Sesión finalizada",
                f"{summary['farewell']}\n\nDuración: {summary['duration_minutes']} minutos"
            )
        event.accept()


def main():
    """Función principal"""
    import os
    from dotenv import load_dotenv
    
    # Cargar variables de entorno
    load_dotenv()
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Crear usuario si no existe
    from src.data.database import get_db_manager
    db = get_db_manager()
    
    user = db.get_user_by_name("Maitena")
    if not user:
        user = db.create_user(name="Maitena", age=9, grade_level=4)
        logger.info(f"User created: {user}")
    
    # Iniciar aplicación
    app = QApplication(sys.argv)
    window = MainWindow(user_id=user.id)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
