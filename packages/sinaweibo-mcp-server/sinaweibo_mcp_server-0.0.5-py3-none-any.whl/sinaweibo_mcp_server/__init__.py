from . import weibo_server

def main():
    """Main entry point for the package."""
    weibo_server.main()

def login():
    """Login entry point for the package."""
    weibo_server.login()

# Expose important items at package level
__all__ = ['main', 'weibo_server', 'login']