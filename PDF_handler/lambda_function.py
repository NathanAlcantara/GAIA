import json
import os
import requests
from boto3 import client

TELEGRAM_TOKEN = os.environ['BotToken']
BOT_URL = 'https://api.telegram.org/bot{}/'.format(TELEGRAM_TOKEN)
FILE_URL = 'https://api.telegram.org/file/bot{}/'.format(TELEGRAM_TOKEN)
BUCKET_NAME = os.environ['BucketName']


def lambda_handler(event, context):
    message = json.loads(event['Records'][0]['Sns']['Message'])
    document = message['document']
    file_id = document['file_id']
    file_name = document['file_name']

    # Requisita o link do arquivo para o telegram
    url = BOT_URL + 'getFile?file_id={}'.format(file_id)
    response = requests.get(url).json()
    file_path = response['result']['file_path']

    # Requisita o arquivo para o telegram
    url = FILE_URL + file_path
    file = requests.get(url).content

    # Salva o arquivo no bucket
    s3_client = client('s3')
    s3_client.put_object(Body=file, Bucket=BUCKET_NAME, Key=file_name)

    # Solicita ao textract análise do documento
    textract_client = client('textract')

    doc_location = {
        'S3Object': {
            'Bucket': BUCKET_NAME,
            'Name': file_name
        }
    }
    feature_types = [
        "TABLES",
        "FORMS"
    ]

    sns_topic_arn = os.environ['TextractSNSTopicARN']
    role_arn = os.environ['TextractSNSRoleARN']
    job_tag = file_name
    notification_channel = {
        'RoleArn': role_arn,
        'SNSTopicArn': sns_topic_arn
    }

    response = textract_client.start_document_analysis(
        DocumentLocation=doc_location,
        FeatureTypes=feature_types,
        JobTag=job_tag,
        NotificationChannel=notification_channel
    )
