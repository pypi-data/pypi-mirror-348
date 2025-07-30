import os

from funbuild.shell import run_shell, run_shell_list
from funutil import getLogger

from .base import BaseInstall

logger = getLogger("funinstall")


class NewApiInstall(BaseInstall):
    def __init__(self, overwrite=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.overwrite = overwrite

    def install_linux(self, *args, **kwargs) -> bool:
        """
        使用一键脚本安装new-api
        https://docs.newapi.pro/installation/local-development/#_6
        """
        root = f"{os.environ.get('HOME')}/opt"
        if not os.path.exists(root):
            logger.info(f"创建目录{root}")
            os.mkdir(root)
        newapi_root = f"{root}/newapi"
        if os.path.exists(newapi_root) and not self.overwrite:
            logger.info(f"目录{newapi_root}已存在，删除")
            run_shell(f"rm -rf {newapi_root}")
        if not os.path.exists(newapi_root):
            logger.info(f"克隆项目到{newapi_root}")
            run_shell_list(
                [
                    f"cd {root}",
                    "rm -rf newapi",
                    "git clone https://github.com/Calcium-Ion/new-api.git newapi",
                ]
            )
        logger.info("构建前端")
        run_shell_list(
            [
                f"cd {newapi_root}/web",
                "npm install",
                'export NODE_OPTIONS="--max-old-space-size=8192"',
                "npm run build",
            ]
        )
        logger.info("构建后端")
        run_shell_list(
            [
                f"cd {newapi_root}",
                "go mod download",
                "cp .env.example .env",
                "go build -o newapi.sh",
                "bash ./newapi.sh",
            ]
        )
        return True
