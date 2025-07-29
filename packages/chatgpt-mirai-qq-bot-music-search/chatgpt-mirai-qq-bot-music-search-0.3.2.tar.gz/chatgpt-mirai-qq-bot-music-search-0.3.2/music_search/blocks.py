from typing import Any, Dict, List, Optional, Annotated
from kirara_ai.workflow.core.block import Block, Input, Output, ParamMeta
from kirara_ai.im.message import IMMessage, TextMessage, VoiceMessage
from kirara_ai.im.sender import ChatSender
from .music_searcher import MusicSearcher
import asyncio
from kirara_ai.logger import get_logger
from kirara_ai.ioc.container import DependencyContainer

logger = get_logger("MusicSearch")

def get_options_provider(container: DependencyContainer, block: Block) -> List[str]:
    return ["酷美", "网易", "qq", "酷狗", "咪咕"]
class MusicSearchBlock(Block):
    """音乐搜索Block"""
    name = "music_search"
    description = "通过歌曲名称搜索音乐或歌词"

    inputs = {
        "music_name": Input(name="music_name", label="歌曲名", data_type=str, description="歌曲名称"),
        "singer": Input(name="singer", label="歌手", data_type=str, description="歌手名称", nullable=True, default=""),
        "source": Input(name="source", label="歌曲来源", data_type=str, description="歌曲来源，来源列表如下['酷美', '网易', 'qq', '酷狗', '咪咕']", nullable=True, default="网易"),
    }

    outputs = {
        "music_url": Output(name="music_url", label="音乐URL", data_type=str, description="音乐URL"),
        "lyrics": Output(name="lyrics", label="歌词", data_type=str, description="歌词")
    }

    def __init__(self, source: Annotated[Optional[str],ParamMeta(label="来源", description="要使用的音乐平台", options_provider=get_options_provider),] = "网易",):
        super().__init__()
        self.searcher = MusicSearcher()
        self.source = source

    def execute(self, **kwargs) -> Dict[str, Any]:
        music_name = kwargs.get("music_name", "")
        singer = kwargs.get("singer", "")
        source = kwargs.get("source", self.source)
        logger.info(f"搜索歌曲: {music_name} - {singer} - {source}")
        try:
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            logger.info(f"asyncio搜索歌曲: {music_name} - {singer} - {source}")
            result = loop.run_until_complete(
                self.searcher._play_music({
                    "music_name": music_name,
                    "singer": singer,
                    "source": source
                })
            )
            return {
                "music_url": result["music_url"],
                "lyrics": result["lyrics"]
            }
        except Exception as e:
            return {
                "music_url": "",
                "lyrics": f"搜索失败: {str(e)}"
            }

class MusicUrlToIMMessage(Block):
    """音乐URL转IMMessage"""
    name = "music_url_to_im_message"
    container: DependencyContainer
    inputs = {
        "music_url": Input("music_url", "音乐URL", str, "音乐URL"),
        "lyrics": Input("lyrics", "歌词", str, "歌词")
    }
    outputs = {"msg": Output("msg", "IM消息", IMMessage, "IM消息")}
    def __init__(self):
        self.split_by = ","
    def execute(self, music_url: str, lyrics: str) -> Dict[str, Any]:
        message_elements = []
        if music_url and music_url.startswith("http"):
            message_elements.append(VoiceMessage(music_url))
        if lyrics:
            message_elements.append(TextMessage(f"歌词:\n{lyrics}"))

        return {"msg": IMMessage(sender=ChatSender.get_bot_sender(), message_elements=message_elements)}
