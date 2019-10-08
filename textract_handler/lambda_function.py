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

    # Extrai blocos de palavras
    word_blocks = [block for block in blocks if block['BlockType'] == 'WORD']

    # Extrai blocos de células
    cell_blocks = [block for block in blocks if block['BlockType'] == 'CELL']

    # Extrai blocos de tabelas
    table_blocks = [block for block in blocks if block['BlockType'] == 'TABLE']

    # Carrega as palavras em células com texto
    def list_cell_words(cell):
        words = []
        if 'Relationships' in cell:
            for rel in cell['Relationships']:
                for child_id in rel['Ids']:
                    block = list(filter(lambda block: block['Id'] == child_id, word_blocks))
                    if len(block) > 0:
                        words.append(block[0]['Text'])
        cell['Words'] = words
        return cell

    cells_and_texts = list(map(list_cell_words, cell_blocks))

    # Lista células com a palavra 'Nome'
    filtered_cells = list(filter(lambda cell: 'Nome' in cell['Words'], cells_and_texts))

    # Caso haja mais de uma célula, então seleciona aquela que está mais acima na página
    if len(filtered_cells) > 1:
        filtered_cells = list(filter(lambda cell: cell['Page'] == 1, filtered_cells))
        filtered_cells = sorted(filtered_cells, key=lambda cell: cell['Geometry']['BoundingBox']['Top'])

    # Registra célula que pertence a tabela de descrição
    name_cell = filtered_cells[0]

    # Encontra a tabela de informações pela célula de nome
    def find_table_by_cell(table):
        if 'Relationships' in table:
            for rel in table['Relationships']:
                return name_cell['Id'] in rel['Ids']

    info_table = list(filter(find_table_by_cell, table_blocks))[0]

    # Carrega as células com texto da tabela
    def load_table_cells(table):
        result = []
        for rel in table['Relationships']:
            for child_id in rel['Ids']:
                cell = list(filter(lambda cell: cell['Id'] == child_id, cells_and_texts))[0]
                result.append(cell)
        return result

    info_cells = load_table_cells(info_table)

    # Carrega os dados em um dicionário
    def find_info_data(info):
        # Identifica a célula com o texto procurado e carrega toda a coluna
        temp_cell = list(filter(lambda cell: info in cell['Words'], info_cells))[0]
        cells = list(filter(lambda cell: cell['ColumnIndex'] == temp_cell['ColumnIndex'], info_cells))
        # Necessário considerar os casos onde as linhas vêm mescladas em uma célula por erro do textract
        if len(cells) == 1:
            result = ''.join(list(filter(lambda word: word != info, temp_cell['Words'])))
            result = result.replace(info, '')
        # E os casos onde o texto vem em células distintas, nesse caso necessário excluir a célula de cabeçalho
        else:
            cells = list(filter(lambda cell: cell['Id'] != temp_cell['Id']))
            result = ''.join(list(map(lambda cell: ''.join(cell['Words'], cells))))
        return result.strip()

    header = dict(Nome=find_info_data('Nome'),
                  Prova=find_info_data('Prova'),
                  HoraLancamento=' '.join([find_info_data('Data Lancamento'), find_info_data('Hora Lancamento')]),
                  HoraEntrega=' '.join([find_info_data('Data Entrega'), find_info_data('Hora Entrega')]))
