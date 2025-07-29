from setuptools import setup, find_packages

setup(
    name='sinaweibo_mcp_server',  # 包名
    version='0.2',  # 版本号
    packages=find_packages(),  # 自动查找包
    install_requires=[  # 依赖项
        'requests',
        # 'selenium',
        # 'mcp',
        # 'mcpo'
    ],
    entry_points={
        'console_scripts': [
            'login_weibo = weibo_mcp_server:login',
            'weibo_mcp_server = weibo_mcp_server:main'
        ],
    },
    author='MengAlong',  # 作者
    author_email='alongmeng@gmail.com',  # 作者邮箱
    description='weibo mcp server',  # 描述
    long_description=open('README.md').read(),  # 长描述
    long_description_content_type='text/markdown',  # 长描述格式
    url='',  # 项目地址
    license='Apache2.0',  # 许可证
    python_requires='>=3.12'
)
