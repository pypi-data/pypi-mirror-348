import time

from weibo_mcp_server.weibo_mcp_server.weibo_control  import WeiboPoster

current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

if __name__ == '__main__':
    poster = WeiboPoster()
    poster.login("13002910813")
    poster.login_to_publish("这是一条测试微博，我看看效果怎么样"+current_time)
