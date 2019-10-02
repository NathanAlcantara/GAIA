import json
import os
import requests
from boto3 import client

TELEGRAM_TOKEN = os.environ['BotToken']
URL = "https://api.telegram.org/bot{}/".format(TELEGRAM_TOKEN)


def publish_sns(message, topic_arn):
    sns_client = client('sns')
    sns_client.publish(
        TopicArn=topic_arn,
        Message=json.dumps(message)
    )


def get_block_text(block):
    if 'Text' in block:
        return block['Text']


def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    requests.get(url)


def lambda_handler(event, context):
    email_dump_arn = os.environ['EmailDumpARN']
    message = json.loads(event['Records'][0]['Sns']['Message'])

    job_id = message['JobId']
    file_name = message['DocumentLocation']['S3ObjectName']
    textract_client = client('textract')
    response = textract_client.get_document_analysis(
        JobId=job_id
    )

    # Extrai lista de blocos
    blocks = response['Blocks']

    # Extrai tabelas
    tables = [block for block in blocks if block['BlockType'] == 'TABLE']

    # Extrai blocos de célula que contém texto
    tables_rels_list = [[rel_list for rel_list in table['Relationships']] for table in tables]

    tables_childs_ids = [
        [relationship['Ids'] for relationship in rel_list]
        for rel_list in tables_rels_list
    ]

    tables_childs_blocks = [
        [block for block in blocks if block['Id'] in child_ids]
        for relationships in tables_childs_ids for child_ids in relationships
    ]

    cells_with_text = [
        [cell for cell in child_list if 'Relationships' in cell] for child_list in tables_childs_blocks
    ]

    # Extrai e lista textos das células
    cells_rels_list = [
        [
            [rel_list for rel_list in cell['Relationships']]
            for cell in table
        ] for table in cells_with_text
    ]

    cells_childs_ids = [
        [[relationship['Ids'] for relationship in cell]
         for cell in table
         ] for table in cells_rels_list
    ]

    cells_child_blocks = [
        [
            [
                [block for block in blocks if block['Id'] in child_ids]
                for relationship in cell for child_ids in relationship
            ] for cell in table
        ] for table in cells_childs_ids
    ]

    cells_text_blocks = [
        [
            [
                [block for block in child_blocks if 'Text' in block]
                for child_blocks in cell
            ] for cell in table
        ] for table in cells_child_blocks
    ]

    cells_texts = [
        [
            [block['Text'] for text_blocks in cell for block in text_blocks]
            for cell in table
        ] for table in cells_text_blocks
    ]

    # Montar texto da tabela
    tables_texts = [
        [': '.join(text_list) for text_list in table] for table in cells_texts
    ]

    # Identificar nome e número da prova

    prova_number = ''.join([
        cell_text[1]
        for table in cells_texts for cell_text in table
        if 'Prova' in cell_text
    ])

    prova_name = ''.join([
        cell_text[1]
        for table in cells_texts for cell_text in table
        if 'Nome' in cell_text
    ])

    # Envia uma mensagem com o nome e número da prova
    # Essa etapa é temporária, apenas para debug, por isso o chat_id harcoded
    message = f'Nome da prova: {prova_name} \n' \
              f'Número da prova: {prova_number}'
    send_message(message, '54337384')
