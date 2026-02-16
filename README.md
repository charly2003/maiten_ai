# 🎓 Asistente Educativo IA para Maitena

Aplicación de escritorio en Python con un agente de IA que ayuda a Maitena (9 años) en todas sus materias escolares. Incluye un avatar personalizable y soporte de voz.

## 📁 Estructura del Proyecto

```
asistente_maitena/
├── src/                          # Código fuente principal
│   ├── ui/                       # Interfaz de usuario
│   │   ├── main_window.py        # Ventana principal
│   │   ├── avatar_widget.py      # Widget del avatar
│   │   ├── chat_widget.py        # Widget del chat
│   │   ├── subject_selector.py   # Selector de materias
│   │   └── customization_panel.py # Panel de personalización
│   │
│   ├── logic/                    # Lógica de negocio
│   │   ├── app_controller.py     # Controlador principal
│   │   ├── session_manager.py    # Gestión de sesiones
│   │   ├── subject_manager.py    # Gestión de materias
│   │   └── voice_manager.py      # Gestión de voz
│   │
│   ├── ai/                       # Inteligencia artificial
│   │   ├── ai_agent.py           # Agente educativo
│   │   ├── prompt_engine.py      # Motor de prompts
│   │   ├── content_adapter.py    # Adaptador de contenido
│   │   └── safety_filter.py      # Filtro de seguridad
│   │
│   ├── data/                     # Capa de datos
│   │   ├── database.py           # Gestión de base de datos
│   │   ├── models.py             # Modelos de datos
│   │   └── content_loader.py     # Cargador de contenido
│   │
│   └── services/                 # Servicios externos
│       ├── tts_service.py        # Text-to-Speech
│       ├── stt_service.py        # Speech-to-Text
│       └── api_client.py         # Cliente API Claude
│
├── assets/                       # Recursos visuales y multimedia
│   ├── avatars/                  # Imágenes del avatar
│   │   ├── expressions/          # Expresiones faciales
│   │   ├── clothes/              # Ropa y accesorios
│   │   └── backgrounds/          # Fondos
│   └── icons/                    # Iconos de la aplicación
│
├── config/                       # Archivos de configuración
│   ├── settings.yaml             # Configuración general
│   ├── subjects.yaml             # Definición de materias
│   └── prompts.yaml              # Templates de prompts
│
├── data/                         # Datos persistentes
│   ├── user_profile.db           # Base de datos SQLite
│   └── curriculum/               # Contenido curricular
│       ├── matematicas.json
│       ├── lengua.json
│       └── ciencias.json
│
├── logs/                         # Archivos de log
│
├── tests/                        # Tests unitarios
│   ├── test_ai.py
│   ├── test_logic.py
│   └── test_ui.py
│
├── docs/                         # Documentación
│   ├── arquitectura.md
│   ├── guia_usuario.md
│   └── api_reference.md
│
├── main.py                       # Punto de entrada de la aplicación
├── requirements.txt              # Dependencias Python
├── .env.example                  # Ejemplo de variables de entorno
├── setup.py                      # Script de instalación
└── README.md                     # Este archivo
```

## 🚀 Características Principales

### ✨ Interfaz de Usuario
- Ventana principal amigable para niños
- Avatar personalizable con múltiples expresiones
- Chat interactivo con burbujas de diálogo
- Selector visual de materias
- Tema colorido y atractivo

### 🤖 Inteligencia Artificial
- Agente educativo basado en Claude API
- Explicaciones adaptadas para niña de 9 años
- Práctica interactiva en todas las materias
- Filtro de seguridad para contenido apropiado

### 🎤 Funcionalidades de Voz
- Text-to-Speech (el asistente habla)
- Speech-to-Text (Maitena puede hablar)
- Voces naturales y amigables

### 📊 Seguimiento de Progreso
- Historial de conversaciones
- Estadísticas de aprendizaje
- Sistema de logros y recompensas
- Reportes de progreso por materia

## 🛠️ Stack Tecnológico

- **Lenguaje**: Python 3.10+
- **UI Framework**: PyQt6 / CustomTkinter
- **IA**: Anthropic Claude API
- **Base de Datos**: SQLite + SQLAlchemy
- **Voz**: pyttsx3, SpeechRecognition
- **Gráficos**: Pillow, pygame

## 📦 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tuusuario/asistente_maitena.git
cd asistente_maitena

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env y añadir tu API key de Claude

# Ejecutar la aplicación
python main.py
```

## 🎯 Uso

1. **Iniciar la aplicación**: Ejecuta `python main.py`
2. **Personalizar avatar**: Click en el botón de personalización
3. **Seleccionar materia**: Elige matemáticas, lengua, ciencias, etc.
4. **Empezar a aprender**: Haz preguntas o solicita práctica
5. **Usar voz** (opcional): Click en el micrófono para hablar

## 📚 Materias Soportadas

- 🔢 **Matemáticas**: Operaciones, fracciones, geometría
- 📖 **Lengua**: Gramática, lectura, escritura
- 🔬 **Ciencias Naturales**: Biología, física básica
- 🌍 **Ciencias Sociales**: Geografía, historia
- 🎨 **Arte**: Creatividad y expresión
- 🏃 **Educación Física**: Salud y bienestar

## 🔒 Seguridad y Privacidad

- Todos los datos se almacenan localmente
- Filtro de contenido apropiado para menores
- Sin recopilación de datos personales
- Supervisión parental recomendada

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto para uso educativo.

## 👨‍💻 Autor

Desarrollado con ❤️ para Maitena

---

**Versión**: 1.0.0  
**Última actualización**: Febrero 2026
