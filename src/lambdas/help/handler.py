import json
import sys
import logging
import unicodedata
from awsHelper import OK_RESPONSE, ERROR_RESPONSE, publishSnsTopic
from textHelper import removerEspeciais, alphabet_position

logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logging.basicConfig(level=logging.INFO)


def ajuda(event, context):
    logger.info('entrou no arquivo de ajuda o/')

    message = json.loads(event['Records'][0]['Sns']['Message'])

    logger.info(message)

    characteres = message['characteres']
    chatId = message['chatId']

    logger.info(characteres)
    logger.info(chatId)

    if chatId:

        entrada = str(characteres)

        with open('commands.json', 'r') as arquivo:
            data = arquivo.read()

        Ajuda = json.loads(data)

        #  esse proximo bloco so sera utilizado qdo o texto vier em branco, caso contrario os if abaixo limpam ele
        MsgEnv = "Olá. Tudo bem? Seguinte, segue abaixo uma pequena lista do que eu sei fazer: \n"
        for comando in Ajuda:
            ajudaStr = Ajuda[comando]
            MsgEnv = MsgEnv + "/" + comando + \
                " - " + ajudaStr['curta'] + "\n"
        MsgEnv = MsgEnv + "\n \n Ah e se voce quiser pode pedir ajuda para um comando especifico, utilizando /ajuda comando, por exemplo '/ajuda contar '"

        if entrada.startswith('autor') or entrada.startswith(' autor'):
            findComando = entrada.replace('autor', '').replace(' ', '')
            for comando in Ajuda:
                ajudaStr = Ajuda[comando]
                if comando == findComando:
                    MsgEnv = "O autor é o " + ajudaStr['autor']
        else:
            findComando = entrada.replace(' ', '')
            for comando in Ajuda:
                ajudaStr = Ajuda[comando]
                if comando == findComando:
                    MsgEnv = ajudaStr['longa']

        MESSAGE = json.dumps(
            {'text': MsgEnv, 'messageType': 'text'})
        publishSnsTopic(chatId, MESSAGE)

        return OK_RESPONSE
    else:
        MsgEnv = 'Voce não informou os parametros necessários para a execução desse comando. Por favor, consulte /ajuda'
        MESSAGE = json.dumps(
            {'text': MsgEnv, 'messageType': 'text'})
        publishSnsTopic(chatId, MESSAGE)

        return OK_RESPONSE

    return ERROR_RESPONSE
