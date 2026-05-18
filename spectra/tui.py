"""
Spectra TUI - Terminal User Interface
Beautiful terminal interface with animations, colors and panels
"""

import sys
import time
import threading
import os
import shutil

# ─── ANSI Color codes ────────────────────────────────────────────────────────

class C:
    RESET       = "\033[0m"
    BOLD        = "\033[1m"
    DIM         = "\033[2m"
    ITALIC      = "\033[3m"

    # Purples / violets
    PURPLE      = "\033[38;5;129m"
    PURPLE_BG   = "\033[48;5;129m"
    VIOLET      = "\033[38;5;135m"
    LAVENDER    = "\033[38;5;183m"
    MAGENTA     = "\033[38;5;201m"
    PINK        = "\033[38;5;213m"
    DEEP_PURPLE = "\033[38;5;93m"
    LILAC       = "\033[38;5;177m"

    # UI colors
    WHITE       = "\033[97m"
    GRAY        = "\033[38;5;245m"
    DARK_GRAY   = "\033[38;5;238m"
    GREEN       = "\033[38;5;83m"
    RED         = "\033[38;5;196m"
    YELLOW      = "\033[38;5;220m"
    CYAN        = "\033[38;5;51m"
    ORANGE      = "\033[38;5;208m"

    # Backgrounds
    BG_BLACK    = "\033[40m"
    BG_DARK     = "\033[48;5;232m"
    BG_PURPLE   = "\033[48;5;54m"


def supports_color():
    return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()


def term_width():
    return shutil.get_terminal_size((80, 24)).columns


def term_height():
    return shutil.get_terminal_size((80, 24)).lines


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def hide_cursor():
    print("\033[?25l", end='', flush=True)


def show_cursor():
    print("\033[?25h", end='', flush=True)


def move_cursor(row, col):
    print(f"\033[{row};{col}H", end='', flush=True)


# ─── Logo ASCII ───────────────────────────────────────────────────────────────

LOGO_LINES = [
    "       .::::::..............................:::----:.       ",
    "    .---..                                        .:-+=.   ",
    "   =*-                                                -#+. ",
    " .++.                                                   =+.",
    ".=-                                                      :=",
    "--                                                        --",
    "-.                            ...::::..                   .-",
    ":.                       ..:::----==++*****-              .-",
    ":.                      .              :*##+              .-",
    ":.            .--::            -=:       ..:++.           .-",
    ":.          :--::             -*+           -+*=.         .-",
    ":.        :--::       .::    :*+  --:         :+*+:       .-",
    ":.      :--::      .:---:   .++.  :-=+=-:       :+*+:     .-",
    ":.    :--::     .---:.     .==.       :+*+=       -***.   .-",
    ":.     .::::     .::--:.   ==:     .:--=-:.     .-=++-    .:",
    ":.       .::-:       .:=- -=:     :-:.         :---:      .:",
    ":.         .:-=-         -=-                 .:::.        .:",
    ":.           .:-=..-:    .:                ....           .:",
    ":.             . .+*#*=:..    ......      .               .:",
    ":.                .---===--::...                          .:",
    "-.                                                        .:",
    "-.                                                        .-",
    "-:                                                        .-",
    ":=:                                                      .:.",
    " :+=                                                    .:. ",
    "  :*#-                                                 .:   ",
    "    :==:.                                           ...     ",
    "       ......                                    ..         ",
]


def print_logo(animated=True):
    """Print the Spectra logo with purple gradient animation"""
    w = term_width()

    gradient = [
        C.DEEP_PURPLE, C.PURPLE, C.VIOLET, C.LAVENDER,
        C.LILAC, C.LAVENDER, C.VIOLET, C.PURPLE,
        C.MAGENTA, C.PINK, C.MAGENTA, C.PURPLE,
    ]

    total = len(LOGO_LINES)
    for i, line in enumerate(LOGO_LINES):
        color = gradient[i % len(gradient)]
        centered = line.center(w)
        if animated:
            print(f"{C.BOLD}{color}{centered}{C.RESET}", flush=True)
            time.sleep(0.018)
        else:
            print(f"{C.BOLD}{color}{centered}{C.RESET}")

    # Title and version
    print()
    title = "✦  S P E C T R A  ✦"
    version = "v0.1.0  •  Screen Mirror"
    print(f"{C.BOLD}{C.MAGENTA}{title.center(w)}{C.RESET}")
    print(f"{C.DIM}{C.LAVENDER}{version.center(w)}{C.RESET}")
    print()


# ─── Box drawing helpers ──────────────────────────────────────────────────────

def box(title, lines, color=None, width=None):
    """Draw a beautiful rounded box with title"""
    color = color or C.PURPLE
    w = width or min(term_width() - 4, 70)
    inner = w - 2

    title_str = f" {title} "
    top = f"╭{'─' * ((inner - len(title_str)) // 2)}{title_str}{'─' * ((inner - len(title_str) + 1) // 2)}╮"

    print(f"{color}{top.center(term_width())}{C.RESET}")
    for line in lines:
        pad = inner - len(_strip_ansi(line))
        print(f"{color}│{C.RESET} {line}{' ' * max(0, pad - 1)}{color}│{C.RESET}".center(term_width() + len(color) + len(C.RESET) * 2))
    print(f"{color}╰{'─' * inner}╯{C.RESET}".center(term_width()))


def _strip_ansi(text):
    """Remove ANSI codes for length calculation"""
    import re
    return re.sub(r'\033\[[0-9;]*m', '', text)


def divider(char="─", color=None):
    color = color or C.DEEP_PURPLE
    w = term_width()
    print(f"{color}{char * w}{C.RESET}")


def label(text, value, lcolor=None, vcolor=None):
    lcolor = lcolor or C.GRAY
    vcolor = vcolor or C.WHITE
    return f"{lcolor}{text}{C.RESET}  {vcolor}{value}{C.RESET}"


def badge(text, color=None):
    color = color or C.PURPLE
    return f"{color}[{text}]{C.RESET}"


# ─── Spinner ──────────────────────────────────────────────────────────────────

class Spinner:
    FRAMES = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    PULSE  = ["◐","◓","◑","◒"]
    DOTS   = ["   ","·  ","·· ","···","·· ","·  "]

    def __init__(self, message="", style="pulse", color=None):
        self.message = message
        self.frames = self.PULSE if style == "pulse" else (
            self.DOTS if style == "dots" else self.FRAMES
        )
        self.color = color or C.PURPLE
        self._stop = threading.Event()
        self._thread = None

    def _spin(self):
        i = 0
        while not self._stop.is_set():
            frame = self.frames[i % len(self.frames)]
            print(f"\r  {self.color}{frame}{C.RESET}  {C.WHITE}{self.message}{C.RESET}   ", end='', flush=True)
            i += 1
            time.sleep(0.12)

    def start(self):
        hide_cursor()
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()
        return self

    def stop(self, success=True, message=None):
        self._stop.set()
        if self._thread:
            self._thread.join()
        msg = message or self.message
        icon = f"{C.GREEN}✓{C.RESET}" if success else f"{C.RED}✗{C.RESET}"
        print(f"\r  {icon}  {C.WHITE}{msg}{C.RESET}   ")
        show_cursor()


# ─── Progress bar ─────────────────────────────────────────────────────────────

def progress_bar(label, duration=1.5, color=None):
    color = color or C.PURPLE
    w = 30
    steps = 30
    for i in range(steps + 1):
        filled = int(w * i / steps)
        bar = "█" * filled + "░" * (w - filled)
        pct = int(100 * i / steps)
        print(f"\r  {C.GRAY}{label}{C.RESET}  {color}{bar}{C.RESET}  {C.WHITE}{pct}%{C.RESET}", end='', flush=True)
        time.sleep(duration / steps)
    print()


# ─── Status panel ─────────────────────────────────────────────────────────────

class StatusPanel:
    """Live updating status panel"""

    def __init__(self):
        self.status = {
            "server":   ("STOPPED",  C.RED),
            "network":  ("SCANNING", C.YELLOW),
            "clients":  ("0",        C.GRAY),
            "ip":       ("—",        C.GRAY),
            "port":     ("7799",     C.PURPLE),
            "mirroring":("IDLE",     C.GRAY),
        }
        self._lock = threading.Lock()

    def update(self, key, value, color=None):
        with self._lock:
            self.status[key] = (value, color or C.WHITE)

    def render(self):
        w = term_width()
        col_w = min(w - 4, 68)

        def row(k, label):
            val, color = self.status.get(k, ("—", C.GRAY))
            dots = "." * (24 - len(label))
            return f"  {C.GRAY}{label}{C.RESET}{C.DARK_GRAY}{dots}{C.RESET}{color}{val}{C.RESET}"

        lines = [
            row("server",    "Server"),
            row("ip",        "Local IP"),
            row("port",      "Port"),
            row("network",   "Network"),
            row("clients",   "Connected clients"),
            row("mirroring", "Mirroring"),
        ]
        box("◈  STATUS", lines, color=C.DEEP_PURPLE, width=col_w)


# ─── Menu ─────────────────────────────────────────────────────────────────────

class Menu:
    """Arrow-key navigable menu"""

    def __init__(self, title, options):
        self.title = title
        self.options = options  # list of (key, label, description)
        self.selected = 0

    def _render(self):
        w = term_width()
        print()
        print(f"{C.BOLD}{C.MAGENTA}  {self.title}{C.RESET}")
        print(f"  {C.DARK_GRAY}{'─' * 50}{C.RESET}")
        for i, (key, label, desc) in enumerate(self.options):
            if i == self.selected:
                arrow = f"{C.MAGENTA}▶{C.RESET}"
                k     = f"{C.BOLD}{C.PURPLE}[{key}]{C.RESET}"
                lbl   = f"{C.BOLD}{C.WHITE}{label}{C.RESET}"
                dsc   = f"{C.LAVENDER}{desc}{C.RESET}"
                bg    = f"{C.BG_PURPLE} {C.RESET}" if False else ""
            else:
                arrow = f"{C.DARK_GRAY} {C.RESET}"
                k     = f"{C.DARK_GRAY}[{key}]{C.RESET}"
                lbl   = f"{C.GRAY}{label}{C.RESET}"
                dsc   = f"{C.DARK_GRAY}{desc}{C.RESET}"
            print(f"  {arrow} {k} {lbl}  {dsc}")
        print(f"  {C.DARK_GRAY}{'─' * 50}{C.RESET}")
        print(f"  {C.DIM}{C.GRAY}↑↓ navigate  •  Enter / key to select  •  q to quit{C.RESET}")
        print()

    def run(self):
        """Run interactive menu, return selected key"""
        import tty
        import termios

        def getch():
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
                if ch == '\x1b':
                    ch2 = sys.stdin.read(1)
                    ch3 = sys.stdin.read(1)
                    return f"\x1b{ch2}{ch3}"
                return ch
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)

        hide_cursor()
        try:
            while True:
                # Clear previous render lines
                n = len(self.options) + 6
                print(f"\033[{n}A\033[J", end='')
                self._render()

                ch = getch()

                if ch == '\x1b[A':  # up
                    self.selected = (self.selected - 1) % len(self.options)
                elif ch == '\x1b[B':  # down
                    self.selected = (self.selected + 1) % len(self.options)
                elif ch in ('\r', '\n'):  # enter
                    return self.options[self.selected][0]
                elif ch == 'q':
                    return 'q'
                else:
                    # Check direct key press
                    for i, (key, _, _) in enumerate(self.options):
                        if ch.lower() == key.lower():
                            self.selected = i
                            return key
        except (ImportError, termios.error):
            # Windows fallback — simple input
            show_cursor()
            self._render()
            return input("  Select option: ").strip().lower()
        finally:
            show_cursor()


# ─── Notification helpers ─────────────────────────────────────────────────────

def success(msg):
    print(f"\n  {C.GREEN}✓{C.RESET}  {C.WHITE}{msg}{C.RESET}")

def error(msg):
    print(f"\n  {C.RED}✗{C.RESET}  {C.RED}{msg}{C.RESET}")

def info(msg):
    print(f"\n  {C.CYAN}ℹ{C.RESET}  {C.WHITE}{msg}{C.RESET}")

def warn(msg):
    print(f"\n  {C.YELLOW}⚠{C.RESET}  {C.YELLOW}{msg}{C.RESET}")

def section(title):
    print(f"\n  {C.BOLD}{C.VIOLET}◈  {title}{C.RESET}")
    print(f"  {C.DEEP_PURPLE}{'─' * (len(title) + 5)}{C.RESET}\n")
