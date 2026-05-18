"""
Spectra WebSocket Server
Handles connections from the Spectra mobile app
"""

import asyncio
import json
import time
import threading
from typing import Callable, Optional


class SpectraServer:
    """
    WebSocket server that the mobile app connects to.
    Handles screen frame sending and control event receiving.
    """

    def __init__(
        self,
        ip: str,
        port: int,
        on_client_connect: Optional[Callable] = None,
        on_client_disconnect: Optional[Callable] = None,
        on_message: Optional[Callable] = None,
    ):
        self.ip = ip
        self.port = port
        self.on_client_connect = on_client_connect
        self.on_client_disconnect = on_client_disconnect
        self.on_message = on_message

        self.clients: set = set()
        self.running = False
        self._server = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None
        self.stats = {
            "connected_at": None,
            "frames_sent": 0,
            "bytes_sent": 0,
            "messages_received": 0,
        }

    async def _handler(self, websocket):
        """Handle a new WebSocket connection"""
        client_addr = websocket.remote_address
        self.clients.add(websocket)
        self.stats["connected_at"] = time.time()

        if self.on_client_connect:
            self.on_client_connect(client_addr)

        try:
            # Send welcome handshake
            await websocket.send(json.dumps({
                "type": "welcome",
                "server": "spectra",
                "version": "0.1.0",
                "pcName": "Spectra PC",
            }))

            async for raw in websocket:
                self.stats["messages_received"] += 1
                try:
                    data = json.loads(raw)
                    if self.on_message:
                        self.on_message(client_addr, data)
                except json.JSONDecodeError:
                    pass

        except Exception:
            pass
        finally:
            self.clients.discard(websocket)
            if self.on_client_disconnect:
                self.on_client_disconnect(client_addr)

    async def _start_async(self):
        try:
            import websockets
            self._server = await websockets.serve(
                self._handler,
                self.ip,
                self.port,
                ping_interval=20,
                ping_timeout=10,
            )
            self.running = True
            await self._server.wait_closed()
        except ImportError:
            raise RuntimeError(
                "websockets library not installed.\n"
                "Run: pip install websockets"
            )

    def start_background(self):
        """Start server in background thread"""
        self._loop = asyncio.new_event_loop()

        def run():
            asyncio.set_event_loop(self._loop)
            self._loop.run_until_complete(self._start_async())

        self._thread = threading.Thread(target=run, daemon=True)
        self._thread.start()

        # Wait for server to actually start
        for _ in range(30):
            if self.running:
                break
            time.sleep(0.1)

    def stop(self):
        """Stop the server"""
        if self._server and self._loop:
            self._loop.call_soon_threadsafe(self._server.close)
        self.running = False

    async def _broadcast_async(self, data: dict):
        if not self.clients:
            return
        message = json.dumps(data)
        dead = set()
        for ws in self.clients.copy():
            try:
                await ws.send(message)
                self.stats["frames_sent"] += 1
                self.stats["bytes_sent"] += len(message)
            except Exception:
                dead.add(ws)
        self.clients -= dead

    def broadcast(self, data: dict):
        """Send data to all connected clients"""
        if self._loop and self.running:
            asyncio.run_coroutine_threadsafe(
                self._broadcast_async(data),
                self._loop
            )

    def send_frame(self, frame_b64: str, width: int, height: int):
        """Send a screen frame to all clients"""
        self.broadcast({
            "type": "frame",
            "data": frame_b64,
            "w": width,
            "h": height,
            "ts": time.time(),
        })

    def send_latency_ping(self):
        """Send a ping for latency measurement"""
        self.broadcast({"type": "ping", "ts": time.time()})

    @property
    def client_count(self) -> int:
        return len(self.clients)

    def get_stats(self) -> dict:
        stats = dict(self.stats)
        stats["client_count"] = self.client_count
        stats["uptime"] = (
            time.time() - stats["connected_at"]
            if stats["connected_at"] else 0
        )
        return stats
