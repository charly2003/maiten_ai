"""
Maiten AI - Learn better
Chat Widget

Widget de chat con burbujas, typing indicator y funcionalidades avanzadas.
"""

import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea,
    QFrame, QTextEdit, QPushButton, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QPoint
from PyQt6.QtGui import QFont, QTextCursor

from .styles import COLORS

logger = logging.getLogger(__name__)


class MessageBubble(QFrame):
    """Burbuja individual de mensaje"""
    
    def __init__(self, message: str, is_user: bool, parent=None):
        super().__init__(parent)
        
        self.is_user = is_user
        self.init_ui(message)
    
    def init_ui(self, message: str):
        """Inicializa la burbuja"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(12, 8, 12, 8)
        
        # Label del mensaje
        self.message_label = QLabel(message)
        self.message_label.setWordWrap(True)
        self.message_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self.message_label.setFont(QFont("Segoe UI", 13))
        
        if self.is_user:
            self.setStyleSheet(f"""
                QFrame {{
                    background-color: {COLORS['primary']};
                    border-radius: 18px;
                    border-bottom-right-radius: 4px;
                }}
                QLabel {{
                    color: {COLORS['white']};
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QFrame {{
                    background-color: {COLORS['gray_100']};
                    border-radius: 18px;
                    border-bottom-left-radius: 4px;
                }}
                QLabel {{
                    color: {COLORS['text_primary']};
                }}
            """)
        
        self.setMaximumWidth(500)
        layout.addWidget(self.message_label)


class TypingIndicator(QFrame):
    """Indicador de que el asistente está escribiendo"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['gray_100']};
                border-radius: 18px;
                padding: 12px 16px;
            }}
        """)
        self.setMaximumWidth(80)
        
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        # Tres puntos animados
        self.dots = []
        for i in range(3):
            dot = QLabel("●")
            dot.setFont(QFont("Segoe UI", 16))
            dot.setStyleSheet(f"color: {COLORS['gray_400']};")
            self.dots.append(dot)
            layout.addWidget(dot)
        
        # Timer para animación
        self.animation_step = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self._animate)
        self.timer.start(400)
    
    def _animate(self):
        """Anima los puntos"""
        for i, dot in enumerate(self.dots):
            if i == self.animation_step % 3:
                dot.setStyleSheet(f"color: {COLORS['primary']};")
            else:
                dot.setStyleSheet(f"color: {COLORS['gray_400']};")
        
        self.animation_step += 1
    
    def stop(self):
        """Detiene la animación"""
        self.timer.stop()


class ChatWidget(QWidget):
    """
    Widget de chat completo con funcionalidades avanzadas
    """
    
    message_sent = pyqtSignal(str)  # Cuando se envía un mensaje
    voice_requested = pyqtSignal()  # Cuando se solicita entrada por voz
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.messages = []
        self.typing_indicator = None
        
        self.init_ui()
        
        logger.info("Chat Widget initialized")
    
    def init_ui(self):
        """Inicializa la interfaz del chat"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Área de mensajes con scroll
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {COLORS['bg_secondary']};
            }}
        """)
        
        # Widget contenedor de mensajes
        self.messages_widget = QWidget()
        self.messages_layout = QVBoxLayout()
        self.messages_layout.addStretch()
        self.messages_widget.setLayout(self.messages_layout)
        
        self.scroll_area.setWidget(self.messages_widget)
        layout.addWidget(self.scroll_area)
        
        # Área de input
        self.create_input_area()
        layout.addWidget(self.input_frame)
    
    def create_input_area(self):
        """Crea el área de entrada de mensajes"""
        self.input_frame = QFrame()
        self.input_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['white']};
                border-top: 2px solid {COLORS['gray_200']};
                padding: 12px;
            }}
        """)
        
        input_layout = QHBoxLayout()
        self.input_frame.setLayout(input_layout)
        
        # Campo de texto
        self.message_input = QTextEdit()
        self.message_input.setPlaceholderText("Escribe tu mensaje aquí...")
        self.message_input.setMaximumHeight(100)
        self.message_input.setStyleSheet(f"""
            QTextEdit {{
                background-color: {COLORS['white']};
                border: 2px solid {COLORS['gray_200']};
                border-radius: 20px;
                padding: 10px 16px;
                font-size: 14px;
            }}
            QTextEdit:focus {{
                border-color: {COLORS['primary']};
            }}
        """)
        
        # Detectar Enter para enviar
        self.message_input.installEventFilter(self)
        
        input_layout.addWidget(self.message_input)
        
        # Botones
        buttons_layout = QVBoxLayout()
        
        # Botón de micrófono
        self.mic_button = QPushButton("🎤")
        self.mic_button.setFixedSize(50, 50)
        self.mic_button.setToolTip("Entrada por voz")
        self.mic_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['secondary']};
                color: {COLORS['white']};
                border-radius: 25px;
                font-size: 20px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #3B82F6;
            }}
            QPushButton:pressed {{
                background-color: #2563EB;
            }}
        """)
        self.mic_button.clicked.connect(self.voice_requested.emit)
        
        # Botón de enviar
        self.send_button = QPushButton("➤")
        self.send_button.setFixedSize(50, 50)
        self.send_button.setToolTip("Enviar mensaje")
        self.send_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['primary']};
                color: {COLORS['white']};
                border-radius: 25px;
                font-size: 20px;
                font-weight: bold;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary_dark']};
            }}
            QPushButton:disabled {{
                background-color: {COLORS['gray_300']};
            }}
        """)
        self.send_button.clicked.connect(self.send_message)
        
        buttons_layout.addWidget(self.mic_button)
        buttons_layout.addWidget(self.send_button)
        buttons_layout.addStretch()
        
        input_layout.addLayout(buttons_layout)
    
    def eventFilter(self, obj, event):
        """Filtro de eventos para detectar Enter"""
        if obj == self.message_input and event.type() == event.Type.KeyPress:
            if event.key() == Qt.Key.Key_Return and not event.modifiers():
                self.send_message()
                return True
        return super().eventFilter(obj, event)
    
    def send_message(self):
        """Envía un mensaje"""
        message = self.message_input.toPlainText().strip()
        
        if message:
            self.add_user_message(message)
            self.message_input.clear()
            self.message_sent.emit(message)
            logger.debug(f"Message sent: {message[:50]}...")
    
    def add_user_message(self, message: str):
        """Agrega un mensaje del usuario"""
        bubble = MessageBubble(message, is_user=True)
        
        # Contenedor para alinear a la derecha
        container = QWidget()
        container_layout = QHBoxLayout()
        container_layout.setContentsMargins(40, 4, 8, 4)
        container_layout.addStretch()
        container_layout.addWidget(bubble)
        container.setLayout(container_layout)
        
        # Insertar antes del stretch
        count = self.messages_layout.count()
        self.messages_layout.insertWidget(count - 1, container)
        
        self.messages.append({"role": "user", "content": message, "widget": container})
        self.scroll_to_bottom()
    
    def add_assistant_message(self, message: str):
        """Agrega un mensaje del asistente"""
        # Remover typing indicator si existe
        self.hide_typing_indicator()
        
        bubble = MessageBubble(message, is_user=False)
        
        # Contenedor para alinear a la izquierda
        container = QWidget()
        container_layout = QHBoxLayout()
        container_layout.setContentsMargins(8, 4, 40, 4)
        container_layout.addWidget(bubble)
        container_layout.addStretch()
        container.setLayout(container_layout)
        
        # Insertar antes del stretch
        count = self.messages_layout.count()
        self.messages_layout.insertWidget(count - 1, container)
        
        self.messages.append({"role": "assistant", "content": message, "widget": container})
        self.scroll_to_bottom()
    
    def show_typing_indicator(self):
        """Muestra el indicador de escritura"""
        if self.typing_indicator is None:
            self.typing_indicator = TypingIndicator()
            
            container = QWidget()
            container_layout = QHBoxLayout()
            container_layout.setContentsMargins(8, 4, 40, 4)
            container_layout.addWidget(self.typing_indicator)
            container_layout.addStretch()
            container.setLayout(container_layout)
            
            count = self.messages_layout.count()
            self.messages_layout.insertWidget(count - 1, container)
            
            self.scroll_to_bottom()
    
    def hide_typing_indicator(self):
        """Oculta el indicador de escritura"""
        if self.typing_indicator:
            self.typing_indicator.stop()
            parent = self.typing_indicator.parent()
            if parent:
                self.messages_layout.removeWidget(parent)
                parent.deleteLater()
            self.typing_indicator = None
    
    def scroll_to_bottom(self):
        """Hace scroll hasta el final"""
        QTimer.singleShot(100, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        ))
    
    def clear_chat(self):
        """Limpia todos los mensajes"""
        while self.messages:
            msg = self.messages.pop()
            widget = msg["widget"]
            self.messages_layout.removeWidget(widget)
            widget.deleteLater()
        
        self.hide_typing_indicator()
        logger.info("Chat cleared")
    
    def get_message_history(self) -> list:
        """Obtiene el historial de mensajes"""
        return [{"role": msg["role"], "content": msg["content"]} for msg in self.messages]
    
    def set_input_enabled(self, enabled: bool):
        """Habilita o deshabilita el input"""
        self.message_input.setEnabled(enabled)
        self.send_button.setEnabled(enabled)
        self.mic_button.setEnabled(enabled)
