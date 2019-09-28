import json
import os
import requests

TELE_TOKEN = os.environ['BotToken']
URL = "https://api.telegram.org/bot{}/".format(TELE_TOKEN)


def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    requests.get(url)


def lambda_handler(event, context):
    body = json.loads(event['body'])
    if 'message' in body:
        message = body['message']
        chat_id = message['chat']['id']
        reply = 'chat id: ' + str(chat_id) + '\n'
        if 'document' in message:
            document = message['document']
            file_id = document['file_id']
            file_name = document['file_name']
            reply += 'file id:' + file_id + '\n'
            reply += 'file name:' + file_name
    else:
        reply = 'ainda não sei lidar com esse tipo de mensagem'
    send_message(reply, chat_id)
    return {
        'statusCode': 200
    }
