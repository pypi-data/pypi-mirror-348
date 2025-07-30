# Expose main objects if needed, or leave empty
from .server import mcp
from .settings import settings

__all__ = ["mcp", "settings"]