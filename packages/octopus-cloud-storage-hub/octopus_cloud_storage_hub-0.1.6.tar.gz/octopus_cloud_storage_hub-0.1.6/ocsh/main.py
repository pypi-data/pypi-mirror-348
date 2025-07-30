"""命令行主模块"""

import typer
from pathlib import Path
from rich.console import Console
from ocsh.handlers.oss import OssHandler
from ocsh.config import OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET, OSS_ENDPOINT, OSS_BUCKET_NAME


app = typer.Typer(
    name = "Octopus Cloud Storage Hub",
    help = "Octopus Cloud Storage Hub CLI",
    rich_markup_mode="rich",
    add_completion = False
)

@app.command("upload")
def upload(
    object_name: str = typer.Argument(..., help="Cloud object name"),
    file_path: Path = typer.Argument(..., help="Local file path")
):
    """
    上传文件

    Args:
        object_name: 云存储对象名称
        file_path: 本地文件路径
    """
    pass

@app.command("download")
def download(
    object_name: str = typer.Argument(..., help="Cloud object name"),
    file_path: Path = typer.Argument(..., help="Local file path")
):
    """
    下载文件
    """
    pass

@app.command("delete")
def delete(object_name: str = typer.Argument(..., help="Cloud object name")):
    """
    删除云存储文件
    """
    pass

if __name__ == "__main__":
    app()
