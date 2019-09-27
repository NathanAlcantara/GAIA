import json
import os
from botocore.vendored import requests

TELE_TOKEN = os.environ['BotToken']
URL = "https://api.telegram.org/bot{}/".format(TELE_TOKEN)


def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    requests.get(url)


def lambda_handler(event, context):
    message = json.loads(event['body'])
    chat_id = message['message']['chat']['id']
    file_id = message['message']['document']['file_id']
    file_name = message['message']['document']['file_name']
    reply = 'chat id: ' + chat_id + '\n'
    reply += 'file id:' + file_id + '\n'
    reply += 'file name:' + file_name
    send_message(reply, chat_id)
    return {
        'statusCode': 200
    }
