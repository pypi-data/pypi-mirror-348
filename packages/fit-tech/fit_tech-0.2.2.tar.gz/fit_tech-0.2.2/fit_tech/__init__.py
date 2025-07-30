__version__ = "0.2.2"
from .app.main import app
from .app.core.config import settings

__all__ = [
    "__version__",
    "app",
    "settings",
]
