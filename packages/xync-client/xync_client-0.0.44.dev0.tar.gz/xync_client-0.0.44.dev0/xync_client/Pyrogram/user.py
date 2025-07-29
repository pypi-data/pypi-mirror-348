from pyrogram import enums
from pyrogram.errors import BadRequest, SessionPasswordNeeded, AuthKeyUnregistered
from pyrogram.types import Message, User, SentCode

from xync_client.Pyrogram.base import BaseClient, AuthTopic
from xync_client.Pyrogram.bot import BotClient
from xync_client.loader import WSToken


class UserClient(BaseClient):
    bot: BotClient

    def __init__(self, name: str, bot: BotClient, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.bot = bot

    async def ask_for(self, topic: AuthTopic, question: str) -> str:
        await self.bot.send_message(self.storage.me_id, question)
        self.bot.storage.session.state[self.storage.me_id] = {"waiting_for": topic}
        return await self.bot.wait_auth_from(self.storage.me_id, topic)

    async def send(self, txt: str) -> Message:
        return await self.bot.send_message(self.storage.me_id, txt)

    async def authorize(self, sent_code: SentCode = None) -> User:
        sent_code_desc = {
            enums.SentCodeType.APP: "Telegram app",
            enums.SentCodeType.SMS: "SMS",
            enums.SentCodeType.CALL: "phone call",
            enums.SentCodeType.FLASH_CALL: "phone flash call",
            enums.SentCodeType.FRAGMENT_SMS: "Fragment SMS",
            enums.SentCodeType.EMAIL_CODE: "email code",
        }
        # Step 1: Phone
        if not self.phone_number:
            try:
                self.phone_number = await self.ask_for("phone", "Your phone:")
                if not self.phone_number:
                    await self.authorize()
                sent_code = await self.send_code(self.phone_number)
            except BadRequest as e:
                await self.send(e.MESSAGE)
                self.phone_number = None
                return await self.authorize(sent_code)
        # Step 2: Code
        if not self.phone_code:
            _ = await self.ask_for("code", f"The confirm code sent via {sent_code_desc[sent_code.type]}")
            self.phone_code = _.replace("_", "")
            try:
                signed_in = await self.sign_in(self.phone_number, sent_code.phone_code_hash, self.phone_code)
            except BadRequest as e:
                await self.send(e.MESSAGE)
                self.phone_code = None
                return await self.authorize(sent_code)
            except SessionPasswordNeeded as e:
                # Step 2.1?: Cloud password
                await self.send(e.MESSAGE)
                while True:
                    self.password = await self.ask_for("pass", f"Enter pass: (hint: {await self.get_password_hint()})")
                    try:
                        return await self.check_password(self.password)
                    except BadRequest as e:
                        await self.send(e.MESSAGE)
                        self.password = None

            if isinstance(signed_in, User):
                await self.send("✅")
                return signed_in

            if not signed_in:
                await self.send("No registered such phone number")


async def main():
    from x_model import init_db
    from xync_schema import models
    from xync_client.loader import PG_DSN, TOKEN

    _ = await init_db(PG_DSN, models, True)
    _ = await models.Proxy.load_list(WSToken)
    bot = BotClient(TOKEN)
    await bot.start()
    uc = UserClient(
        "7049542242",
        bot,
        proxy=dict(
            scheme="socks5", hostname="207.244.217.165", port=6712, username="hmxelnzd", password="zaw8ied2qdjc"
        ),
    )
    try:
        await uc.start()
    except AuthKeyUnregistered as e:
        print(e.MESSAGE)
        await uc.send(e.MESSAGE)
        await uc.storage.session.delete()
    else:
        await uc.stop()
    await bot.stop()


if __name__ == "__main__":
    from asyncio import run

    run(main())
