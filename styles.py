"""
Maiten AI - Learn better
UI Styles

Estilos, colores y temas para la interfaz de usuario.
"""

# Paleta de colores de Maiten AI
COLORS = {
    # Colores principales
    "primary": "#8B5CF6",          # Morado principal
    "primary_dark": "#7C3AED",     # Morado oscuro
    "primary_light": "#A78BFA",    # Morado claro
    
    # Colores secundarios
    "secondary": "#60A5FA",        # Azul cielo
    "success": "#34D399",          # Verde éxito
    "warning": "#FBBF24",          # Amarillo
    "error": "#F87171",            # Rojo suave
    "info": "#FB923C",             # Naranja
    
    # Colores neutros
    "white": "#FFFFFF",
    "gray_50": "#F9FAFB",
    "gray_100": "#F3F4F6",
    "gray_200": "#E5E7EB",
    "gray_300": "#D1D5DB",
    "gray_400": "#9CA3AF",
    "gray_500": "#6B7280",
    "gray_600": "#4B5563",
    "gray_700": "#374151",
    "gray_800": "#1F2937",
    "gray_900": "#111827",
    
    # Colores de fondo
    "bg_primary": "#FFFFFF",
    "bg_secondary": "#F9FAFB",
    "bg_accent": "#F3F4F6",
    
    # Colores de texto
    "text_primary": "#111827",
    "text_secondary": "#6B7280",
    "text_on_primary": "#FFFFFF",
}


# Estilos globales de la aplicación
GLOBAL_STYLE = f"""
QWidget {{
    font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
    font-size: 14px;
    color: {COLORS['text_primary']};
}}

QMainWindow {{
    background-color: {COLORS['bg_secondary']};
}}

/* Botones principales */
QPushButton {{
    background-color: {COLORS['primary']};
    color: {COLORS['text_on_primary']};
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-weight: 600;
    font-size: 14px;
}}

QPushButton:hover {{
    background-color: {COLORS['primary_dark']};
}}

QPushButton:pressed {{
    background-color: {COLORS['primary_dark']};
}}

QPushButton:disabled {{
    background-color: {COLORS['gray_300']};
    color: {COLORS['gray_500']};
}}

/* Botones secundarios */
QPushButton[class="secondary"] {{
    background-color: {COLORS['white']};
    color: {COLORS['primary']};
    border: 2px solid {COLORS['primary']};
}}

QPushButton[class="secondary"]:hover {{
    background-color: {COLORS['gray_50']};
}}

/* Botones de éxito */
QPushButton[class="success"] {{
    background-color: {COLORS['success']};
}}

QPushButton[class="success"]:hover {{
    background-color: #10B981;
}}

/* Campos de texto */
QLineEdit, QTextEdit {{
    background-color: {COLORS['white']};
    border: 2px solid {COLORS['gray_200']};
    border-radius: 8px;
    padding: 10px 12px;
    font-size: 14px;
}}

QLineEdit:focus, QTextEdit:focus {{
    border-color: {COLORS['primary']};
    outline: none;
}}

/* Scroll bars */
QScrollBar:vertical {{
    background: {COLORS['gray_100']};
    width: 12px;
    border-radius: 6px;
}}

QScrollBar::handle:vertical {{
    background: {COLORS['gray_400']};
    border-radius: 6px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background: {COLORS['gray_500']};
}}

/* Labels */
QLabel {{
    color: {COLORS['text_primary']};
}}

QLabel[class="title"] {{
    font-size: 24px;
    font-weight: 700;
    color: {COLORS['primary']};
}}

QLabel[class="subtitle"] {{
    font-size: 18px;
    font-weight: 600;
    color: {COLORS['text_primary']};
}}

QLabel[class="caption"] {{
    font-size: 12px;
    color: {COLORS['text_secondary']};
}}

/* Cards */
QFrame[class="card"] {{
    background-color: {COLORS['white']};
    border-radius: 12px;
    border: 1px solid {COLORS['gray_200']};
    padding: 16px;
}}

/* Lista de materias */
QListWidget {{
    background-color: {COLORS['white']};
    border: 2px solid {COLORS['gray_200']};
    border-radius: 8px;
    padding: 8px;
}}

QListWidget::item {{
    padding: 12px;
    border-radius: 6px;
    margin: 4px 0px;
}}

QListWidget::item:hover {{
    background-color: {COLORS['gray_50']};
}}

QListWidget::item:selected {{
    background-color: {COLORS['primary_light']};
    color: {COLORS['white']};
}}

/* Progress bar */
QProgressBar {{
    background-color: {COLORS['gray_200']};
    border-radius: 6px;
    height: 12px;
    text-align: center;
}}

QProgressBar::chunk {{
    background-color: {COLORS['success']};
    border-radius: 6px;
}}

/* ComboBox */
QComboBox {{
    background-color: {COLORS['white']};
    border: 2px solid {COLORS['gray_200']};
    border-radius: 8px;
    padding: 8px 12px;
}}

QComboBox:hover {{
    border-color: {COLORS['primary']};
}}

QComboBox::drop-down {{
    border: none;
}}

/* Menu */
QMenu {{
    background-color: {COLORS['white']};
    border: 1px solid {COLORS['gray_200']};
    border-radius: 8px;
    padding: 4px;
}}

QMenu::item {{
    padding: 8px 16px;
    border-radius: 4px;
}}

QMenu::item:selected {{
    background-color: {COLORS['primary_light']};
    color: {COLORS['white']};
}}
"""


# Estilo para burbujas de chat
CHAT_BUBBLE_USER = f"""
    background-color: {COLORS['primary']};
    color: {COLORS['white']};
    border-radius: 16px;
    padding: 12px 16px;
    margin: 4px;
    max-width: 70%;
    font-size: 14px;
"""

CHAT_BUBBLE_ASSISTANT = f"""
    background-color: {COLORS['gray_100']};
    color: {COLORS['text_primary']};
    border-radius: 16px;
    padding: 12px 16px;
    margin: 4px;
    max-width: 70%;
    font-size: 14px;
"""


# Iconos de materias (emojis)
SUBJECT_ICONS = {
    "matematicas": "🔢",
    "lengua": "📖",
    "ciencias": "🔬",
    "sociales": "🌍",
    "arte": "🎨",
    "educacion_fisica": "🏃"
}


# Expresiones del avatar
AVATAR_EXPRESSIONS = {
    "happy": "😊",
    "thinking": "🤔",
    "excited": "🤩",
    "confused": "😕",
    "celebrating": "🎉",
    "neutral": "😐"
}


def get_button_style(variant="primary", size="medium"):
    """
    Obtiene el estilo para un botón.
    
    Args:
        variant: primary, secondary, success, warning, error
        size: small, medium, large
        
    Returns:
        str: Estilo CSS
    """
    sizes = {
        "small": "padding: 8px 16px; font-size: 12px;",
        "medium": "padding: 12px 24px; font-size: 14px;",
        "large": "padding: 16px 32px; font-size: 16px;"
    }
    
    variants = {
        "primary": f"background-color: {COLORS['primary']}; color: {COLORS['white']};",
        "secondary": f"background-color: {COLORS['white']}; color: {COLORS['primary']}; border: 2px solid {COLORS['primary']};",
        "success": f"background-color: {COLORS['success']}; color: {COLORS['white']};",
        "warning": f"background-color: {COLORS['warning']}; color: {COLORS['gray_900']};",
        "error": f"background-color: {COLORS['error']}; color: {COLORS['white']};"
    }
    
    return f"""
        {variants.get(variant, variants['primary'])}
        {sizes.get(size, sizes['medium'])}
        border-radius: 8px;
        font-weight: 600;
        border: none;
    """


def get_card_style(elevated=False):
    """
    Obtiene el estilo para una tarjeta.
    
    Args:
        elevated: Si True, agrega sombra
        
    Returns:
        str: Estilo CSS
    """
    shadow = "box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);" if elevated else ""
    
    return f"""
        background-color: {COLORS['white']};
        border-radius: 12px;
        border: 1px solid {COLORS['gray_200']};
        padding: 16px;
        {shadow}
    """
