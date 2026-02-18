"""
Maiten AI - Learn better
Avatar Widget

Widget del avatar personalizable con expresiones animadas.
"""

import logging
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap

from .styles import COLORS, AVATAR_EXPRESSIONS

logger = logging.getLogger(__name__)


class AvatarWidget(QWidget):
    """
    Widget del avatar con expresiones animadas
    """
    
    expression_changed = pyqtSignal(str)  # Signal cuando cambia la expresión
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.current_expression = "happy"
        self.is_speaking = False
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self._animate)
        
        self.init_ui()
        
        logger.info("Avatar Widget initialized")
    
    def init_ui(self):
        """Inicializa la interfaz del avatar"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Contenedor del avatar
        self.avatar_frame = QFrame()
        self.avatar_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['white']};
                border-radius: 100px;
                border: 4px solid {COLORS['primary']};
                min-width: 180px;
                max-width: 180px;
                min-height: 180px;
                max-height: 180px;
            }}
        """)
        
        avatar_layout = QVBoxLayout()
        self.avatar_frame.setLayout(avatar_layout)
        
        # Emoji del avatar (grande)
        self.avatar_emoji = QLabel(AVATAR_EXPRESSIONS[self.current_expression])
        self.avatar_emoji.setFont(QFont("Segoe UI Emoji", 80))
        self.avatar_emoji.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar_layout.addWidget(self.avatar_emoji)
        
        layout.addWidget(self.avatar_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Nombre del avatar
        self.name_label = QLabel("Maiten AI")
        self.name_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.name_label.setStyleSheet(f"color: {COLORS['primary']}; margin-top: 12px;")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.name_label)
        
        # Estado del avatar
        self.status_label = QLabel("¡Listo para ayudarte!")
        self.status_label.setFont(QFont("Segoe UI", 12))
        self.status_label.setStyleSheet(f"color: {COLORS['text_secondary']}; margin-top: 4px;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Selector de expresiones (oculto por defecto)
        self.create_expression_selector()
        
        layout.addStretch()
    
    def create_expression_selector(self):
        """Crea el selector de expresiones"""
        self.expression_container = QFrame()
        self.expression_container.setVisible(False)
        
        exp_layout = QVBoxLayout()
        self.expression_container.setLayout(exp_layout)
        
        title = QLabel("Expresiones:")
        title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {COLORS['text_primary']}; margin-top: 16px;")
        exp_layout.addWidget(title)
        
        # Grid de expresiones
        grid_layout = QHBoxLayout()
        
        for expression_name, emoji in AVATAR_EXPRESSIONS.items():
            btn = QPushButton(emoji)
            btn.setFont(QFont("Segoe UI Emoji", 20))
            btn.setFixedSize(50, 50)
            btn.setToolTip(expression_name.title())
            btn.clicked.connect(lambda checked, e=expression_name: self.set_expression(e))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['gray_100']};
                    border-radius: 25px;
                    border: 2px solid {COLORS['gray_200']};
                }}
                QPushButton:hover {{
                    background-color: {COLORS['primary_light']};
                    border-color: {COLORS['primary']};
                }}
            """)
            grid_layout.addWidget(btn)
        
        exp_layout.addLayout(grid_layout)
        
        self.layout().addWidget(self.expression_container)
    
    def set_expression(self, expression: str):
        """
        Cambia la expresión del avatar
        
        Args:
            expression: Nombre de la expresión
        """
        if expression in AVATAR_EXPRESSIONS:
            self.current_expression = expression
            self.avatar_emoji.setText(AVATAR_EXPRESSIONS[expression])
            self.expression_changed.emit(expression)
            logger.debug(f"Avatar expression changed to: {expression}")
    
    def set_status(self, status: str):
        """
        Actualiza el estado del avatar
        
        Args:
            status: Texto de estado
        """
        self.status_label.setText(status)
    
    def start_speaking_animation(self):
        """Inicia animación de hablar"""
        if not self.is_speaking:
            self.is_speaking = True
            self.previous_expression = self.current_expression
            self.animation_timer.start(500)  # Cambiar cada 500ms
            logger.debug("Speaking animation started")
    
    def stop_speaking_animation(self):
        """Detiene animación de hablar"""
        if self.is_speaking:
            self.is_speaking = False
            self.animation_timer.stop()
            self.set_expression(self.previous_expression)
            logger.debug("Speaking animation stopped")
    
    def _animate(self):
        """Animación interna para cuando habla"""
        if self.is_speaking:
            # Alternar entre expresión actual y "thinking"
            if self.current_expression == "thinking":
                self.set_expression("happy")
            else:
                self.set_expression("thinking")
    
    def show_expression_selector(self, show: bool = True):
        """Muestra u oculta el selector de expresiones"""
        self.expression_container.setVisible(show)
    
    def set_thinking(self):
        """Cambia a expresión pensando"""
        self.set_expression("thinking")
        self.set_status("Pensando...")
    
    def set_happy(self):
        """Cambia a expresión feliz"""
        self.set_expression("happy")
        self.set_status("¡Listo para ayudarte!")
    
    def set_excited(self):
        """Cambia a expresión emocionada"""
        self.set_expression("excited")
        self.set_status("¡Excelente!")
    
    def set_celebrating(self):
        """Cambia a expresión celebrando"""
        self.set_expression("celebrating")
        self.set_status("¡Muy bien!")
    
    def set_confused(self):
        """Cambia a expresión confundida"""
        self.set_expression("confused")
        self.set_status("Hmm...")


# Para testing
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    widget = AvatarWidget()
    widget.show_expression_selector(True)
    widget.show()
    
    # Test animaciones
    import time
    QTimer.singleShot(2000, widget.set_thinking)
    QTimer.singleShot(4000, widget.set_excited)
    QTimer.singleShot(6000, widget.start_speaking_animation)
    QTimer.singleShot(10000, widget.stop_speaking_animation)
    
    sys.exit(app.exec())
