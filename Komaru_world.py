
from random import choice

from telethon.tl.types import (
    InputMessagesFilterGif,
    InputMessagesFilterPhotos,
    InputMessagesFilterVideo,
    Message,
)

from .. import loader, utils


class KomaruMod(loader.Module):
    """Random picture/video/gif from the @komaru_world"""

    strings = {
        "name": "Komaru world",
        "choosing": "<emoji document_id=5328311576736833844>🔴</emoji> Choosing {}...",
        "gif": "gif",
        "video": "video",
        "photo": "photo",
    }

    strings_ru = {
        "choosing": "<emoji document_id=5328311576736833844>🔴</emoji> Подбираем {}...",
        "gif": "ваш гиф",
        "video": "ваше видео",
        "photo": "вашу картинку",
    }

    SEARCH_TYPES = {
        InputMessagesFilterGif: "gif",
        InputMessagesFilterPhotos: "photo",
        InputMessagesFilterVideo: "video",
    }

    @loader.command(ru_doc="- подобрать рандом картинку(пикчу)/видео/гиф")
    async def kw(self, message: Message):
        """- choose a random picture/gif/video"""
        search_type = choice(
            [
                InputMessagesFilterGif,
                InputMessagesFilterPhotos,
                InputMessagesFilterVideo,
            ]
        )
        search_type_str = self.strings(self.SEARCH_TYPES[search_type])

        msg = await utils.answer(
            message, self.strings("choosing").format(search_type_str)
        )

        chosed_msg = choice(
            [
                message_in_channel
                async for message_in_channel in self.client.iter_messages(
                    "komaru_world", limit=400, filter=search_type
                )
            ]
        )

        reply = await message.get_reply_message()
        if reply:
            reply = reply.id
        else:
            reply = None

        return await utils.answer_file(
            msg,
            chosed_msg,
            chosed_msg.text or "<b>Подобрал " + search_type_str + ".</b>",
            reply_to=reply,
        )