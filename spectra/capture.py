"""
Spectra Screen Capture
Cross-platform screen capture with compression for streaming
"""

import base64
import io
import platform
import threading
import time
from typing import Optional, Tuple


class ScreenCapture:
    """
    Captures the PC screen and encodes frames for WebSocket streaming.
    Supports Windows, macOS, and Linux.
    """

    QUALITY_PRESETS = {
        "low":    {"quality": 40, "scale": 0.4, "fps": 15},
        "medium": {"quality": 60, "scale": 0.6, "fps": 24},
        "high":   {"quality": 80, "scale": 0.8, "fps": 30},
        "ultra":  {"quality": 90, "scale": 1.0, "fps": 60},
    }

    def __init__(self, quality: str = "medium"):
        self.quality_name = quality
        self.preset = self.QUALITY_PRESETS.get(quality, self.QUALITY_PRESETS["medium"])
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._on_frame = None
        self.stats = {"fps_actual": 0, "frames_captured": 0}
        self._system = platform.system()

    def _capture_frame(self) -> Optional[Tuple[bytes, int, int]]:
        """Capture a single screen frame. Returns (jpeg_bytes, width, height)"""
        try:
            import PIL.ImageGrab as ImageGrab
            from PIL import Image

            img = ImageGrab.grab()

            # Scale down
            scale = self.preset["scale"]
            if scale < 1.0:
                w = int(img.width * scale)
                h = int(img.height * scale)
                img = img.resize((w, h), Image.LANCZOS)

            # Compress to JPEG
            buf = io.BytesIO()
            img.convert("RGB").save(buf, format="JPEG", quality=self.preset["quality"])
            return buf.getvalue(), img.width, img.height

        except ImportError:
            return self._fallback_frame()
        except Exception as e:
            return None

    def _fallback_frame(self) -> Optional[Tuple[bytes, int, int]]:
        """Fallback frame when PIL not available"""
        try:
            if self._system == "Darwin":
                import subprocess
                result = subprocess.run(
                    ["screencapture", "-x", "-t", "jpg", "/tmp/spectra_frame.jpg"],
                    capture_output=True, timeout=1
                )
                if result.returncode == 0:
                    with open("/tmp/spectra_frame.jpg", "rb") as f:
                        data = f.read()
                    return data, 1920, 1080
        except Exception:
            pass
        return None

    def capture_single(self) -> Optional[dict]:
        """Capture one frame and return as dict with base64 data"""
        result = self._capture_frame()
        if result:
            raw, w, h = result
            return {
                "data": base64.b64encode(raw).decode(),
                "w": w,
                "h": h,
                "ts": time.time(),
            }
        return None

    def start_streaming(self, on_frame):
        """Start continuous capture loop, calling on_frame(frame_dict) each frame"""
        self._on_frame = on_frame
        self._running = True

        def loop():
            target_delay = 1.0 / self.preset["fps"]
            last_time = time.time()
            frame_count = 0
            fps_timer = time.time()

            while self._running:
                t0 = time.time()
                frame = self.capture_single()
                if frame and self._on_frame:
                    self._on_frame(frame)
                    frame_count += 1
                    self.stats["frames_captured"] += 1

                # FPS counter
                if time.time() - fps_timer >= 1.0:
                    self.stats["fps_actual"] = frame_count
                    frame_count = 0
                    fps_timer = time.time()

                # Maintain target FPS
                elapsed = time.time() - t0
                sleep = max(0, target_delay - elapsed)
                time.sleep(sleep)

        self._thread = threading.Thread(target=loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)

    def set_quality(self, quality: str):
        self.quality_name = quality
        self.preset = self.QUALITY_PRESETS.get(quality, self.QUALITY_PRESETS["medium"])

    @staticmethod
    def check_dependencies() -> dict:
        """Check which capture backends are available"""
        results = {}
        try:
            from PIL import ImageGrab
            results["pillow"] = True
        except ImportError:
            results["pillow"] = False

        try:
            import mss
            results["mss"] = True
        except ImportError:
            results["mss"] = False

        try:
            import tkinter
            results["tkinter"] = True
        except ImportError:
            results["tkinter"] = False

        return results
