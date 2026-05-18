# ⬡ Spectra

> Mirror and control your phone screen from your PC over WiFi — no cables needed.

```
       .::::::..............................:::----:.
    .---..                                        .:-+=.
   =*-                                                -#+.
 .++.                                                   =+.
.=-                                                      :=.
```

**Spectra** connects your phone to your PC over your local WiFi network.  
Open the Spectra mobile app, scan the QR code shown in your terminal, and start mirroring.

---

## ✦ Install

### One-line install (recommended)

```bash
pip install git+https://github.com/yourname/spectra.git
```

### Or clone and install locally

```bash
git clone https://github.com/yourname/spectra.git
cd spectra
pip install -e .
```

---

## ✦ Usage

```bash
# Launch interactive menu
spectra

# Start mirror server directly
spectra start

# Run diagnostics
spectra diag

# Show version
spectra --version
```

---

## ✦ How it works

```
PC terminal              WiFi (local network)        Phone
────────────             ────────────────────        ─────
spectra start    ──────────────────────────────►   Spectra app
shows QR code                                      scans QR
opens port 7799  ◄──────────── WebSocket ────────  connects
streams screen   ──────────────────────────────►   shows mirror
receives touch   ◄──────────────────────────────   sends gestures
```

1. Run `spectra start` on your PC
2. Open the **Spectra** app on your phone
3. Tap **Scan QR Code** and scan the code in your terminal
4. Your phone screen appears in the app — and you can control it from your PC

> ⚠️ Both devices must be on the **same WiFi network**

---

## ✦ Requirements

- Python 3.9+
- Same WiFi network on phone and PC
- [Spectra mobile app](https://github.com/yourname/spectra-app) installed on phone

### Optional (for faster capture)

```bash
pip install mss          # faster screen capture on Windows/Mac
pip install Pillow       # image processing (usually auto-installed)
```

---

## ✦ Dependencies

| Package      | Purpose                  |
|--------------|--------------------------|
| `websockets` | Real-time communication  |
| `qrcode`     | QR code generation       |
| `Pillow`     | Screen capture & encoding|

---

## ✦ Project structure

```
spectra/
├── spectra/
│   ├── __init__.py     # Version
│   ├── cli.py          # Main entry point & TUI
│   ├── tui.py          # Terminal UI components
│   ├── server.py       # WebSocket server
│   ├── network.py      # IP detection, QR generation
│   └── capture.py      # Screen capture engine
├── setup.py
├── pyproject.toml
└── README.md
```

---

## ✦ License

MIT — do whatever you want with it.

---

Made with 💜 by [Your Name](https://github.com/yourname)
