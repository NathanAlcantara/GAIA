import json
import os
import requests
from boto3 import client

TELEGRAM_TOKEN = os.environ['BotToken']
BOT_URL = 'https://api.telegram.org/bot{}/'.format(TELEGRAM_TOKEN)
FILE_URL = 'https://api.telegram.org/file/bot{}/'.format(TELEGRAM_TOKEN)
BUCKET_NAME = os.environ['BucketName']


def get_telegram_file(file_id):
    # Requisita o link do arquivo para o telegram
    url = BOT_URL + 'getFile?file_id={}'.format(file_id)
    response = requests.get(url).json()
    file_path = response['result']['file_path']

    # Requisita o arquivo para o telegram
    url = FILE_URL + file_path
    return requests.get(url).content


def salvar_arquivo_s3(file, file_name):
    s3_client = client('s3')
    s3_client.put_object(Body=file, Bucket=BUCKET_NAME, Key=file_name)


def iniciar_analise_textract(file_name):
    textract_client = client('textract')
    sns_topic_arn = os.environ['TextractSNSTopicARN']
    role_arn = os.environ['TextractSNSRoleARN']

    doc_location = {
        'S3Object': {
            'Bucket': BUCKET_NAME,
            'Name': file_name
        }
    }

    feature_types = [
        'TABLES',
        'FORMS'
    ]

    notification_channel = {
        'RoleArn': role_arn,
        'SNSTopicArn': sns_topic_arn
    }

    return textract_client.start_document_analysis(
        DocumentLocation=doc_location,
        FeatureTypes=feature_types,
        NotificationChannel=notification_channel
    )


def publicar_mensagem_sqs(file_name, job_id):
    sqs_queue_url = os.environ['SQSQueueTextractURL']
    sqs_client = client('sqs')
    message_body = {
        'job_id': job_id,
        'file_name': file_name
    }
    client.send_message(
        QueueUrl=sqs_queue_url,
        MessageBody=json.dumps(message_body)
    )


def lambda_handler(event, context):
    message = json.loads(event['Records'][0]['Sns']['Message'])
    document = message['document']
    file_id = document['file_id']
    file_name = document['file_name']

    # Faz o download do arquivo
    file = get_telegram_file(file_id)

    # Salva o arquivo no bucket
    salvar_arquivo_s3(file, file_name)
    del file

    # Solicita ao textract análise do documento
    response = iniciar_analise_textract(file_name)
    job_id = response['JobId ']

    # Publica a mensagem na fila do SQS
    publicar_mensagem_sqs(file_name, job_id)

    return job_id
