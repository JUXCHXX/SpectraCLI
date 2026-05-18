"""
Spectra Mirror Window
Real-time phone screen display in a floating tkinter window
"""

import queue
import threading
import time
from typing import Optional


class MirrorWindow:
    """
    Floating tkinter window for displaying phone screen frames in real time.
    Reads frames from a thread-safe queue and renders with FPS/latency metrics.
    """

    def __init__(self, frame_queue: Optional[queue.Queue] = None):
        self.frame_queue = frame_queue if frame_queue else queue.Queue(maxsize=2)
        self.running = False
        self.window = None
        self.label = None
        self.thread = None
        self.fps_counter = 0
        self.fps_display = 0
        self.fps_timer = time.time()
        self.latency_ms = 0

    def _create_window(self):
        """Create and configure the tkinter window"""
        try:
            import tkinter as tk
            from PIL import Image, ImageTk

            root = tk.Tk()
            root.title("Spectra Mirror")
            root.geometry("400x700")
            root.attributes("-topmost", True)
            root.resizable(True, True)

            label = tk.Label(root, bg="black")
            label.pack(fill=tk.BOTH, expand=True)

            return root, label
        except ImportError:
            return None, None

    def start(self):
        """Start the mirror window in a separate thread"""
        if self.running:
            return
        self.running = True

        def run_window():
            try:
                import tkinter as tk
                from PIL import Image, ImageTk

                self.window, self.label = self._create_window()
                if not self.window:
                    self.running = False
                    return

                def update_frame():
                    """Poll queue and update frame every 30ms"""
                    if not self.running:
                        self.window.quit()
                        return

                    try:
                        img = self.frame_queue.get_nowait()

                        w = self.window.winfo_width()
                        h = self.window.winfo_height()
                        if w > 1 and h > 1:
                            img = img.resize((w, h), Image.LANCZOS)

                        photo = ImageTk.PhotoImage(img)
                        self.label.config(image=photo)
                        self.label.image = photo

                        self.fps_counter += 1
                        if time.time() - self.fps_timer >= 1.0:
                            self.fps_display = self.fps_counter
                            self.fps_counter = 0
                            self.fps_timer = time.time()

                    except queue.Empty:
                        pass

                    self._update_title()
                    self.window.after(33, update_frame)

                update_frame()
                self.window.mainloop()
            except Exception:
                pass
            finally:
                self.running = False

        self.thread = threading.Thread(target=run_window, daemon=True)
        self.thread.start()

    def set_latency(self, latency_ms: int):
        """Update ping latency display"""
        self.latency_ms = latency_ms

    def _update_title(self):
        """Update window title with FPS and latency"""
        if self.window:
            title = f"Spectra Mirror | {self.fps_display}fps | {self.latency_ms}ms"
            try:
                self.window.title(title)
            except Exception:
                pass

    def stop(self):
        """Stop and close the mirror window"""
        self.running = False
        if self.window:
            try:
                self.window.quit()
                self.window.destroy()
            except Exception:
                pass
        self.window = None
        self.label = None
