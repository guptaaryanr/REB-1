from __future__ import annotations
import socket


def default_host() -> str:
    try:
        return socket.gethostname()
    except Exception:
        return "unknown-host"
