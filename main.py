
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
    # Желательно переделать на условную конструкцию с проверкой на то является ли чат группой
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
    count = 1
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
                  "\n4) Выход\n")
        if x == "1":
            try:
                chat_id = int(input("\nВведите номер чата: "))
                if 0 < chat_id < len(chats):
                    names = await get_chat_names(chats[chat_id - 1])
                    print(names)
                    mess_count = int(input("\nЧисло сообщений: "))
                    print(f"\nЧат { chats[chat_id - 1][1] }")
                    result = []
                    count = 0
                    async for message in client.iter_messages(chats[chat_id - 1][0]):
                        text = ""
                        media = ""
                        if count < mess_count:
                            data = message.to_dict()
                            if data["_"] == "Message":
                                from_id = str(data["peer_id"][list(data["peer_id"].keys())[1]])
                                try:
                                    if data["from_id"] != None:
                                        from_id = str(data["from_id"][list(data["from_id"].keys())[1]])
                                except:
                                    pass
                                try:
                                    text += names[int(from_id)]
                                except:
                                    text += chats[chat_id - 1][1]
                                text += " > " + data["message"]
                                try:
                                    if data["media"] != None:
                                        media = "~document~"
                                        if data["media"]["video"] != False:
                                            media += "video~"
                                        if data["media"]["voice"] != False:
                                            media += "voice~"
                                        if data["media"]["round"] != False:
                                            media += "round~"
                                        if data["media"]["document"] != False:
                                            if data["media"]["document"]["mime_type"] == "image/webp" or data["media"]["document"]["mime_type"] == "video/webp":
                                                media += "sticker~"
                                            elif data["media"]["document"]["mime_type"] == "":
                                                media += '"' + data["media"]["document"]["attributes"][0]["file_name"] + '"~'
                                    text += media
                                except:
                                    pass
                                result.append(text)
                            count += 1
                        else:
                            break
                    result = '\n'.join(result[::-1])
                    print(result)
                else:
                    return_errors("2")
            except:
                return_errors("1")
        elif x == "2":
            user_id = int(input("\nВведите id чата: "))
            message = input("\nВведите текст сообщения: ")
            t = input("\nВы действительно хотите отправить сообщение (Да/нет)")
            if t.lower() == 'да':
                await client.send_message(user_id, message)
        elif x == "3":
            chats = await get_chats()
        elif x == "4":
            break


with client:
    client.loop.run_until_complete(main())