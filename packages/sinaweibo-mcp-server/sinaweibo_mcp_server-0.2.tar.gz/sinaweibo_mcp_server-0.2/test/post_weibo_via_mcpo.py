import time

import requests

current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

def create_note(base_url, content, image_paths=""):

    url = f"{base_url}/post_weibo"
    payload = {
        "content": content,
        "images": []
    }

    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    return resp.json()

if __name__ == '__main__':
    base_url = "http://0.0.0.0:8007/weibo-mcp-server"
    create_note(base_url, "测试发布一个新微博"+current_time, "")