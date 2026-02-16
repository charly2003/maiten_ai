# 📂 Estructura Detallada del Proyecto

## Árbol de Directorios Completo

```
asistente_maitena/
│
├── 📄 main.py                      # Punto de entrada principal
├── 📄 requirements.txt             # Dependencias del proyecto
├── 📄 .env.example                 # Plantilla de variables de entorno
├── 📄 .gitignore                   # Archivos a ignorar en git
├── 📄 README.md                    # Documentación principal
├── 📄 ESTRUCTURA.md                # Este archivo
├── 📄 setup.py                     # Script de instalación
│
├── 📁 src/                         # Código fuente
│   ├── 📄 __init__.py
│   │
│   ├── 📁 ui/                      # 🎨 Capa de Interfaz de Usuario
│   │   ├── 📄 __init__.py
│   │   ├── 📄 main_window.py       # Ventana principal de la app
│   │   ├── 📄 avatar_widget.py     # Widget animado del avatar
│   │   ├── 📄 chat_widget.py       # Widget de conversación
│   │   ├── 📄 subject_selector.py  # Selector de materias
│   │   ├── 📄 customization_panel.py # Panel de personalización
│   │   └── 📄 styles.py            # Estilos y temas
│   │
│   ├── 📁 logic/                   # ⚙️ Capa de Lógica de Negocio
│   │   ├── 📄 __init__.py
│   │   ├── 📄 app_controller.py    # Controlador principal de la app
│   │   ├── 📄 session_manager.py   # Gestión de sesiones y contexto
│   │   ├── 📄 subject_manager.py   # Gestión de contenido por materia
│   │   └── 📄 voice_manager.py     # Coordinador de servicios de voz
│   │
│   ├── 📁 ai/                      # 🤖 Capa de Inteligencia Artificial
│   │   ├── 📄 __init__.py
│   │   ├── 📄 ai_agent.py          # Agente educativo principal
│   │   ├── 📄 prompt_engine.py     # Generador de prompts
│   │   ├── 📄 content_adapter.py   # Adaptador de nivel educativo
│   │   └── 📄 safety_filter.py     # Filtro de contenido seguro
│   │
│   ├── 📁 data/                    # 💾 Capa de Datos
│   │   ├── 📄 __init__.py
│   │   ├── 📄 database.py          # Gestor de base de datos SQLite
│   │   ├── 📄 models.py            # Modelos ORM (Usuario, Sesión, etc.)
│   │   └── 📄 content_loader.py    # Cargador de contenido curricular
│   │
│   └── 📁 services/                # 🌐 Servicios Externos
│       ├── 📄 __init__.py
│       ├── 📄 tts_service.py       # Servicio Text-to-Speech
│       ├── 📄 stt_service.py       # Servicio Speech-to-Text
│       └── 📄 api_client.py        # Cliente para Anthropic API
│
├── 📁 assets/                      # 🎨 Recursos Multimedia
│   ├── 📁 avatars/
│   │   ├── 📁 expressions/         # Expresiones faciales (PNG)
│   │   │   ├── happy.png
│   │   │   ├── thinking.png
│   │   │   ├── excited.png
│   │   │   ├── confused.png
│   │   │   └── neutral.png
│   │   │
│   │   ├── 📁 clothes/             # Ropa y accesorios (PNG)
│   │   │   ├── dress_blue.png
│   │   │   ├── dress_pink.png
│   │   │   ├── tshirt_green.png
│   │   │   └── accessories.png
│   │   │
│   │   └── 📁 backgrounds/         # Fondos para el avatar
│   │       ├── classroom.png
│   │       ├── library.png
│   │       └── outdoor.png
│   │
│   └── 📁 icons/                   # Iconos de la aplicación
│       ├── app_icon.png
│       ├── mic_on.png
│       ├── mic_off.png
│       └── subject_icons/
│           ├── math.png
│           ├── language.png
│           ├── science.png
│           └── social.png
│
├── 📁 config/                      # ⚙️ Configuración
│   ├── 📄 settings.yaml            # Configuración general de la app
│   ├── 📄 subjects.yaml            # Definición de materias y temas
│   └── 📄 prompts.yaml             # Templates de prompts para IA
│
├── 📁 data/                        # 📊 Datos Persistentes
│   ├── 📄 user_profile.db          # Base de datos SQLite
│   └── 📁 curriculum/              # Contenido curricular
│       ├── 📄 matematicas.json     # Temas de matemáticas
│       ├── 📄 lengua.json          # Temas de lengua
│       ├── 📄 ciencias.json        # Temas de ciencias
│       └── 📄 sociales.json        # Temas de sociales
│
├── 📁 logs/                        # 📝 Archivos de Log
│   └── app.log                     # Log principal de la aplicación
│
├── 📁 tests/                       # 🧪 Tests Unitarios
│   ├── 📄 __init__.py
│   ├── 📄 test_ai.py               # Tests de módulos IA
│   ├── 📄 test_logic.py            # Tests de lógica de negocio
│   ├── 📄 test_ui.py               # Tests de interfaz
│   └── 📄 test_services.py         # Tests de servicios
│
└── 📁 docs/                        # 📚 Documentación
    ├── 📄 arquitectura.md          # Arquitectura del sistema
    ├── 📄 guia_usuario.md          # Guía de usuario
    ├── 📄 api_reference.md         # Referencia de API
    └── 📄 desarrollo.md            # Guía para desarrolladores
```

## 📦 Descripción de Cada Módulo

### 🎨 UI Layer (src/ui/)
- **main_window.py**: Ventana principal que contiene todos los widgets
- **avatar_widget.py**: Dibuja y anima el avatar con expresiones
- **chat_widget.py**: Área de conversación con burbujas de mensajes
- **subject_selector.py**: Botones para elegir materias
- **customization_panel.py**: Panel para personalizar el avatar

### ⚙️ Logic Layer (src/logic/)
- **app_controller.py**: Orquesta toda la aplicación
- **session_manager.py**: Mantiene contexto de conversación
- **subject_manager.py**: Carga y gestiona contenido educativo
- **voice_manager.py**: Coordina TTS y STT

### 🤖 AI Layer (src/ai/)
- **ai_agent.py**: Interfaz con Claude API
- **prompt_engine.py**: Genera prompts contextuales
- **content_adapter.py**: Adapta respuestas al nivel de 9 años
- **safety_filter.py**: Valida contenido apropiado

### 💾 Data Layer (src/data/)
- **database.py**: Conexión y operaciones de BD
- **models.py**: Definición de tablas (User, Session, Progress)
- **content_loader.py**: Lee archivos JSON de contenido

### 🌐 Services Layer (src/services/)
- **tts_service.py**: Convierte texto a voz
- **stt_service.py**: Convierte voz a texto
- **api_client.py**: Cliente HTTP para Claude

## 🔄 Flujo de Datos

```
Usuario (Maitena)
    ↓
main_window.py → chat_widget.py
    ↓
app_controller.py
    ↓
session_manager.py → subject_manager.py
    ↓
ai_agent.py → prompt_engine.py
    ↓
api_client.py → Claude API
    ↓
content_adapter.py → safety_filter.py
    ↓
session_manager.py (guarda en BD)
    ↓
avatar_widget.py (muestra respuesta)
    ↓
tts_service.py (lee en voz alta)
    ↓
Usuario (Maitena)
```

## 🚀 Próximos Pasos

1. ✅ Estructura de carpetas creada
2. ⏳ Implementar módulos de datos
3. ⏳ Desarrollar capa de IA
4. ⏳ Construir interfaz de usuario
5. ⏳ Integrar servicios de voz
6. ⏳ Testing y pulido
7. ⏳ Deployment

---

**Estado actual**: Estructura base completa ✅
