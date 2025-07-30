import httpx
import aiofiles
from tikhub import Client

from app.utils.helper import check_api_key
from app.providers.video_providers.video_provider import VideoProvider
from app.models.video_downloader import VideoModel


class TikTokProvider(VideoProvider):
    """TikTok 视频解析器"""
    def __init__(self):
        super().__init__()
        self.api_key = check_api_key("TIKHUB_API_KEY")

    async def get_video_info(self, url) -> VideoModel:
        """
        解析 TikTok 视频信息

        Args:
            url (str): TikTok 视频链接
        Returns:
            VideoModel: 解析后的视频信息模型
        """
        # self.console.print(f"[green]Parsing TikTok video info from {url}...[/green]")
        client = Client(api_key=self.api_key)

        try:
            video_info = await client.TikTokAppV3.fetch_one_video_by_share_url(url)
            
            # with open("tiktok_video_info.json", "w") as f:
            #     json.dump(video_info, f, indent=4)

            row = video_info["data"]["aweme_details"][0]
            result = {
                "title": row["desc"],
                "download_url": row["video"]["play_addr_h264"]["url_list"][0],
                "play_url": row["video"]["play_addr_h264"]["url_list"][0],
                "duration": int(row["video"]["duration"]),
                "author": row["author"]["nickname"]
            }
            
            return result
        
        except KeyError as e:
            self.console.print(f"[red]Error parsing TikTok video info: {e}[/red]")
            raise ValueError(f"Failed to parse TikTok video info: {e}")

    async def download_video(self, download_url, output_path):
        """
        下载 TikTok 视频

        Args:
            download_url (str): TikTok 视频下载链接
            output_path (str): 下载后保存的文件路径
        """
        self.console.print(f"[green]Downloading TikTok video from {download_url}...[/green]")
        
        # httpx.AsyncClient()方法默认超时时间为5秒，此处需要更多的超时时间来等待执行结束
        async with httpx.AsyncClient(timeout=30.0) as http_client:
            try:
                response = await http_client.get(download_url)
                response.raise_for_status()  # 检查响应状态 | Check response status
            except httpx.HTTPStatusError as e:
                self.console.print(f"[red]Error downloading video: {e.response.status_code}[/red]")
                raise ValueError(f"Failed to download video: {e}")
            except Exception as e:
                self.console.print(f"[red]Unexpected error: {e}[/red]")
                raise

        # 保存文件 | Save file
        async with aiofiles.open(output_path, "wb") as file:
            await file.write(response.content)

        return output_path

    