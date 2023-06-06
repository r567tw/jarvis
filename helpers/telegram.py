import requests
import os

def send(message):
    bot_token = os.getenv("TELEGRAM_TOKEN")
    bot_chatID = os.getenv("TELEGRAM_ChatID")
    notify_url  = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + message

    response = requests.get(notify_url)
    # print(response.json())
    result = response.json()
    if result["ok"]:
        return True
    else:
        return False
