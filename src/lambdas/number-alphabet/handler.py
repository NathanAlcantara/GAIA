import json
import sys
import logging
import unicodedata
from awsHelper import OK_RESPONSE, ERROR_RESPONSE, publishSnsTopic
from textHelper import removerEspeciais, alphabet_reverse

logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logging.basicConfig(level=logging.INFO)


def letras(event, context):
    logger.info('entrnou no conversor de numeros para letras o/')

    message = json.loads(event['Records'][0]['Sns']['Message'])

    logger.info(message)

    characters = message['characters']
    chatId = message['chatId']

    logger.info(characters)
    logger.info(chatId)

    if characters and chatId:

        Msg = str(characters)

        MsgEnv = removerEspeciais(Msg)
        Resposta = alphabet_reverse(MsgEnv)
        if Resposta == MsgEnv or Resposta == '' or Resposta == ' ':
            MsgEnv = "Ei, não consegui converter nada. Você tem certeza que está usando a função correta? Talvez voce queira usar a /numeros"
        else:
            MsgEnv = "Aqui está, veja que ignorei tudo o que não era válido: \n " + Resposta

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
