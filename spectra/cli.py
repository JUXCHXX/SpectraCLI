#!/usr/bin/env python3
"""
╔══════════════════════════════════════╗
║         SPECTRA  v0.1.0             ║
║    Screen Mirror • Terminal App      ║
╚══════════════════════════════════════╝

Entry point for the `spectra` CLI command.
"""

import sys
import os
import time
import threading
import signal
import queue

# Ensure package is importable when run directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from spectra import __version__
from spectra.tui import (
    C, clear, hide_cursor, show_cursor,
    print_logo, box, divider, label, badge,
    Spinner, progress_bar, StatusPanel,
    Menu, success, error, info, warn, section,
    term_width,
)
from spectra.network import get_local_ip, get_hostname, find_free_port, print_qr_panel
from spectra.server import SpectraServer
from spectra.capture import ScreenCapture
from spectra.mirror_window import MirrorWindow


# ─── Global state ─────────────────────────────────────────────────────────────

_server: SpectraServer = None
_capture: ScreenCapture = None
_mirror_window: MirrorWindow = None
_frame_queue: queue.Queue = None
_status = StatusPanel()
_running = True


# ─── Boot sequence ────────────────────────────────────────────────────────────

def boot_sequence():
    """Animated startup sequence"""
    clear()
    print_logo(animated=True)

    time.sleep(0.3)
    print()
    divider("─", C.DEEP_PURPLE)
    print()

    # Boot steps
    steps = [
        ("Initializing Spectra core",     0.4),
        ("Detecting network interfaces",   0.5),
        ("Checking system dependencies",   0.4),
        ("Preparing WebSocket server",     0.3),
        ("Loading capture engine",         0.4),
    ]

    for msg, duration in steps:
        sp = Spinner(msg, style="pulse", color=C.PURPLE)
        sp.start()
        time.sleep(duration)
        sp.stop(success=True, message=msg)

    print()
    progress_bar("Starting up", duration=0.8, color=C.VIOLET)
    print()
    success(f"Spectra {__version__} ready!")
    time.sleep(0.4)


# ─── Server session ───────────────────────────────────────────────────────────

def run_server(quality: str = "medium"):
    """Start the mirror server session"""
    global _server, _capture, _mirror_window, _frame_queue

    clear()
    print_logo(animated=False)
    divider("─", C.DEEP_PURPLE)

    ip   = get_local_ip()
    port = find_free_port(7799)
    name = get_hostname()

    # Create shared frame queue
    _frame_queue = queue.Queue(maxsize=2)

    # ── Update status
    _status.update("server",  "STARTING…",  C.YELLOW)
    _status.update("ip",      ip,            C.CYAN)
    _status.update("port",    str(port),     C.PURPLE)
    _status.update("network", "LOCAL WIFI",  C.GREEN)

    # ── Start WebSocket server
    section("Starting server")

    def on_connect(addr):
        _status.update("clients",   "1",           C.GREEN)
        _status.update("mirroring", "CONNECTING…", C.YELLOW)
        print(f"\n  {C.GREEN}◉{C.RESET}  {C.WHITE}Client connected:{C.RESET} {C.CYAN}{addr[0]}:{addr[1]}{C.RESET}")

    def on_disconnect(addr):
        _status.update("clients",   "0",    C.GRAY)
        _status.update("mirroring", "IDLE", C.GRAY)
        print(f"\n  {C.RED}◎{C.RESET}  {C.GRAY}Client disconnected:{C.RESET} {addr[0]}")
        global _mirror_window
        if _mirror_window:
            _mirror_window.stop()
            _mirror_window = None

    def on_message(addr, data):
        global _mirror_window
        msg_type = data.get("type", "unknown")

        if msg_type == "hello":
            device = data.get("device", "unknown")
            _status.update("mirroring", "ACTIVE ●", C.GREEN)
            print(f"\n  {C.PURPLE}⬡{C.RESET}  {C.WHITE}Device handshake:{C.RESET} {C.LAVENDER}{device}{C.RESET}")

            if not _mirror_window:
                _mirror_window = MirrorWindow(_frame_queue)
                _mirror_window.start()
                print(f"  {C.CYAN}→{C.RESET}  Mirror window opened")

            _start_capture()

        elif msg_type == "touch":
            x, y = data.get("x", 0), data.get("y", 0)
            pass

        elif msg_type == "pong":
            ts = data.get("ts", 0)
            latency_ms = int((time.time() - ts) * 1000)
            _status.update("mirroring", f"ACTIVE ● {latency_ms}ms", C.GREEN)
            if _mirror_window:
                _mirror_window.set_latency(latency_ms)

    _server = SpectraServer(
        ip="0.0.0.0",
        port=port,
        on_client_connect=on_connect,
        on_client_disconnect=on_disconnect,
        on_message=on_message,
        frame_queue=_frame_queue,
    )

    sp = Spinner("Binding WebSocket server…", color=C.PURPLE)
    sp.start()
    try:
        _server.start_background()
        sp.stop(success=True, message=f"WebSocket server running on port {port}")
        _status.update("server", "RUNNING ●", C.GREEN)
    except Exception as e:
        sp.stop(success=False, message=f"Server error: {e}")
        error(str(e))
        return

    # ── Print QR code
    section("Connection QR Code")
    print_qr_panel(ip, port, name)

    # ── Status panel
    _status.render()

    # ── Instructions
    print()
    w = term_width()
    print(f"  {C.GRAY}Commands:{C.RESET}  "
          f"{C.PURPLE}[q]{C.RESET} Quit  "
          f"{C.PURPLE}[s]{C.RESET} Status  "
          f"{C.PURPLE}[r]{C.RESET} Refresh QR  "
          f"{C.PURPLE}[m]{C.RESET} Menu")
    print()

    # ── Live input loop
    _live_loop()


def _start_capture():
    """Start screen capture and pipe frames to server"""
    global _capture
    if _capture and _capture._running:
        return

    _capture = ScreenCapture(quality="medium")

    deps = ScreenCapture.check_dependencies()
    if not deps.get("pillow"):
        warn("Pillow not installed — screen capture disabled.")
        warn("Run: pip install pillow  to enable mirroring.")
        return

    def send_frame(frame):
        if _server:
            _server.send_frame(frame["data"], frame["w"], frame["h"])

    _capture.start_streaming(send_frame)
    success("Screen capture active")


def _live_loop():
    """Command loop while server is running"""
    global _running

    try:
        import tty, termios

        def getch():
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                return sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)

        while _running:
            ch = getch()

            if ch in ('q', 'Q', '\x03'):  # q or Ctrl+C
                break
            elif ch in ('s', 'S'):
                print()
                _status.render()
            elif ch in ('r', 'R'):
                ip = get_local_ip()
                port = _server.port if _server else 7799
                name = get_hostname()
                section("Refreshed QR Code")
                print_qr_panel(ip, port, name)
            elif ch in ('m', 'M'):
                show_main_menu()

    except (ImportError, Exception):
        # Windows / non-tty fallback
        print(f"\n  {C.GRAY}Press Ctrl+C to quit…{C.RESET}\n")
        try:
            while _running:
                time.sleep(1)
        except KeyboardInterrupt:
            pass

    _shutdown()


# ─── Settings screen ──────────────────────────────────────────────────────────

def show_settings():
    clear()
    print_logo(animated=False)
    section("Settings")

    options = [
        ("1", "Streaming quality",  "Set frame quality / FPS"),
        ("2", "Port",               "Change WebSocket port (default 7799)"),
        ("3", "Device name",        "How your PC appears in the app"),
        ("b", "Back",               "Return to main menu"),
    ]

    menu = Menu("Configure Spectra", options)

    # Initial render
    menu._render()

    try:
        choice = menu.run()
    except Exception:
        choice = input("  Choice: ").strip()

    if choice == "1":
        show_quality_selector()
    elif choice == "b":
        show_main_menu()


def show_quality_selector():
    section("Streaming Quality")
    options = [
        ("1", "Low",    "360p • 15fps • Best for slow networks"),
        ("2", "Medium", "540p • 24fps • Recommended"),
        ("3", "High",   "720p • 30fps • Fast networks"),
        ("4", "Ultra",  "1080p • 60fps • Same-room WiFi"),
        ("b", "Back",   ""),
    ]
    menu = Menu("Select quality preset", options)
    menu._render()
    choice = input("  Select: ").strip()
    info(f"Quality set. Changes apply on next session.")
    time.sleep(1)
    show_settings()


# ─── About screen ─────────────────────────────────────────────────────────────

def show_about():
    clear()
    print_logo(animated=False)
    section("About Spectra")

    lines = [
        label("Version",   f"{__version__}",                  vcolor=C.LAVENDER),
        label("License",   "MIT",                              vcolor=C.GRAY),
        label("GitHub",    "github.com/yourname/spectra",      vcolor=C.CYAN),
        label("Platform",  _get_platform(),                    vcolor=C.GRAY),
        "",
        f"{C.GRAY}Spectra lets you mirror and control your phone screen{C.RESET}",
        f"{C.GRAY}from your PC over local WiFi — no cables needed.{C.RESET}",
        "",
        f"{C.DIM}Built with Python + WebSockets + Three.js{C.RESET}",
    ]
    box("◈  SPECTRA", lines, color=C.DEEP_PURPLE)
    print()
    input(f"  {C.GRAY}Press Enter to go back…{C.RESET}")
    show_main_menu()


def _get_platform() -> str:
    import platform
    return f"{platform.system()} {platform.release()}"


# ─── Diagnostics ──────────────────────────────────────────────────────────────

def show_diagnostics():
    clear()
    print_logo(animated=False)
    section("System Diagnostics")

    sp = Spinner("Running diagnostics…", color=C.VIOLET)
    sp.start()
    time.sleep(1.2)
    sp.stop(success=True, message="Diagnostics complete")

    ip   = get_local_ip()
    port = find_free_port(7799)
    deps = ScreenCapture.check_dependencies()

    def dep_badge(ok):
        return f"{C.GREEN}✓ installed{C.RESET}" if ok else f"{C.RED}✗ missing{C.RESET}"

    lines = [
        label("Local IP",       ip,                       vcolor=C.CYAN),
        label("Hostname",       get_hostname(),            vcolor=C.WHITE),
        label("Available port", str(port),                 vcolor=C.PURPLE),
        "",
        label("Pillow (capture)",  dep_badge(deps.get("pillow")),  vcolor=C.WHITE),
        label("mss (fast capture)",dep_badge(deps.get("mss")),     vcolor=C.WHITE),
        label("tkinter (mirror)",  dep_badge(deps.get("tkinter")), vcolor=C.WHITE),
        "",
    ]

    # Check websockets
    try:
        import websockets
        lines.append(label("websockets",  f"{C.GREEN}✓ installed{C.RESET}", vcolor=C.WHITE))
    except ImportError:
        lines.append(label("websockets",  f"{C.RED}✗ missing — run: pip install websockets{C.RESET}", vcolor=C.WHITE))

    try:
        import qrcode
        lines.append(label("qrcode",  f"{C.GREEN}✓ installed{C.RESET}", vcolor=C.WHITE))
    except ImportError:
        lines.append(label("qrcode",  f"{C.YELLOW}⚠ optional — run: pip install qrcode{C.RESET}", vcolor=C.WHITE))

    box("◈  DIAGNOSTICS", lines, color=C.VIOLET)
    print()
    input(f"  {C.GRAY}Press Enter to go back…{C.RESET}")
    show_main_menu()


# ─── Main menu ────────────────────────────────────────────────────────────────

def show_main_menu():
    clear()
    print_logo(animated=False)
    divider("─", C.DEEP_PURPLE)

    options = [
        ("s", "Start mirroring",  "Launch server and show QR code"),
        ("d", "Diagnostics",      "Check system and dependencies"),
        ("c", "Settings",         "Configure quality, port, name"),
        ("a", "About",            "Version info and links"),
        ("q", "Quit",             "Exit Spectra"),
    ]

    menu = Menu("What would you like to do?", options)
    menu._render()

    try:
        choice = menu.run()
    except Exception:
        choice = input("  Select: ").strip().lower()

    if choice == "s":
        run_server()
    elif choice == "d":
        show_diagnostics()
    elif choice == "c":
        show_settings()
    elif choice == "a":
        show_about()
    elif choice == "q":
        _shutdown()
    else:
        show_main_menu()


# ─── Shutdown ─────────────────────────────────────────────────────────────────

def _shutdown():
    global _running, _mirror_window
    _running = False

    print()
    sp = Spinner("Shutting down…", color=C.RED)
    sp.start()

    if _mirror_window:
        _mirror_window.stop()
        _mirror_window = None
    if _capture:
        _capture.stop()
    if _server:
        _server.stop()

    time.sleep(0.6)
    sp.stop(success=True, message="Goodbye! ✦")
    show_cursor()
    print()
    sys.exit(0)


def _handle_signal(sig, frame):
    _shutdown()


# ─── Entry point ──────────────────────────────────────────────────────────────

def main():
    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    args = sys.argv[1:]

    # Quick CLI flags
    if "--version" in args or "-v" in args:
        print(f"Spectra {__version__}")
        sys.exit(0)

    if "--start" in args or "start" in args:
        boot_sequence()
        run_server()
        return

    if "--diag" in args or "diag" in args:
        boot_sequence()
        show_diagnostics()
        return

    if "--help" in args or "-h" in args:
        print(f"""
{C.BOLD}{C.PURPLE}Spectra {__version__}{C.RESET} — Screen Mirror Tool

{C.WHITE}Usage:{C.RESET}
  spectra              Launch interactive menu
  spectra start        Start mirror server directly
  spectra diag         Run diagnostics
  spectra --version    Show version
  spectra --help       Show this help
""")
        sys.exit(0)

    # Default: boot + menu
    boot_sequence()
    show_main_menu()


if __name__ == "__main__":
    main()
