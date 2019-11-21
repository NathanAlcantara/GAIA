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
    logger.info('entrou no contado o/')

    message = json.loads(event['Records'][0]['Sns']['Message'])

    logger.info(message)

    characters = message['characters']
    chatId = message['chatId']

    logger.info(characters)
    logger.info(chatId)

    if characters and chatId:

        Msg = str(characters)
        lenMsgBruta = len(Msg)

        Msg = Msg.replace('\r', '').replace(
            '\n', '')  # removemos a quebra de linha por nada :(
        lenMsg = len(Msg)
        lenMsgSemEspaco = len(Msg.replace(" ", ""))

        MsgSemPonto = Msg.replace(" ", "")  # msg sem espaco
        tbl = dict.fromkeys(i for i in range(sys.maxunicode)
                            if unicodedata.category(chr(i)).startswith('P'))  # tabela para pontuacao unicode
        # msg sem ponto e espaco, removendo pontuacao
        MsgSemPonto = MsgSemPonto.translate(tbl)
        # subtrai seis devido a palavra 'contar'
        lenMsgSemPonto = len(MsgSemPonto)
        lenMsgSemPontoEspacada = (lenMsg - lenMsgSemEspaco) + lenMsgSemPonto
        qtdUpper = sum(map(str.isupper, Msg))
        # subtrai seis devido a palavra contar
        qtdLower = sum(map(str.islower, Msg))
        MsgEnv = "Total: " + str(lenMsg)
        MsgEnv = MsgEnv + "\nSem espaços: " + str(lenMsgSemEspaco)
        MsgEnv = MsgEnv + "\nSem pontuação: " + str(lenMsgSemPonto)
        MsgEnv = MsgEnv + "\nSem pontuação e com espaço: " + \
            str(lenMsgSemPontoEspacada)
        MsgEnv = MsgEnv + "\nMinúsculas: " + str(qtdLower)
        MsgEnv = MsgEnv + "\nMaiúsculas: " + str(qtdUpper)
        if lenMsgBruta > lenMsg:
            MsgEnv = MsgEnv + \
                "\nEsteja ciente que transformei suas {} linhas em apenas uma. Se você quiser considerá-las, lembre-se de somar isso.".format(
                    lenMsgBruta - lenMsg + 1)
        if qtdUpper > 0:
            strUpper = ''.join([x for x in Msg if x.isupper()])
            MsgEnv = MsgEnv + "\nAh, separei as maiúsculas para você: " + strUpper
        if qtdUpper > qtdLower:
            MsgPura = Msg.replace("/contar", "")
            strLower = ''.join([x for x in MsgPura if x.islower()])
            MsgEnv = MsgEnv + \
                "\nNesse caso pareceu ser interessante separar as minúsculas, aqui: " + strLower

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
