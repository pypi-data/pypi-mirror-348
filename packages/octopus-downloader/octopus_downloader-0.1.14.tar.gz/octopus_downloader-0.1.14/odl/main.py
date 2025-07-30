import typer
import os
import secrets
import asyncio
import json
import importlib.metadata

from dotenv import load_dotenv
from typing import Optional
from pathlib import Path
from rich.console import Console

from odl.utils.helper import set_api_key, check_api_key, response_json
from odl.models.video_downloader import VideoDownloaderOptions
from odl.providers.video import ProviderFactory


# 当前运行环境
run_env = "development"

# 加载环境变量
# 如果在 GitHub Actions 环境中运行，直接加载默认的 .env 文件
# 否则，在本地开发环境中显式加载当前目录下的 .env 文件
if "RUNNER_TEMP" in os.environ:
    load_dotenv()
    run_env = "production"
else:
    load_dotenv(dotenv_path=".env")

# 初始化命令行器
app = typer.Typer(
    name="odl",
    help="A command line tool for downloading files from Octopus Deploy.",
    rich_markup_mode="rich",
    add_completion=False
)

console = Console()

@app.command("info")
def info(url: str = typer.Argument(..., help="The URL of the video playback page.")):
    """
    Get video information from the provided URL.
    """
    async def async_info():
        try:
            provider = ProviderFactory.create_provider(url)
            video_info = await provider.get_video_info(url)
            result = response_json("success", "Video information retrieved successfully.", video_info)

            return result
            
        except Exception as e:
            result = response_json("error", str(e), {})
            return result

    result = asyncio.run(async_info())
    print(json.dumps(result, indent=4))
    return result


@app.command("download")
def download(
    url: str = typer.Argument(..., help="The URL of the file to download."),
    output_dir: Path = typer.Argument(..., help="The directory to save the downloaded file."),
    filename: Optional[str] = typer.Option(None, "--filename", "-f", help="The name of the downloaded file.")
):
    """
    Download a file from the provided URL.
    This command will download the file and save it to the specified output directory.
    
    Args:
        url (str): The URL of the file to download.
        output_dir (str): The directory to save the downloaded file.
        filename (str): The name of the downloaded file.
    """
    if not output_dir.exists():
        try:
            # 下载路径不存在则自动创建
            Path(output_dir).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise Exception(f"Create download path failed: {e}")

    if not filename:
        filename = secrets.token_urlsafe(8) + ".mp4"

    options = VideoDownloaderOptions(
        url=url,
        output_dir=output_dir,
        filename=filename
    )

    output_file = os.path.join(output_dir, filename)

    async def async_download():
        try:
            provider = ProviderFactory.create_provider(url)

            video_info = await provider.get_video_info(url)
            if not video_info:
                raise Exception(f"Parsed video information failed: {url}")
            
            await provider.download_video(video_info['download_url'], output_file)

        except Exception as e:
            raise Exception(f"{e}")
    
    asyncio.run(async_download())
    print(f"Completed! Save as {output_file}")


@app.command("setenv")
def setenv(
    key: str = typer.Argument(..., help="The name of the environment variable."),
    value: str = typer.Argument(..., help="The value of the environment variable.")
):
    """
    Set an environment variable.
    
    Args:
        key (str): The name of the environment variable.
        value (str): The value of the environment variable.
    """
    if not key or not value:
        console.print("[red]Key and value cannot be empty.[/red]")
        raise typer.Exit(code=1)

    try:
        set_api_key(key, value)
        console.print(f"[green]Environment variable {key} set to {value}.[/green]")
    except Exception as e:
        console.print(f"[red]Error setting environment variable: {e}[/red]")
        raise typer.Exit(code=1)
    
@app.command("checkenv")
def checkenv(
    key: str = typer.Argument(..., help="The name of the environment variable.")
):
    """
    Check if an environment variable is set.
    
    Args:
        key (str): The name of the environment variable.
    """
    if not key:
        console.print("[red]Key cannot be empty.[/red]")
        raise typer.Exit(code=1)

    try:
        api_key = check_api_key(key)
        console.print(f"[green]Environment variable {key} has been set.[/green]")
    except ValueError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=1)
    
def get_version():
    """获取当前已发布的版本号"""
    try:
        return importlib.metadata.version("octopus-downloader")
    except importlib.metadata.PackageNotFoundError:
        return "unknown"

@app.callback(invoke_without_command=True)
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the version and exit",
        is_eager=True
    )
):
    if version:
        print(get_version())
        raise typer.Exit()


if __name__ == "__main__":
    app()