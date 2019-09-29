import json
import os
import requests
from boto3 import client

TELEGRAM_TOKEN = os.environ['BotToken']
URL = "https://api.telegram.org/bot{}/".format(TELEGRAM_TOKEN)


def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    requests.get(url)


def publish_sns_pdf(message):
    topic_arn = os.environ['PDFTopicARN']
    sns_client = client('sns')
    sns_client.publish(
        TopicArn=topic_arn,
        Message=json.dumps(message)
    )


def lambda_handler(event, context):
    body = json.loads(event['body'])
    if 'message' in body:
        message = body['message']
        chat_id = message['chat']['id']
        reply = 'Chat id: ' + str(chat_id) + '\n'
        if 'document' in message:
            document = message['document']
            file_id = document['file_id']
            file_name = document['file_name']
            if document['mime_type'] == 'application/pdf':
                # Disparar aviso para SNS de PDFs
                publish_sns_pdf(message)
            reply += 'File id:' + file_id + '\n'
            reply += 'File name:' + file_name
        else:
            reply += 'Ainda não sei lidar com esse tipo de mensagem'
        send_message(reply, chat_id)
    return {
        'statusCode': 200
    }
