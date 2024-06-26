
from telethon import TelegramClient
from telethon.tl.types import User, Channel, Chat
from telethon.tl.functions.users import GetFullUserRequest
from config import API_ID, API_HASH

client = TelegramClient("anon", API_ID, API_HASH)

def return_errors(error: str) -> None:
    errors = {
        "1": "\nВведён некоректный номер чата, либо отсутствует подключение к интернету",
        "2": "\nВведён некоректный номер чата",
        "3": "\nВведён некоректный id пользователя",
        "4": "\nПользователя с введённым id не найдено"
    }
    print("\nОшибка:", errors[error])
    return True

async def get_chat_names(chat: list) -> list:
    names = {}
    chat_metadata = await client.get_entity(chat[0])
    if (type(chat_metadata) == Channel) and (chat_metadata.to_dict()["megagroup"] == True):
        for name in await client.get_participants(chat[0]):
            names[name.id] = name.first_name
    if type(chat_metadata) == Chat:
        for name in await client.get_participants(chat[0]):
            names[name.id] = name.first_name
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
                    mess_count = int(input("\nЧисло сообщений: "))
                    line_break = 0
                    for item in list(names.items()):
                        if line_break % 5 == 0:
                            print()
                        print(item[1] + ': ' + str(item[0]), end=',  ')
                        line_break += 1
                    print(f"\n\nЧат { chats[chat_id - 1][1] }")
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
                                        try:
                                            if data["media"]["video"] != False:
                                                media += "video~"
                                        except:
                                            pass
                                        try:
                                            if data["media"]["voice"] != False:
                                                media += "voice~"
                                        except:
                                            pass
                                        try:
                                            if data["media"]["round"] != False:
                                                media += "round~"
                                        except:
                                            pass
                                        try:
                                            if data["media"]["photo"] != False:
                                                media += "photo~"
                                        except:
                                            pass
                                        try:
                                            if data["media"]["document"] != False:
                                                if data["media"]["document"]["mime_type"] == "image/webp" or data["media"]["document"]["mime_type"] == "video/webp":
                                                    media += "sticker~"
                                                elif data["media"]["document"]["mime_type"] == "":
                                                    media += '"' + data["media"]["document"]["attributes"][0]["file_name"] + '"~'
                                        except:
                                            pass
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
            flag = True
            try:
                user_id = int(input("\nВведите id пользователя: "))
            except:
                return_errors("3")
                flag = False
            if flag:
                message = input("\nВведите текст сообщения: ")
                t = input("\nВы действительно хотите отправить сообщение (Да/нет): ")
                if t.lower() == 'да':
                    try:
                        await client.send_message(user_id, message)
                    except ValueError:
                        return_errors("4")
        elif x == "3":
            chats = await get_chats()
        elif x == "4":
            break


with client:
    client.loop.run_until_complete(main())