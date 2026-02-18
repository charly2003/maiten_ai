"""
Maiten AI - Learn better
Sidebar Widget

Barra lateral con navegación, materias y estadísticas.
"""

import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QFrame, QProgressBar
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from .styles import COLORS, SUBJECT_ICONS

logger = logging.getLogger(__name__)


class SubjectListItem(QWidget):
    """Item personalizado para la lista de materias"""
    
    def __init__(self, subject_data: dict, parent=None):
        super().__init__(parent)
        
        self.subject_data = subject_data
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la UI del item"""
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Icono
        icon = SUBJECT_ICONS.get(self.subject_data['name'].lower(), "📖")
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Segoe UI Emoji", 24))
        layout.addWidget(icon_label)
        
        # Info de la materia
        info_layout = QVBoxLayout()
        
        name_label = QLabel(self.subject_data['name'])
        name_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        name_label.setStyleSheet(f"color: {COLORS['text_primary']};")
        info_layout.addWidget(name_label)
        
        # Progreso
        if 'progress' in self.subject_data and self.subject_data['progress']:
            progress_data = self.subject_data['progress']
            mastery = progress_data.get('average_mastery', 0)
            
            progress_bar = QProgressBar()
            progress_bar.setMaximum(100)
            progress_bar.setValue(int(mastery * 100))
            progress_bar.setTextVisible(False)
            progress_bar.setMaximumHeight(6)
            progress_bar.setStyleSheet(f"""
                QProgressBar {{
                    background-color: {COLORS['gray_200']};
                    border-radius: 3px;
                }}
                QProgressBar::chunk {{
                    background-color: {COLORS['success']};
                    border-radius: 3px;
                }}
            """)
            info_layout.addWidget(progress_bar)
            
            stats_label = QLabel(f"{int(mastery * 100)}% dominado")
            stats_label.setFont(QFont("Segoe UI", 10))
            stats_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
            info_layout.addWidget(stats_label)
        
        layout.addLayout(info_layout, 1)


class SidebarWidget(QWidget):
    """
    Barra lateral con navegación y estadísticas
    """
    
    subject_selected = pyqtSignal(str)  # Materia seleccionada
    dashboard_clicked = pyqtSignal()
    settings_clicked = pyqtSignal()
    achievements_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.current_section = "subjects"
        self.init_ui()
        
        logger.info("Sidebar Widget initialized")
    
    def init_ui(self):
        """Inicializa la interfaz del sidebar"""
        self.setMaximumWidth(320)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['white']};
            }}
        """)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(16, 16, 16, 16)
        
        # Header con logo
        self.create_header()
        layout.addWidget(self.header_frame)
        
        # Navegación
        self.create_navigation()
        layout.addWidget(self.nav_frame)
        
        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet(f"background-color: {COLORS['gray_200']};")
        layout.addWidget(separator)
        
        # Materias
        self.create_subjects_list()
        layout.addWidget(self.subjects_frame, 1)
        
        # Estadísticas rápidas
        self.create_stats()
        layout.addWidget(self.stats_frame)
        
        layout.addStretch()
        
        # Botones inferiores
        self.create_bottom_buttons()
        layout.addWidget(self.bottom_frame)
    
    def create_header(self):
        """Crea el header con logo"""
        self.header_frame = QFrame()
        layout = QVBoxLayout()
        self.header_frame.setLayout(layout)
        
        # Logo
        logo = QLabel("🎓")
        logo.setFont(QFont("Segoe UI Emoji", 48))
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo)
        
        # Título
        title = QLabel("Maiten AI")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {COLORS['primary']};")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Tagline
        tagline = QLabel("Learn better")
        tagline.setFont(QFont("Segoe UI", 12))
        tagline.setStyleSheet(f"color: {COLORS['text_secondary']};")
        tagline.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(tagline)
    
    def create_navigation(self):
        """Crea los botones de navegación"""
        self.nav_frame = QFrame()
        layout = QVBoxLayout()
        self.nav_frame.setLayout(layout)
        layout.setContentsMargins(0, 16, 0, 16)
        
        # Botón Dashboard
        self.dashboard_btn = self.create_nav_button("📊", "Dashboard")
        self.dashboard_btn.clicked.connect(self.dashboard_clicked.emit)
        layout.addWidget(self.dashboard_btn)
        
        # Botón Logros
        self.achievements_btn = self.create_nav_button("🏆", "Logros")
        self.achievements_btn.clicked.connect(self.achievements_clicked.emit)
        layout.addWidget(self.achievements_btn)
    
    def create_nav_button(self, icon: str, text: str) -> QPushButton:
        """Crea un botón de navegación"""
        btn = QPushButton(f"{icon}  {text}")
        btn.setFont(QFont("Segoe UI", 12))
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {COLORS['text_primary']};
                text-align: left;
                padding: 12px 16px;
                border: none;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['gray_100']};
            }}
            QPushButton:pressed {{
                background-color: {COLORS['gray_200']};
            }}
        """)
        return btn
    
    def create_subjects_list(self):
        """Crea la lista de materias"""
        self.subjects_frame = QFrame()
        layout = QVBoxLayout()
        self.subjects_frame.setLayout(layout)
        
        # Título
        title = QLabel("📚 Materias")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {COLORS['text_primary']}; margin-bottom: 8px;")
        layout.addWidget(title)
        
        # Lista
        self.subjects_list = QListWidget()
        self.subjects_list.setStyleSheet(f"""
            QListWidget {{
                background-color: transparent;
                border: none;
                outline: none;
            }}
            QListWidget::item {{
                background-color: {COLORS['gray_50']};
                border-radius: 8px;
                margin: 4px 0px;
                padding: 4px;
            }}
            QListWidget::item:hover {{
                background-color: {COLORS['gray_100']};
            }}
            QListWidget::item:selected {{
                background-color: {COLORS['primary_light']};
            }}
        """)
        self.subjects_list.itemClicked.connect(self._on_subject_clicked)
        layout.addWidget(self.subjects_list)
    
    def create_stats(self):
        """Crea las estadísticas rápidas"""
        self.stats_frame = QFrame()
        self.stats_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['gray_50']};
                border-radius: 12px;
                padding: 12px;
            }}
        """)
        
        layout = QVBoxLayout()
        self.stats_frame.setLayout(layout)
        
        title = QLabel("📈 Esta Semana")
        title.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Tiempo de estudio
        self.time_label = QLabel("⏱️ 0 minutos")
        self.time_label.setFont(QFont("Segoe UI", 10))
        self.time_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(self.time_label)
        
        # Puntos
        self.points_label = QLabel("⭐ 0 puntos")
        self.points_label.setFont(QFont("Segoe UI", 10))
        self.points_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(self.points_label)
    
    def create_bottom_buttons(self):
        """Crea botones inferiores"""
        self.bottom_frame = QFrame()
        layout = QHBoxLayout()
        self.bottom_frame.setLayout(layout)
        
        # Botón Configuración
        settings_btn = QPushButton("⚙️")
        settings_btn.setFixedSize(40, 40)
        settings_btn.setToolTip("Configuración")
        settings_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['gray_100']};
                border-radius: 20px;
                font-size: 18px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {COLORS['gray_200']};
            }}
        """)
        settings_btn.clicked.connect(self.settings_clicked.emit)
        layout.addWidget(settings_btn)
        
        layout.addStretch()
        
        # Usuario
        user_label = QLabel("👤 Maitena")
        user_label.setFont(QFont("Segoe UI", 11))
        user_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        layout.addWidget(user_label)
    
    def load_subjects(self, subjects: list):
        """Carga las materias en la lista"""
        self.subjects_list.clear()
        
        for subject in subjects:
            item = QListWidgetItem(self.subjects_list)
            widget = SubjectListItem(subject)
            item.setSizeHint(widget.sizeHint())
            self.subjects_list.setItemWidget(item, widget)
            item.setData(Qt.ItemDataRole.UserRole, subject['name'])
        
        logger.debug(f"Loaded {len(subjects)} subjects")
    
    def _on_subject_clicked(self, item):
        """Maneja el click en una materia"""
        subject_name = item.data(Qt.ItemDataRole.UserRole)
        self.subject_selected.emit(subject_name)
        logger.debug(f"Subject selected: {subject_name}")
    
    def update_stats(self, time_minutes: int, points: int):
        """Actualiza las estadísticas"""
        self.time_label.setText(f"⏱️ {time_minutes} minutos")
        self.points_label.setText(f"⭐ {points} puntos")
