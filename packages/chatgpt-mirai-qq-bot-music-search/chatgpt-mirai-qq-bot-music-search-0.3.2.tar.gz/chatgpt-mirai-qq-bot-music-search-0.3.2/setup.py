from setuptools import setup, find_packages
import io
import os

version = os.environ.get('RELEASE_VERSION', '0.3.2'
'').lstrip('v')

setup(
    name="chatgpt-mirai-qq-bot-music-search",
    version=version,
    packages=find_packages(),
    include_package_data=True,  # 这行很重要
    package_data={
        "music_search": ["example/*.yaml", "example/*.yml"],
    },
    install_requires=[
        "beautifulsoup4","kirara-ai>=3.2.0"
    ],
    entry_points={
        'chatgpt_mirai.plugins': [
            'music_search = music_search:MusicSearchPlugin'
        ]
    },
    author="chuanSir",
    author_email="416448943@qq.com",

    description="MusicSearchPlugin for lss233/chatgpt-mirai-qq-bot",
    long_description=io.open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/chuanSir123/music_search",
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: GNU Affero General Public License v3',
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/chuanSir123/music_search/issues",
        "Documentation": "https://github.com/chuanSir123/music_search/wiki",
        "Source Code": "https://github.com/chuanSir123/music_search",
    },
    python_requires=">=3.8",
)
