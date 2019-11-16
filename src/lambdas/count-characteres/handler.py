import json
import sys
import logging
import unicodedata
from awsHelper import OK_RESPONSE, ERROR_RESPONSE, publishSnsTopic

logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logging.basicConfig(level=logging.INFO)


def count(event, context):
    logger.info('entrnou no contado o/')

    message = json.loads(event['Records'][0]['Sns']['Message'])

    logger.info(message)

    characteres = message['characteres']
    chatId = message['chatId']

    logger.info(characteres)
    logger.info(chatId)

    if characteres and chatId:

        Msg = str(characteres)
        lenMsg = len(Msg)
        lenMsgSemEspaco = len(Msg.replace(" ", ""))

        MsgSemPonto = Msg.replace(" ", "")  # msg sem espaco
        tbl = dict.fromkeys(i for i in range(sys.maxunicode)
                            if unicodedata.category(chr(i)).startswith('P'))  # tabela para pontuacao unicode
        # msg sem ponto e espaco, removendo pontuacao
        MsgSemPonto = MsgSemPonto.translate(tbl)
        # subtrai seis devido a palavra 'contar'
        lenMsgSemPonto = len(MsgSemPonto) - 6
        lenMsgSemPontoEspacada = (lenMsg - lenMsgSemEspaco) + lenMsgSemPonto
        qtdUpper = sum(map(str.isupper, Msg))
        # subtrai seis devido a palavra contar
        qtdLower = sum(map(str.islower, Msg))-6
        MsgEnv = "Total: " + str(lenMsg)
        MsgEnv = MsgEnv + "\nSem espaços: " + str(lenMsgSemEspaco)
        MsgEnv = MsgEnv + "\nSem pontuação: " + str(lenMsgSemPonto)
        MsgEnv = MsgEnv + "\nSem pontuação e com espaço: " + \
            str(lenMsgSemPontoEspacada)
        MsgEnv = MsgEnv + "\nMinusculas: " + str(qtdLower)
        MsgEnv = MsgEnv + "\nMaiusculas: " + str(qtdUpper)
        if qtdUpper > 0:
            strUpper = ''.join([x for x in Msg if x.isupper()])
            MsgEnv = MsgEnv + "\nAh, separei as maiusculas para voce: " + strUpper
        if qtdUpper > qtdLower:
            strLower = ''.join([x for x in Msg if x.islower()])
            MsgEnv = MsgEnv + \
                "\nNesse caso pareceu ser interessante separar as minusculas, aqui: " + strLower

        MESSAGE = json.dumps({'chatId': chatId, 'message': MsgEnv})
        publishSnsTopic(chatId, MESSAGE)

        return OK_RESPONSE

    return ERROR_RESPONSE
