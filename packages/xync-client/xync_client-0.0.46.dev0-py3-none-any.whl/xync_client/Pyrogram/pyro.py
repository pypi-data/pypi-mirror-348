from asyncio import run, sleep

from pyrogram.errors import UserNotParticipant
from pyrogram.raw.functions.photos import GetUserPhotos
from pyrogram.raw.types.photos import Photos
from pyrogram.types import Chat, ChatPrivileges
from x_model import init_db

from xync_client.Pyrogram.client import UserClient, BotClient
from xync_client.Pyrogram.pg_storage import PgStorage
from xync_client.loader import TG_API_ID, TG_API_HASH, PG_DSN, TOKEN
from xync_schema import models


class PyroClient:
    max_privs = ChatPrivileges(
        can_manage_chat=True,  # default
        can_delete_messages=True,
        can_delete_stories=True,  # Channels only
        can_manage_video_chats=True,  # Groups and supergroups only
        can_restrict_members=True,
        can_promote_members=True,
        can_change_info=True,
        can_post_messages=True,  # Channels only
        can_post_stories=True,  # Channels only
        can_edit_messages=True,  # Channels only
        can_edit_stories=True,  # Channels only
        can_invite_users=True,
        can_pin_messages=True,  # Groups and supergroups only
        can_manage_topics=True,  # Supergroups only
        is_anonymous=True,
    )

    def __init__(self, ss_id: str):
        self.u: UserClient = UserClient(ss_id, TG_API_ID, TG_API_HASH, storage_engine=PgStorage(ss_id))
        self.b: BotClient = BotClient("6806432376", TG_API_ID, TG_API_HASH, storage_engine=PgStorage("6806432376"))

    async def create_orders_forum(self, uid: str | int) -> tuple[int, bool]:
        chat: Chat = await self.app.create_supergroup("Xync Orders", "Xync Orders")
        if not (await self.app.toggle_forum_topics(chat_id=chat.id, enabled=True)):
            await self.app.delete_channel(chat.id)
            await chat.leave()
            raise Exception(f"Chat {chat.id} for {self.app.me.username} not converted to forum")
        await chat.add_members(["XyncNetBot"])  # , "xync_bot"
        await chat.promote_member("XyncNetBot", self.max_privs)
        added = await chat.add_members([uid])
        try:
            await sleep(1, await chat.get_member(uid))
        except UserNotParticipant:
            added = False
        # await chat.leave()
        return chat.id, added

    async def get_user_photos(self, uid: str | int) -> Photos:
        try:
            peer = await self.app.resolve_peer(uid)
        except Exception as e:
            raise e
        return await self.app.invoke(GetUserPhotos(user_id=peer, offset=0, limit=1, max_id=-1))


async def main():
    _ = await init_db(PG_DSN, models, True)
    user: models.User = await models.User.filter(status__gt=0).first()
    bot = BotClient(TOKEN)
    await bot.start()
    uc = UserClient(str(user.username_id), bot)
    await uc.start()
    await uc.stop()
    await bot.stop()


if __name__ == "__main__":
    run(main())
