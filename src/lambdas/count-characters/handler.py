import json
import sys
import logging
import unicodedata
from io import StringIO
from awsHelper import OK_RESPONSE, ERROR_RESPONSE, publishSnsTopic, GetPublicLink
from textHelper import removePontuacao

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

        # verificar se há mais de uma linha
        LisMsg = str(Msg).splitlines()
        if len(ListMsg) > 1:
            TextoLongo(ListMsg, chatId)
            return OK_RESPONSE

        Msg = Msg.replace('\r', '').replace(
            '\n', '')  # removemos a quebra de linha por nada :(
        lenMsg = len(Msg)
        lenMsgSemEspaco = len(Msg.replace(" ", ""))

        MsgSemPonto = Msg.replace(" ", "")  # msg sem espaco
        MsgSemPonto = removePontuacao(MsgSemPonto)
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


def TextoLongo(LisMsg, chatId):
    ctLinha = LenMsg = LenMsgSemEspaco = LenMsgSemPonto = LenMsgEspacada = 0
    MsgUpper = MsgLower = 0
    Resposta = 'Linha;Total;Sem Espaços;Sem Pontuação;Sem Pontuação e com Espaços;Maiúsculas;Minúsculas'
    for Linha in LisMsg:
        ctLinha = ctLinha + 1
        Linha = Linha.replace('\r', '').replace(
            '\n', '')  # removi as quebras, se houver ?
        LenLinha = len(Linha)  # tamanho da linha
        LenLinhaSemEspaco = len(Linha.replace(" ", ""))
        LinhaSemPonto = removePontuacao(Linha)
        LenLinhaSemPonto = len(LinhaSemPonto)
        LenLinhaEspacada = (LenLinha - LenLinhaSemPonto) + LenLinhaSemPonto
        LinhaUpper = sum(map(str.isupper, Linha))
        LinhaLower = sum(map(str.islower, Linha))
        Resposta = Resposta + "\n" + "{};{};{};{};{};{};{}".format(
            ctLinha, LenLinha, LenLinhaSemEspaco, LenLinhaSemPonto, LenLinhaEspacada, LinhaUpper, LinhaLower)

        # aqui somamos de todo o texto
        LenMsg = LenMsg + LenLinha
        LenMsgSemEspaco = LenMsgSemEspaco + LenLinhaSemEspaco
        LenMsgSemPonto = LenMsgSemPonto + LenLinhaSemPonto
        LenMsgEspacada = LenMsgEspacada + LenLinhaEspacada
        MsgUpper = MsgUpper + LinhaUpper
        MsgLower = MsgLower + LinhaLower

    Resposta = Resposta + "\n" + "{};{};{};{};{};{};{}".format(
        "Total", LenMsg, LenMsgSemEspaco, LenMsgSemPonto, LenMsgEspacada, MsgUpper, MsgLower)

    logger.info(Resposta)

    RespostaIO = StringIO(Resposta)

    LinkPublic = GetPublicLink(RespostaIO, 'csv', 6000, 'gaia-publico')

    MESSAGE = json.dumps(
        {'text': LinkPublic, 'messageType': 'document'})
    publishSnsTopic(chatId, MESSAGE)
