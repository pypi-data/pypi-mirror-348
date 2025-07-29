from pyrogram import enums
from pyrogram.errors import BadRequest, SessionPasswordNeeded, AuthKeyUnregistered
from pyrogram.types import Message, User, SentCode

from pyro_client.client.base import BaseClient, AuthTopic
from pyro_client.client.bot import BotClient


class UserClient(BaseClient):
    bot: BotClient

    def __init__(self, name: str, api_id: str, api_hash: str, bot_token: str = None, proxy: dict = None,
                 device: str = "iPhone 17 Air", app: str = "XyncNet 1.0", ver: str = "iOS 19.0.1"):
        super().__init__(name, api_id, api_hash, device_model=device, app_version=app, system_version=ver)
        self.bot = bot_token and BotClient(api_id, api_hash, bot_token)

    async def start(self, use_qr: bool = False, except_ids: list[int] = None):
        await self.bot.start()
        await super().start(use_qr=use_qr, except_ids=except_ids or [])

    async def ask_for(self, topic: AuthTopic, question: str) -> str:
        await self.bot.send_message(self.storage.me_id, question)
        self.bot.storage.session.state[self.storage.me_id] = {"waiting_for": topic}
        return await self.bot.wait_auth_from(self.storage.me_id, topic)

    async def receive(self, txt: str, photo: bytes = None, video: bytes = None) -> Message:
        return await self.bot.send(txt, self.me.id, photo, video)

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

    async def stop(self, block: bool = True):
        await super().stop(block)
        await self.bot.stop(block)


async def main():
    from x_auth import models
    from x_model import init_db

    from pyro_client.loader import WSToken, PG_DSN, TOKEN, API_ID, API_HASH

    _ = await init_db(PG_DSN, models, True)
    await models.Proxy.load_list(WSToken)
    session = await models.Session.filter(is_bot=False).order_by("-date").first()
    uc = UserClient("", API_ID, API_HASH, TOKEN)
    # try:
    await uc.start()
    await uc.receive("hi")
    # except Exception as e:
    #     print(e.MESSAGE)
    #     await uc.send(e.MESSAGE)
    #     await uc.storage.session.delete()
    # finally:
    await uc.stop()


if __name__ == "__main__":
    from asyncio import run

    run(main())
