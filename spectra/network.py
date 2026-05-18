"""
Spectra Network utilities
Local IP detection, QR code generation, port management
"""

import socket
import json
import os
import platform


def get_local_ip() -> str:
    """Get the machine's local network IP address"""
    try:
        # Connect to an external address (doesn't actually send data)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def get_hostname() -> str:
    return socket.gethostname()


def is_port_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) != 0


def find_free_port(start=7799) -> int:
    port = start
    while not is_port_free(port) and port < 7900:
        port += 1
    return port


def build_connection_payload(ip: str, port: int, name: str = None) -> dict:
    return {
        "app":    "spectra",
        "v":      "1",
        "ip":     ip,
        "port":   port,
        "pcName": name or get_hostname(),
    }


def generate_qr(data: str, colorful: bool = True) -> list[str]:
    """
    Generate a QR code as ASCII art lines for terminal display.
    Uses pure Python — no external qr library needed for basic display.
    Falls back to showing the connection string if qr libs not available.
    """
    try:
        import qrcode
        from qrcode.image.pure import PyPNGImage

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=1,
            border=1,
        )
        qr.add_data(data)
        qr.make(fit=True)

        matrix = qr.get_matrix()
        lines = []
        for row in matrix:
            line = ""
            for cell in row:
                line += "██" if cell else "  "
            lines.append(line)
        return lines

    except ImportError:
        # Fallback: show text box
        lines = [
            "┌─────────────────────────────────┐",
            "│  QR library not installed.       │",
            "│  Run:  pip install qrcode        │",
            "│                                  │",
            f"│  Manual connect:                 │",
            f"│  {data[:32]:<32}│",
            "└─────────────────────────────────┘",
        ]
        return lines


def print_qr_panel(ip: str, port: int, pc_name: str):
    """Print the full QR panel for terminal display"""
    from spectra.tui import C, term_width

    payload = build_connection_payload(ip, port, pc_name)
    json_str = json.dumps(payload)

    qr_lines = generate_qr(json_str)

    w = term_width()
    qr_w = len(qr_lines[0]) if qr_lines else 40
    pad = max(0, (w - qr_w) // 2)
    margin = " " * pad

    print(f"\n{C.BOLD}{C.WHITE}{'Scan with Spectra app'.center(w)}{C.RESET}\n")

    for i, line in enumerate(qr_lines):
        # Color QR modules purple
        colored = line.replace("██", f"{C.PURPLE}██{C.RESET}")
        print(f"{margin}{colored}")

    print()
    print(f"{C.DIM}{C.GRAY}{'or connect manually:'.center(w)}{C.RESET}")
    print(f"{C.BOLD}{C.LAVENDER}{f'{ip}:{port}'.center(w)}{C.RESET}\n")
