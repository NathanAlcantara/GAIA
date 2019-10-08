import json
import os
import logging
from boto3 import client
from telegram import Bot

AWS_REGION = os.environ.get('REGION')
AWS_ACCOUNT_ID = os.environ.get('ACCOUNT_ID')
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

bot = Bot(TELEGRAM_TOKEN)

OK_RESPONSE = {
    'statusCode': 200,
    'headers': {'Content-Type': 'application/json'},
    'body': json.dumps('ok')
}
ERROR_RESPONSE = {
    'statusCode': 400,
    'body': json.dumps('Oops, something went wrong!')
}

# Logging is cool!
logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logging.basicConfig(level=logging.INFO)


def publishSnsTopic(chatId, message, snsName='send-telegram-response'):

    sns_client = client('sns')

    body = json.dumps({
        'chatId': chatId,
        'message': message
    })

    logger.info("Publicando mensagem: " + body + ", no sns: '" + snsName + "'")

    arnSNS = "arn:aws:sns" + AWS_REGION + AWS_ACCOUNT_ID + ":" + snsName

    params = {
        'Message': body,
        'TopicArn': arnSNS
    }

    return sns_client.publish(params)
