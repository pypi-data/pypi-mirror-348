import typer
from funutil import getLogger

from .coder_server import CodeServerInstall
from .go import GoInstall
from .new_api import NewApiInstall
from .nodejs import NodeJSInstall

logger = getLogger("funinstall")


app = typer.Typer()


@app.command(name="code-server")
def install_coder_server() -> bool:
    return CodeServerInstall().install()


@app.command(name="go")
def install_go(
    version: str = typer.Option(None, "--version", "-v", help="Go 版本"),
) -> bool:
    return GoInstall(version=version).install()


@app.command(name="new-api")
def install_new_api() -> bool:
    return NewApiInstall().install()


@app.command(name="nodejs")
def install_nodejs(
    version: str = typer.Option(None, "--version", "-v", help="nodejs 版本"),
    lasted: bool = typer.Option(False, "--lasted", "-l", help="是否安装最新版本"),
    update: bool = typer.Option(False, "--update", "-u", help="是否更新版本"),
) -> bool:
    return NodeJSInstall().install()
