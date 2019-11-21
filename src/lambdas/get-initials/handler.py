import json
import sys
import logging
import unicodedata
from awsHelper import OK_RESPONSE, ERROR_RESPONSE, publishSnsTopic
from textHelper import removePontuacao

logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logging.basicConfig(level=logging.INFO)


def iniciais(event, context):
    logger.info('vamos pegar as iniciais')

    message = json.loads(event['Records'][0]['Sns']['Message'])

    logger.info(message)

    characters = message['characters']
    chatId = message['chatId']

    logger.info(characters)
    logger.info(chatId)

    if characters and chatId:

        Msg = str(characters)

        LisMsg = str(Msg).splitlines()  # cria um array com as linhas
        FinalSemPonto = InicialSemPonto = Final = Inicial = ''
        for Linha in LisMsg:
            if Linha != '':
                LinhaSemPonto = removePontuacao(Linha.replace(" ", ""))
                InicialSemPonto = InicialSemPonto + ' ' + LinhaSemPonto[0][0]
                FinalSemPonto = FinalSemPonto + ' ' + LinhaSemPonto[-1:]
                Linha = Linha.replace(" ", "")
                Inicial = Inicial + ' ' + Linha[0][0]
                Final = Final + ' ' + Linha[-1:]

        MsgEnv = "Aqui está minha análise:\n"
        MsgEnv = MsgEnv + "\nIniciais:  " + Inicial
        MsgEnv = MsgEnv + "\nFinais:  " + Final
        MsgEnv = MsgEnv + "\nIniciais sem pontuação:  " + InicialSemPonto
        MsgEnv = MsgEnv + "\nFinais sem pontuação:  " + FinalSemPonto

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
