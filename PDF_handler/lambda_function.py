import json
import os
import requests
from boto3 import client

TELEGRAM_TOKEN = os.environ['BotToken']
URL = 'https://api.telegram.org/bot{}/'.format(TELEGRAM_TOKEN)


def lambda_handler(event, context):
    message = json.loads(event['Records'][0]['Sns']['Message'])
    document = message['document']
    file_id = document['file_id']
    file_name = document['file_name']

    # Requisita o link do arquivo para o telegram
    url = URL + 'getFile?file_id={}'.format(file_id)
    response = requests.get(url).json()
    file_path = response['result']['file_path']

    # Requisita o arquivo para o telegram
    url = URL + file_path
    file = requests.get(url, stream=True).content

    # Salva o arquivo no bucket
    s3_client = client('s3')
    bucket_name = os.environ['BucketName']
    s3_client.put_object(Body=file, Bucket=bucket_name, Key=file_name)

    # Solicita ao textract análise do documento

    # Grava mensagem na pilha SQS
