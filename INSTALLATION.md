# 📦 Guía de Instalación - Maiten AI

## ✅ Requisitos Previos

- **Python 3.10+** instalado
- **pip** actualizado
- **Cuenta Anthropic** con API Key ([obtener aquí](https://console.anthropic.com/))

---

## 🚀 Instalación Paso a Paso

### 1. Clonar el Repositorio

```bash
git clone https://github.com/charly2003/maiten_ai.git
cd maiten_ai
```

### 2. Crear Entorno Virtual

#### Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\activate
```

#### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Nota para Linux/macOS:** Si tienes problemas con `pip`, usa:
```bash
pip install -r requirements.txt --break-system-packages
```

### 4. Configurar Variables de Entorno

1. Copiar el archivo de ejemplo:
```bash
cp .env.example .env
```

2. Editar `.env` y agregar tu API key:
```env
ANTHROPIC_API_KEY=tu_api_key_de_anthropic_aqui
```

### 5. Crear Estructura de Datos

Los directorios se crean automáticamente, pero asegúrate de tener el archivo de matemáticas:

```bash
# Verificar que existe
ls data/curriculum/matematicas.json
```

---

## 🎮 Ejecutar la Aplicación

### Modo Principal (Con Interfaz Gráfica)

```bash
python main.py
```

### Modo de Prueba (Solo Consola)

```bash
# Probar TTS
python src/services/tts_service.py

# Probar STT  
python src/services/stt_service.py

# Probar Voice Manager
python src/logic/voice_manager.py
```

---

## 🔧 Solución de Problemas

### Error: "ANTHROPIC_API_KEY not found"

**Solución:** Asegúrate de haber configurado el archivo `.env` correctamente.

```bash
# Verificar que el archivo existe
cat .env

# Debe contener:
ANTHROPIC_API_KEY=sk-ant-...
```

### Error: "No module named 'PyQt6'"

**Solución:** Instalar PyQt6:
```bash
pip install PyQt6
```

### Error: "pyttsx3 initialization failed"

**Solución Windows:**
```bash
pip install pywin32
```

**Solución macOS:**
```bash
# pyttsx3 usa NSSpeechSynthesizer, viene pre-instalado
# Si hay problemas, reinstalar:
pip uninstall pyttsx3
pip install pyttsx3
```

**Solución Linux:**
```bash
sudo apt-get install espeak espeak-data libespeak-dev
pip install pyttsx3
```

### Error: "No default microphone available"

**Solución:** 
- Verificar que tengas un micrófono conectado
- En Windows: Configuración → Sistema → Sonido → Entrada
- En macOS: Preferencias del Sistema → Sonido → Entrada
- En Linux: `arecord -l` para listar dispositivos

### Error: "Could not create database"

**Solución:**
```bash
# Crear manualmente el directorio
mkdir -p data
python -c "from src.data.database import get_db_manager; get_db_manager().create_tables()"
```

---

## 📁 Estructura de Archivos

Después de la instalación, deberías tener:

```
maiten_ai/
├── .env                    ← Tu API key aquí
├── main.py                 ← Ejecutar este archivo
├── requirements.txt
├── data/
│   ├── user_profile.db    ← Se crea automáticamente
│   └── curriculum/
│       └── matematicas.json
├── logs/
│   └── maiten_ai.log      ← Se crea automáticamente
└── src/
    ├── ai/
    ├── data/
    ├── logic/
    ├── services/
    └── ui/
```

---

## 🎯 Primera Ejecución

1. **Iniciar la aplicación:**
```bash
python main.py
```

2. **Seleccionar una materia** desde el menú lateral (ej: 🔢 Matemáticas)

3. **Hacer una pregunta:** 
   - Escribir en el campo de texto: "¿Qué son las fracciones?"
   - O usar el botón 🎤 para hablar

4. **Recibir respuesta:**
   - El asistente responderá por texto
   - Si TTS está habilitado, también hablará

---

## 🔑 Obtener API Key de Anthropic

1. Ir a https://console.anthropic.com/
2. Crear cuenta o iniciar sesión
3. Ir a "API Keys"
4. Click en "Create Key"
5. Copiar la key (empieza con `sk-ant-...`)
6. Pegarla en tu archivo `.env`

**Nota:** La API Key es gratuita para empezar, con créditos limitados.

---

## 📊 Verificar Instalación

```bash
# Verificar Python
python --version
# Debe ser 3.10 o superior

# Verificar pip
pip --version

# Verificar que las dependencias están instaladas
pip list | grep -E "PyQt6|anthropic|pyttsx3|speech"

# Verificar estructura
ls -la data/curriculum/
```

---

## 🆘 Soporte

Si encuentras problemas:

1. **Revisar logs:**
```bash
cat logs/maiten_ai.log
```

2. **Verificar instalación:**
```bash
python -c "import PyQt6; import anthropic; import pyttsx3; print('✓ All imports OK')"
```

3. **Abrir un issue en GitHub** con:
   - Sistema operativo
   - Versión de Python
   - Mensaje de error completo
   - Contenido de `logs/maiten_ai.log`

---

## 🎉 ¡Listo!

Si todo funciona correctamente, deberías ver:

```
============================================================
Starting Maiten AI - Learn better
============================================================
User loaded: Maitena (ID: 1)
Application started successfully
```

¡Ahora puedes empezar a usar Maiten AI! 🎓✨
