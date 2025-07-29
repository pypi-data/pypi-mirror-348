import os
import time

from mcp.server import FastMCP
from mcp.types import TextContent

from .weibo_control import WeiboPoster

mcp = FastMCP("weibo")
phone = os.getenv("phone", "")
path = os.getenv("json_path", "/tmp")


def login():
    poster = WeiboPoster(path)
    poster.login(phone)
    time.sleep(1)
    poster.close()

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
        code, info = poster.login_to_publish(content, images)
        poster.close()
        res = info
    except Exception as e:
        res = "error:" + str(e)

    return [TextContent(type="text", text=res)]


def main():
    mcp.run()


if __name__ == "__main__":
    main()
