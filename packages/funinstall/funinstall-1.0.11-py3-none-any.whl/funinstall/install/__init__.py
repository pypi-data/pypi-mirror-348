from .command import app as install_app
from .coder_server import install_code_server
from .go import install_go
from .new_api import install_newapi
from .nodejs import install_nodejs

__all__ = [
    "install_app",
    "install_go",
    "install_nodejs",
    "install_newapi",
    "install_code_server",
]
