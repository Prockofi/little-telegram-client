
from telethon import TelegramClient
from telethon.tl.functions.users import GetFullUserRequest
from config import API_ID, API_HASH

client = TelegramClient("anon", API_ID, API_HASH)

def return_errors(error: str) -> None:
    errors = {
        "1": "Введён некоректный номер чата, либо отсутствует подключение к интернету",
        "2": "Введён некоректный номер чата",
    }
    print("Ошибка:", errors[error])
    return True

async def get_chat_names(chat: list) -> list:
    names = {}
    #
    # Желательно переделать на условную конструкцию с проверкой является ли чат группой
    #
    try:
        for name in await client.get_participants(chat[0]):
            names[name.id] = name.first_name
    except:
        names[chat[0]] = chat[1]
    me = (await client(GetFullUserRequest("me"))).to_dict()
    names[me["full_user"]["id"]] = me["users"][0]["first_name"]
    return names

async def get_chats() -> list:
    count = 0
    chats = []
    print("~ ~ ~ Список чатов ~ ~ ~")
    async for chat in client.iter_dialogs():
        print(f"{ count }) { chat.name }")
        chats.append([chat.id, chat.name])
        count += 1
    print("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")
    return chats

async def main() -> None:
    chats = await get_chats()
    while True:
        x = input("\n1) Посмотреть чат"
                  "\n2) Отправить сообщение"
                  "\n3) Обновить чаты"
                  "\n4) Выход")
        if x == "1":
            try:
                chat_id = int(input("\nВведите номер чата: "))
                if 0 < chat_id < len(chats):
                    names = await get_chat_names(chats[chat_id - 1])
                    print(names)
                else:
                    return_errors("2")
            except:
                return_errors("1")
        elif x == "2":
            pass
        elif x == "3":
            pass
        elif x == "4":
            break


with client:
    client.loop.run_until_complete(main())