# ⬡ Spectra

> **Espeja la pantalla de tu teléfono en tu PC por WiFi — sin cables, en tiempo real.**

```
       .::::::..............................:::----:.
    .---..                                        .:-+=.
   =*-                                                -#+.
 .++.                                                   =+.
.=-                                                      :=.
```

---

## 📱 ¿Qué es Spectra?

**Spectra** es una herramienta de espejo de pantalla en tiempo real que conecta tu teléfono Android o iOS con tu PC a través de WiFi local.

- ✅ **Espejo en vivo**: Ve la pantalla de tu teléfono en una ventana flotante en tu PC
- ✅ **Métricas en tiempo real**: Muestra FPS y latencia en el título de la ventana
- ✅ **Sin cables**: Funciona completamente por WiFi en tu red local
- ✅ **Fácil de usar**: Solo escanea un código QR desde tu terminal
- ✅ **Multiplataforma**: Funciona en Windows, macOS y Linux

**Caso de uso**: Útil para:
- Demostrar tu teléfono en presentaciones
- Grabar tutoriales
- Debugging de aplicaciones
- Captura de pantalla de alta calidad

---

## 🚀 Instalación

### Paso 1: Descargar el repositorio

```bash
git clone https://github.com/yourname/spectra.git
cd spectra
```

### Paso 2: Instalar dependencias

```bash
pip install -e .
```

Esto instala automáticamente:
- `websockets` - Comunicación en tiempo real
- `qrcode` - Generación de códigos QR
- `Pillow` - Procesamiento de imágenes

### Verificar la instalación

```bash
spectra --version
```

Deberías ver: `Spectra 0.1.0`

---

## ⚙️ Configuración de dependencias (Opcional)

Para una captura más rápida en Windows/Mac:

```bash
pip install mss
```

Para usar la ventana espejo, necesitas:
- **Windows**: Viene preinstalado
- **macOS**: Viene preinstalado  
- **Linux**: `sudo apt-get install python3-tk`

---

## 📖 Cómo usar Spectra

### Opción 1: Menú interactivo (Recomendado)

```bash
spectra
```

Se abrirá un menú donde puedes:
1. **Start mirroring** - Inicia el servidor y muestra código QR
2. **Diagnostics** - Verifica dependencias y configuración
3. **Settings** - Configura calidad, puerto, nombre del dispositivo
4. **About** - Información de versión

### Opción 2: Iniciar servidor directamente

```bash
spectra start
```

Inicia inmediatamente el servidor sin menú.

### Opción 3: Ejecutar diagnósticos

```bash
spectra diag
```

Verifica que todas las dependencias estén correctamente instaladas.

---

## 🔄 Flujo completo paso a paso

### En tu PC:

**1.** Abre una terminal en la carpeta del proyecto:
```bash
cd ~/spectra
```

**2.** Inicia Spectra:
```bash
spectra start
```

Verás algo así en la terminal:

```
╔══════════════════════════════════════╗
║         SPECTRA  v0.1.0             ║
║    Screen Mirror • Terminal App      ║
╚══════════════════════════════════════╝

───────────────────────────────────────

✓ Spectra 0.1.0 ready!

◈ Starting server

✓ WebSocket server running on port 7799

◈ Connection QR Code

[Código QR aquí]

Commands:  [q] Quit  [s] Status  [r] Refresh QR  [m] Menu
```

**3.** Copia la IP que aparece (ej: `192.168.1.100`)

### En tu teléfono:

**1.** Abre la app Spectra (disponible en Google Play / App Store)

**2.** Toca **"Escanear código QR"**

**3.** Apunta la cámara al código QR que ves en tu PC

**4.** La app se conectará automáticamente

### De vuelta en tu PC:

**✅ Tu pantalla de teléfono aparecerá en una ventana flotante**

- Verás el FPS en tiempo real
- Verás la latencia en ms
- Puedes redimensionar la ventana
- La ventana siempre estará al frente

---

## 🎮 Controles durante la sesión

| Tecla | Acción |
|-------|--------|
| `q` | Salir y detener espejo |
| `s` | Mostrar estado |
| `r` | Refrescar código QR |
| `m` | Abrir menú |

---

## 📊 Tabla de dependencias

| Paquete | Propósito | Estado |
|---------|-----------|--------|
| `websockets` | Protocolo WebSocket | **Requerido** |
| `qrcode` | Generar códigos QR | **Requerido** |
| `Pillow` | Procesamiento de imágenes | **Requerido** |
| `tkinter` | Ventana flotante GUI | **Requerido** |
| `mss` | Captura rápida | Opcional |

---

## 🖼️ Capturas de pantalla

### Terminal con código QR
![Placeholder for terminal QR code](https://via.placeholder.com/800x400?text=Terminal+QR+Code)

### Ventana espejo flotante
![Placeholder for mirror window](https://via.placeholder.com/800x400?text=Floating+Mirror+Window)

### Contador de FPS y latencia
![Placeholder for FPS counter](https://via.placeholder.com/800x400?text=FPS+Counter+Display)

---

## 🔧 Solución de problemas

### ❌ Error: "Module not found: tkinter"

**Linux:**
```bash
sudo apt-get install python3-tk
```

**macOS:**
```bash
brew install python-tk
```

---

### ❌ Error: "Module not found: websockets"

```bash
pip install websockets
```

---

### ❌ La ventana espejo no aparece

1. Verifica que tkinter esté instalado: `spectra diag`
2. Verifica que Pillow esté instalado: `pip install Pillow`
3. Asegúrate de que el teléfono está conectado

---

### ❌ La pantalla se ve entrecortada o lenta

1. Baja la calidad: Menú → Settings → Quality → Low
2. Acércate al router WiFi
3. Reduce otro tráfico de red

---

### ❌ No puedo ver el teléfono en la red

- ✅ Ambos (PC y teléfono) **deben estar en la misma red WiFi**
- ✅ Verifica que el cortafuegos no bloquea puerto 7799
- ✅ Intenta con un puerto diferente: Menú → Settings → Port

---

## 📁 Estructura del proyecto

```
spectra/
├── spectra/
│   ├── __init__.py          # Versión
│   ├── cli.py               # Entrada principal y TUI
│   ├── tui.py               # Componentes de interfaz terminal
│   ├── server.py            # Servidor WebSocket
│   ├── mirror_window.py     # Ventana flotante tkinter
│   ├── network.py           # Detección IP, generación QR
│   └── capture.py           # Motor de captura de pantalla
├── setup.py
├── pyproject.toml
└── README.md
```

---

## 🔐 Requisitos

- **Python 3.9+**
- **Red WiFi local** (PC y teléfono en la misma red)
- **App Spectra** instalada en tu teléfono

---

## 📝 Cómo funciona internamente

```
Terminal PC              WiFi (red local)           Teléfono
──────────              ────────────────           ─────────
spectra start    ←──────────────────────────→   App Spectra
muestra QR                                       escanea QR
abre puerto 7799 ←────── WebSocket ─────────→   se conecta
transmite pantalla ←──────────────────────────→ muestra espejo
recibe gestos    ←──────────────────────────→   envía toques
```

**Paso a paso:**

1. Ejecutas `spectra start` en tu PC
2. La app Spectra escanea el código QR
3. Se abre una conexión WebSocket
4. Tu PC envía frames de pantalla codificados en base64
5. Tu teléfono los decodifica y muestra
6. Los gestos se envían de vuelta (si lo implementas)

---

## 📋 Características

- 🪟 **Ventana flotante**: Siempre visible y redimensionable
- 📊 **Métricas en vivo**: FPS y latencia en el título
- 🔒 **Seguro**: Solo en red local
- ⚡ **Bajo latency**: Optimizado para <50ms
- 🎛️ **Presets de calidad**: Low/Medium/High/Ultra
- 🖥️ **Multiplataforma**: Windows, macOS, Linux

---

## 📄 Licencia

MIT — Usa libremente

---

Hecho con 💜 por [Tu nombre](https://github.com/yourname)
