import concurrent
import os
import requests
import tempfile
import time

from mcp.server import FastMCP
from mcp.types import TextContent

try:
    from weibo_control import WeiboPoster
except ImportError:
    from .weibo_control import WeiboPoster

mcp = FastMCP("weibo")
phone = os.getenv("phone", "")
path = os.getenv("json_path", "/tmp")


def login():
    poster = WeiboPoster(path)
    poster.login(phone)
    time.sleep(1)
    poster.close()

def download_image(url):
    local_filename = url.split('/')[-1]
    temp_dir = tempfile.gettempdir()

    local_path = os.path.join(temp_dir, local_filename)  # 假设缓存地址为/tmp
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_path

def download_images_parallel(urls):
    """
    并行下载图片到本地缓存地址
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(download_image, urls))
    return results

@mcp.tool()
def post_weibo(content: str, images: list) -> list[TextContent]:
    """
    发布微博。

    Args:
        content (str): 要发布的微博内容。
        images (list): 要发布的图片列表。

    Returns:
        list[TextContent]: 包含发布结果的列表。

    Raises:
        异常: 如果在登录或发布过程中发生异常，则返回包含错误信息的TextContent对象。

    """

    poster = WeiboPoster(path)
    res = ""
    try:
        if len(images)>0 and images[0].startswith("http"):
            # 使用并行下载图片
            print("downloading images...")
            local_images = download_images_parallel(images)
        else:
            local_images = images

        code, info = poster.login_to_publish(content, local_images)
        poster.close()
        res = info
    except Exception as e:
        res = "error:" + str(e)

    return [TextContent(type="text", text=res)]


def main():
    mcp.run()


if __name__ == "__main__":
    main()
