from xync_client.Pyrogram.base import AuthTopic

from xync_client.Pyrogram.base import BaseClient


class BotClient(BaseClient):
    def __init__(self, token: str):
        super().__init__(token.split(":")[0], bot_token=token)

    async def wait_auth_from(self, uid: int, topic: AuthTopic, past: int = 0, timeout: int = 60) -> str:
        return await super().wait_from(uid, topic, past, timeout)
