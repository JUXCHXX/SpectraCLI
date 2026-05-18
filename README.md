<div align="center">

```
███████╗██████╗ ███████╗ ██████╗████████╗██████╗  █████╗ 
██╔════╝██╔══██╗██╔════╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗
███████╗██████╔╝█████╗  ██║        ██║   ██████╔╝███████║
╚════██║██╔═══╝ ██╔══╝  ██║        ██║   ██╔══██╗██╔══██║
███████║██║     ███████╗╚██████╗   ██║   ██║  ██║██║  ██║
╚══════╝╚═╝     ╚══════╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝
```

**Mirror and control your phone screen from your PC — no cables, no cloud, no limits.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-8B5CF6?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![WebSocket](https://img.shields.io/badge/WebSocket-RFC%206455-7C3AED?style=for-the-badge&logo=websocket&logoColor=white)](https://websockets.readthedocs.io)
[![React](https://img.shields.io/badge/React-18-06B6D4?style=for-the-badge&logo=react&logoColor=white)](https://react.dev)
[![Capacitor](https://img.shields.io/badge/Capacitor-5-119EFF?style=for-the-badge&logo=capacitor&logoColor=white)](https://capacitorjs.com)
[![License](https://img.shields.io/badge/License-MIT-A855F7?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-6D28D9?style=for-the-badge)](https://github.com/yourname/spectra)

<br/>

<!-- LOGO PLACEHOLDER -->
<!-- <img src="assets/spectra-logo.png" alt="Spectra Logo" width="200"/> -->

</div>

---

## 🖥️ Terminal Preview

<!-- TERMINAL SCREENSHOT PLACEHOLDER -->
> 📸 *Add a screenshot of Spectra running in your terminal here*
<!-- <img src="assets/terminal-preview.png" alt="Spectra Terminal" width="100%"/> -->

---

## 📱 Mobile Preview

<!-- MOBILE SCREENSHOT PLACEHOLDER -->
> 📸 *Add a screenshot of the Spectra app on your phone here*
<!-- <img src="assets/mobile-preview.png" alt="Spectra Mobile App" width="300"/> -->

---

## ✨ What is Spectra?

Spectra is a **local WiFi screen mirroring tool** made up of two parts:

| Part | Description |
|------|-------------|
| 🖥️ **Spectra CLI** | Python server that runs on your PC, generates a QR code and receives screen frames |
| 📱 **Spectra App** | Android/iOS app that captures your phone screen and sends it to your PC in real time |

Everything happens **on your local network** — no internet required, no data sent to any cloud, no subscriptions.

---

## ⚡ How It Works

```
  PC (server)                WiFi                 Phone (client)
  ───────────               ──────               ───────────────
  spectra start   ─────────────────────────────►  Open Spectra App
  Opens port 7799                                  Scan QR code
  Shows QR with IP ◄───────────────────────────── Reads IP + port
  Accepts connection ◄──────────────────────────  Connects via WebSocket
  Receives frames  ◄────────────────────────────  Sends screen frames
  Shows mirror win.          real-time            Captures screen @ 24fps
```

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology |
|-------|-----------|
| 🐍 Server | Python 3.8+ |
| 🔌 Protocol | WebSockets (RFC 6455) |
| 📸 Capture | Pillow + MSS |
| 📡 QR Code | qrcode[pil] |
| 🖼️ Mirror Window | Tkinter |
| 📱 Mobile App | React + TypeScript |
| 📲 Native Bridge | Capacitor 5 |
| 🎨 UI | Tailwind CSS |

</div>

---

## 📋 Requirements

### PC Side (this repo)
- Python **3.8 or higher**
- Windows, macOS or Linux
- Connected to **local WiFi**

### Phone Side
- Android **8.0+** or iOS **13+**
- **Spectra APK** installed (see below ↓)
- Connected to the **same WiFi network** as your PC

> ⚠️ **Both devices must be on the same WiFi network.** Mobile data will NOT work.

---

## 📲 Step 1 — Install the Spectra App on your phone

Before running the PC server, you need the Spectra app on your Android phone.

**Download the APK:**

```
https://github.com/yourname/spectra/releases/latest
```

1. Download `spectra-release.apk` from the Releases page
2. On your Android phone, go to **Settings → Security → Install unknown apps** and enable it for your browser or file manager
3. Open the downloaded APK and tap **Install**
4. Open the **Spectra** app — you'll see the QR scanner screen

> 🍎 **iOS users:** iOS sideloading requires TestFlight or a developer build. See [iOS Setup](docs/ios-setup.md) for instructions.

---

## 💻 Step 2 — Install the PC Server

### Option A — Install from GitHub (recommended)

```bash
# Clone the repo
git clone https://github.com/yourname/spectra.git
cd spectra

# Create a virtual environment
python -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# Install dependencies
pip install websockets Pillow qrcode mss

# Install Spectra
pip install -e .
```

### Option B — Run without installing

```bash
git clone https://github.com/yourname/spectra.git
cd spectra
pip install websockets Pillow qrcode mss
python -m spectra.cli
```

---

## 🚀 Step 3 — Start Mirroring

```bash
spectra
```

You'll see the animated boot sequence, then the main menu. Select **Start Mirroring**.

Spectra will:
1. Detect your local IP automatically
2. Show a **QR code** in the terminal
3. Open a floating **Mirror Window** on your PC
4. Wait for your phone to connect

On your phone, open the Spectra app and **scan the QR code**. The mirror window will start showing your phone screen in real time.

---

## 🎛️ CLI Commands

Once the server is running, use these keyboard shortcuts:

| Key | Action |
|-----|--------|
| `s` | Show status panel |
| `r` | Refresh QR code |
| `m` | Back to main menu |
| `q` | Quit Spectra |
| `Ctrl+C` | Force quit |

---

## 📦 CLI Arguments

```bash
spectra              # Launch interactive menu
spectra start        # Start mirror server directly
spectra diag         # Run system diagnostics
spectra --version    # Show version
spectra --help       # Show help
```

---

## 🔧 Troubleshooting

**Mirror window is black / no image:**
> Make sure you opened the Spectra app and it shows "Connected". The phone must send a `hello` message before streaming starts.

**Can't connect / QR doesn't work:**
> Both devices must be on the same WiFi. Check your PC firewall — allow Python on port `7799`.

**`ModuleNotFoundError: No module named 'websockets'`:**
```bash
pip install websockets Pillow qrcode mss
```

**`pip install -e .` fails:**
```bash
pip install --upgrade setuptools pip
pip install -e .
```

**Port 7799 already in use:**
> Spectra will automatically find the next available port and update the QR code.

---

## 🗂️ Project Structure

```
spectra/
├── spectra/
│   ├── __init__.py       # Version info
│   ├── cli.py            # Main entry point + TUI
│   ├── server.py         # WebSocket server
│   ├── capture.py        # Screen capture engine
│   ├── network.py        # IP detection + QR generation
│   └── tui.py            # Terminal UI components
├── setup.py
├── pyproject.toml
└── README.md
```

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

1. Fork the repo
2. Create your branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m 'Add your feature'`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

MIT © [yourname](https://github.com/yourname)

---

<div align="center">

Made with 💜 and Python

**[⬆ Back to top](#)**

</div>
