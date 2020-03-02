import json
import requests
from boto3 import client
from awsHelper import OK_RESPONSE, ERROR_RESPONSE, publishSnsTopic, Telegram_Token


def get_telegram_file(file_id):
    telegram_token = Telegram_Token
    bot_url = 'https://api.telegram.org/bot{}/'.format(telegram_token)
    file_url = 'https://api.telegram.org/file/bot{}/'.format(telegram_token)

    # Requisita o link do arquivo para o telegram
    url = bot_url + 'getFile?file_id={}'.format(file_id)
    response = requests.get(url).json()
    file_path = response['result']['file_path']

    # Requisita o arquivo para o telegram
    url = file_url + file_path
    return requests.get(url).content


def save_file_s3(file, file_name, bucket_name):
    #TODO transferir client para layer
    s3_client = client('s3')
    s3_client.put_object(Body=file, Bucket=bucket_name, Key=file_name)


def lambda_handler(event, context):
    message_input = json.loads(event['Records'][0]['Sns']['Message'])
    chat_id = message_input['chatId']
    document = message_input['document']
    bucket = message_input['bucket']
    file_id = document['fileId']
    file_name = document['fileName']

    # Faz o download do arquivo
    file = get_telegram_file(file_id)

    # Salva o arquivo no bucket
    save_file_s3(file, file_name, bucket)
    del file

    if 'target_sns' in message_input:
        target_sns = message_input['targetSns']
        output = []
        output['status'] = 200
        publishSnsTopic(chat_id, output, target_sns)