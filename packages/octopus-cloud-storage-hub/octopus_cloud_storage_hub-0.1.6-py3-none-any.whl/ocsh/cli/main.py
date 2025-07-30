"""命令行主模块"""

import json
import typer
from pathlib import Path

from ocsh.handlers.oss import OssHandler
from ocsh.config import OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET, OSS_ENDPOINT, OSS_BUCKET_NAME


app = typer.Typer(
    name = "ocsh",
    help = "Octopus Cloud Storage Hub CLI",
    add_completion = False
)

oss_handler = OssHandler(
    access_key_id = OSS_ACCESS_KEY_ID,
    access_key_secret = OSS_ACCESS_KEY_SECRET,
    endpoint = OSS_ENDPOINT,
    bucket_name = OSS_BUCKET_NAME
)

@app.command("upload")
def upload(
    object_name: str = typer.Argument(..., help="Cloud object name"),
    file_path: Path = typer.Argument(..., help="Local file path")
):
    """
    上传文件
    """
    result = oss_handler.upload(object_name, file_path)
    print(json.dumps(result, indent=4))
    return result

@app.command("download")
def download(
    object_name: str = typer.Argument(..., help="Cloud object name"),
    file_path: Path = typer.Argument(..., help="Local file path")
):
    """
    下载文件
    """
    oss_handler.download(object_name, file_path)

@app.command("delete")
def delete(object_name: str = typer.Argument(..., help="Cloud object name")):
    """
    删除云存储文件
    """
    oss_handler.delete(object_name)

if __name__ == "__main__":
    app()
