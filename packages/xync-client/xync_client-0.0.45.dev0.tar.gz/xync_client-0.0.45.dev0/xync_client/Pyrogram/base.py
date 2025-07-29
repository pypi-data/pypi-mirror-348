from asyncio import sleep
from typing import Literal

from pyrogram import Client
from pyrogram.filters import chat
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message

from xync_client.Pyrogram.storage import PgStorage
from xync_client.loader import TG_API_ID, TG_API_HASH

AuthTopic = Literal["phone", "code", "pass"]


class BaseClient(Client):
    storage: PgStorage

    def __init__(self, name: str, *args, **kwargs):
        super().__init__(
            name,
            TG_API_ID,
            TG_API_HASH,
            storage_engine=PgStorage(name),
            # device_model="iPhone 17 Air", app_version="XyncNet 1.0", system_version="iOS 19.0.1",
            *args,
            **kwargs,
        )

    async def wait_from(self, uid: int, topic: str, past: int = 0, timeout: int = 10) -> str:
        handler = MessageHandler(self.got_msg, chat(uid))
        self.add_handler(handler)
        while past < timeout:
            if txt := self.storage.session.state.get(uid, {}).pop(topic, None):
                self.remove_handler(handler)
                return txt
            await sleep(1)
            past += 1
            return await self.wait_from(uid, topic, past, timeout)

    async def got_msg(self, _, msg: Message):
        if topic := self.storage.session.state.get(msg.from_user.id, {}).pop("waiting_for", None):
            self.storage.session.state[msg.from_user.id][topic] = msg.text
