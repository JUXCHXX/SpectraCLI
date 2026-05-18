<div align="center">

```
███████╗██████╗ ███████╗ ██████╗████████╗██████╗  █████╗ 
██╔════╝██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗
███████╗██████╔╝█████╗  ██║        ██║   ██████╔╝███████║
╚════██║██╔═══╝ ██╔══╝  ██║        ██║   ██╔══██╗██╔══██║
███████║██║     ███████╗╚██████╗   ██║   ██║  ██║██║  ██║
╚══════╝╚═╝     ╚══════╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝
```

**Espeja y controla la pantalla de tu celular desde tu PC — sin cables, sin nube, sin límites.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-8B5CF6?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![WebSocket](https://img.shields.io/badge/WebSocket-RFC%206455-7C3AED?style=for-the-badge&logo=websocket&logoColor=white)](https://websockets.readthedocs.io)
[![React](https://img.shields.io/badge/React-18-06B6D4?style=for-the-badge&logo=react&logoColor=white)](https://react.dev)
[![Capacitor](https://img.shields.io/badge/Capacitor-5-119EFF?style=for-the-badge&logo=capacitor&logoColor=white)](https://capacitorjs.com)
[![Licencia](https://img.shields.io/badge/Licencia-MIT-A855F7?style=for-the-badge)](LICENSE)
[![Plataforma](https://img.shields.io/badge/Plataforma-Windows%20%7C%20macOS%20%7C%20Linux-6D28D9?style=for-the-badge)](https://github.com/yourname/spectra)

<br/>

<!-- ESPACIO PARA EL LOGO -->
<!-- <img src="assets/spectra-logo.png" alt="Logo de Spectra" width="200"/> -->

</div>

---

## 🖥️ Vista en la terminal

<!-- ESPACIO PARA CAPTURA DE PANTALLA DE LA TERMINAL -->
> 📸 *Agrega aquí una captura de cómo se ve Spectra corriendo en tu terminal*
<!-- <img src="assets/terminal-preview.png" alt="Spectra en Terminal" width="100%"/> -->

---

## 📱 Vista en el celular

<!-- ESPACIO PARA CAPTURA DE PANTALLA DEL CELULAR -->
> 📸 *Agrega aquí una captura de cómo se ve la app Spectra en tu celular*
<!-- <img src="assets/mobile-preview.png" alt="App Spectra en Celular" width="300"/> -->

---

## ✨ ¿Qué es Spectra?

Spectra es una herramienta de **espejado de pantalla por WiFi local** que tiene dos partes:

| Parte | Descripción |
|-------|-------------|
| 🖥️ **Spectra CLI** | Servidor Python que corre en tu PC, genera un código QR y recibe los frames de la pantalla |
| 📱 **Spectra App** | App Android/iOS que captura la pantalla de tu celular y la envía a la PC en tiempo real |

Todo ocurre **en tu red local** — sin internet, sin datos enviados a ninguna nube, sin suscripciones.

---

## ⚡ ¿Cómo funciona?

```
  PC (servidor)               WiFi                Celular (cliente)
  ─────────────              ──────              ──────────────────
  spectra start  ──────────────────────────────►  Abrir app Spectra
  Abre puerto 7799                                 Escanear código QR
  Muestra QR con IP ◄──────────────────────────── Lee IP + puerto
  Acepta conexión   ◄──────────────────────────── Conecta por WebSocket
  Recibe frames     ◄──────────────────────────── Envía frames de pantalla
  Muestra ventana              en tiempo real      Captura a 24fps
```

---

## 🛠️ Stack tecnológico

<div align="center">

| Capa | Tecnología |
|------|-----------|
| 🐍 Servidor | Python 3.8+ |
| 🔌 Protocolo | WebSockets (RFC 6455) |
| 📸 Captura | Pillow + MSS |
| 📡 Código QR | qrcode[pil] |
| 🖼️ Ventana espejo | Tkinter |
| 📱 App móvil | React + TypeScript |
| 📲 Puente nativo | Capacitor 5 |
| 🎨 Interfaz | Tailwind CSS |

</div>

---

## 📋 Requisitos

### En la PC (este repositorio)
- Python **3.8 o superior**
- Windows, macOS o Linux
- Conectado a **WiFi local**

### En el celular
- Android **8.0+** o iOS **13+**
- **APK de Spectra** instalada (ver abajo ↓)
- Conectado a la **misma red WiFi** que tu PC

> ⚠️ **Ambos dispositivos deben estar en la misma red WiFi.** Los datos móviles NO funcionarán.

---

## 📲 Paso 1 — Instala la app Spectra en tu celular

Antes de correr el servidor en la PC, necesitas tener la app Spectra instalada en tu Android.

**Descarga el APK:**

```
https://github.com/yourname/spectra/releases/latest
```

1. Descarga `spectra-release.apk` desde la página de Releases
2. En tu Android, ve a **Ajustes → Seguridad → Instalar apps desconocidas** y habilítalo para tu navegador o gestor de archivos
3. Abre el APK descargado y toca **Instalar**
4. Abre la app **Spectra** — verás la pantalla del escáner QR lista para usarse

> 🍎 **Usuarios de iPhone:** El sideloading en iOS requiere TestFlight o una build de desarrollador. Próximamente.

---

## 💻 Paso 2 — Instala el servidor en tu PC

### Opción A — Instalar desde GitHub (recomendado)

```bash
# Clona el repositorio
git clone https://github.com/yourname/spectra.git
cd spectra

# Crea un entorno virtual
python -m venv .venv

# Actívalo
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# Instala las dependencias
pip install websockets Pillow qrcode mss

# Instala Spectra
pip install -e .
```

### Opción B — Ejecutar sin instalar

```bash
git clone https://github.com/yourname/spectra.git
cd spectra
pip install websockets Pillow qrcode mss
python -m spectra.cli
```

---

## 🚀 Paso 3 — Inicia el espejado

```bash
spectra
```

Verás la animación de arranque y luego el menú principal. Selecciona **Iniciar espejado**.

Spectra automáticamente:
1. Detecta tu IP local
2. Muestra un **código QR** en la terminal
3. Abre una **ventana flotante** en tu PC lista para mostrar la pantalla
4. Espera a que tu celular se conecte

En tu celular, abre la app Spectra y **escanea el QR**. La ventana flotante empezará a mostrar la pantalla de tu celular en tiempo real.

---

## 🎛️ Comandos en vivo

Una vez que el servidor está corriendo, usa estos atajos de teclado:

| Tecla | Acción |
|-------|--------|
| `s` | Ver panel de estado |
| `r` | Actualizar código QR |
| `m` | Volver al menú principal |
| `q` | Salir de Spectra |
| `Ctrl+C` | Forzar salida |

---

## 📦 Argumentos de línea de comandos

```bash
spectra              # Abrir menú interactivo
spectra start        # Iniciar servidor directamente
spectra diag         # Ejecutar diagnóstico del sistema
spectra --version    # Ver versión
spectra --help       # Ver ayuda
```

---

## 🔧 Solución de problemas

**La ventana espejo está en negro / no aparece imagen:**
> Asegúrate de que la app Spectra en tu celular muestra "Conectado". El celular debe enviar el mensaje `hello` antes de empezar a transmitir.

**No conecta / el QR no funciona:**
> Ambos dispositivos deben estar en el mismo WiFi. Revisa el firewall de tu PC — permite que Python use el puerto `7799`.

**`ModuleNotFoundError: No module named 'websockets'`:**
```bash
pip install websockets Pillow qrcode mss
```

**`pip install -e .` falla:**
```bash
pip install --upgrade setuptools pip
pip install -e .
```

**El puerto 7799 ya está en uso:**
> Spectra detecta automáticamente el siguiente puerto disponible y actualiza el QR.

---

## 🗂️ Estructura del proyecto

```
spectra/
├── spectra/
│   ├── __init__.py       # Versión del paquete
│   ├── cli.py            # Punto de entrada + TUI
│   ├── server.py         # Servidor WebSocket
│   ├── capture.py        # Motor de captura de pantalla
│   ├── network.py        # Detección de IP + generación de QR
│   └── tui.py            # Componentes de interfaz en terminal
├── setup.py
├── pyproject.toml
└── README.md
```

---

## 🤝 Contribuir

Los pull requests son bienvenidos. Para cambios grandes, por favor abre un issue primero.

1. Haz fork del repositorio
2. Crea tu rama: `git checkout -b feature/tu-feature`
3. Haz commit: `git commit -m 'Agrega tu feature'`
4. Push: `git push origin feature/tu-feature`
5. Abre un Pull Request

---

## 📄 Licencia

MIT © [DevFlorian](https://github.com/JUXCHXX)

---

<div align="center">

Hecho con 💜 y Python

**[⬆ Volver arriba](#)**

</div>
