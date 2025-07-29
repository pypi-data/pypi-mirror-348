from pyro_client.client.base import BaseClient, AuthTopic


class BotClient(BaseClient):
    def __init__(self, api_id: str, api_hash: str, token: str):
        super().__init__(token.split(":")[0], api_id, api_hash, bot_token=token)

    async def wait_auth_from(self, uid: int, topic: AuthTopic, past: int = 0, timeout: int = 60) -> str:
        return await super().wait_from(uid, topic, past, timeout)
