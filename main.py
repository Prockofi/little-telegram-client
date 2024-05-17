from telethon import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest
from config import API_ID, API_HASH

client = TelegramClient("anon", API_ID, API_HASH)

async def main() -> None:
    pass

with client:
    client.loop.run_until_comlete(main())