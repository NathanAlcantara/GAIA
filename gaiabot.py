import json
import logging
import unicodedata
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./vendored"))

import requests

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot, Update, ParseMode

# Logging is cool!
logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logging.basicConfig(level=logging.INFO)

OK_RESPONSE = {
    'statusCode': 200,
    'headers': {'Content-Type': 'application/json'},
    'body': json.dumps('ok')
}
ERROR_RESPONSE = {
    'statusCode': 400,
    'body': json.dumps('Oops, something went wrong!')
}

## vamos configurar o telegram
def configure_telegram():
    """
    Configures the bot with a Telegram Token.
    Returns a bot instance.
    """

    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
    if not TELEGRAM_TOKEN:
        logger.error('The TELEGRAM_TOKEN must be set')
        raise NotImplementedError

    return Bot(TELEGRAM_TOKEN)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

######## Aquiva vamos definir nossos comandos, cada um faz algo e tals
def start(lambda_str):
    """Envia uma mensagem qdo o comando star ocorre"""
    logger.info('Entramos no Start')
    entrada = json.loads(lambda_str) ## pegamos a entrada
    id = int(entrada.get("id")) # a id
    MsgEnv = """Bem vindo, eu sou Gaia, o Cacique dos bots!
Duvidas? Por favor, utilize o comando /ajuda  nele voce encontra um guia rápido e tudo o que voce precisa saber sobre mim ;)"""
    x = {
        "mensagem" : MsgEnv ,
        "id" : id ,
        "formato" : "texto"
    }
    jhon = json.dumps(x)
    botTalk(jhon)

#Comando Ajuda em ação ;)
def help(lambda_str):
    logger.info('Entramos na ajuda')

    entrada = json.loads(lambda_str) ## pegamos a entrada
    id = int(entrada.get("id")) # a id

    MsgEnv = """Nothing to do here, move along.....
Um dia nos vamos fazer um menu de ajuda dahora, mas por enquanto, só sei contar, use /contar e veja por si mesmo'"""

    x = {
        "mensagem" : MsgEnv ,
        "id" : id ,
        "formato" : "texto"
    }
    jhon = json.dumps(x)
    botTalk(jhon)

## funcao para contar caracteres num texto, usamos como padrao o comando em minusculo, preciso avaliar isso melhor
def contarCaracteres(lambda_str):

    entrada = json.loads(lambda_str) ## pegamos a entrada
    Msg = entrada.get("mensagem") # a msg

    lenMsgBruta = len(Msg) # tamanho da msg com  breaklines
    Msg = Msg.replace('\r', '').replace('\n', '') ## removemos a quebra de linha por nada :(

    id = int(entrada.get("id")) # a id

    lenComando = len ("/contar ")
    lenMsg = len(Msg) - lenComando
    lenMsgBruta = lenMsgBruta - lenComando
    lenMsgSemEspaco = len(Msg.replace(" ","")) - 7  # subtrai sete devido a '/contar'

    MsgSemPonto = Msg.replace(" ","") ## msg sem espaco
    tbl = dict.fromkeys(i for i in range(sys.maxunicode)
                        if unicodedata.category(chr(i)).startswith('P')) ## tabela para pontuacao unicode
    MsgSemPonto =  MsgSemPonto.translate(tbl) ## msg sem ponto e espaco, removendo pontuacao
    lenMsgSemPonto = len(MsgSemPonto) - 6 # subtrai seis devido a palavra 'contar'
    lenMsgSemPontoEspacada = (lenMsg - lenMsgSemEspaco) + lenMsgSemPonto
    qtdUpper = sum(map(str.isupper, Msg))
    logger.info(qtdUpper)
    qtdLower = sum(map(str.islower, Msg))-6 # subtrai seis devido a palavra contar
    MsgEnv = "Você não informou nenhum texto, por favor, escreva algo após o /contar "
    if len(Msg) > lenComando :
        MsgEnv = "Total: " + str(lenMsg)
        MsgEnv = MsgEnv + "\nSem espaços: " + str(lenMsgSemEspaco ) 
        MsgEnv = MsgEnv + "\nSem pontuação: "+ str(lenMsgSemPonto) 
        MsgEnv = MsgEnv + "\nSem pontuação e com espaço: "+ str(lenMsgSemPontoEspacada)
        MsgEnv = MsgEnv + "\nMinusculas: " + str(qtdLower)
        MsgEnv = MsgEnv + "\nMaiusculas: " + str(qtdUpper)
        if lenMsgBruta > lenMsg:
            MsgEnv = MsgEnv +"\nEsteja ciente que transformei suas {} linhas em apenas uma. Se voce quiser considera-las, lembre-se de somar isso.".format(lenMsgBruta - lenMsg + 1)
        if qtdUpper > 0  :
            strUpper = ''.join([x for x in Msg if x.isupper()])
            MsgEnv = MsgEnv + "\nAh, separei as maiusculas para voce: " + strUpper
        if qtdUpper > qtdLower :
            MsgPura = Msg.replace("/contar", "")
            strLower = ''.join([x for x in MsgPura if x.islower()])
            MsgEnv = MsgEnv + "\nNesse caso pareceu ser interessante separar as minusculas, aqui: " + strLower
    x = {
        "mensagem" : MsgEnv ,
        "id" : id ,
        "formato" : "texto"
    }
    jhon = json.dumps(x)
    logger.info(MsgEnv)
    botTalk(jhon)

def TextoContar(lambda_str):

    entrada = json.loads(lambda_str) ## pegamos a entrada

    Msg = entrada.get("mensagem") # a msg
    id = int(entrada.get("id")) # a id

    tbl = dict.fromkeys(i for i in range(sys.maxunicode)
                        if unicodedata.category(chr(i)).startswith('P')) ## tabela para pontuacao unicode

    if Msg == '/texto ' or Msg == '/texto':
        MsgEnv = "Você não informou nenhum texto, por favor, escreva algo após o /texto "
    else:
        Msg = Msg.replace('/texto ', '')

        LisMsg = str(Msg).splitlines() ## cria um array com as linhas
        # MsgEnv = "<pre>\n "+ " <b>|Linha | Total | S Esp. | S Pont. | Pont + Esp | Maiusc. | Miusc.| </b>"
        # MsgEnv = MsgEnv + "\n" + "|-----|-----|-----|-----|-----|-----|-----|"
        MsgEnv = "Linha;Total;Sem Espaços;Sem Pontuação;Sem Pontuação e Com Espaços;Maiuscula;Miuscula"
        ctLinha = LenMsg = LenMsgSemEspaco = LenMsgSemPonto = LenMsgEspacada = 0
        MsgUpper = MsgLower = 0

        for Linha in LisMsg :
            ctLinha = ctLinha + 1
            Linha = Linha.replace('\r', '').replace('\n', '') ## removemos a quebra de linha por nada :(
            LenLinha = len(Linha) # tamanho da linha
            LenLinhaSemEspaco = len(Linha.replace(" ","")) 
            LinhaSemPonto = Linha.replace(" ", "").translate(tbl) ## msg sem ponto e espaco, removendo pontuacao
            LenLinhaSemPonto = len(LinhaSemPonto)
            LenLinhaEspacada = (LenLinha - LenLinhaSemEspaco) + LenLinhaSemPonto
            LinhaUpper = sum(map(str.isupper, Linha))
            LinhaLower = sum(map(str.islower, Linha))
            MsgEnv = MsgEnv + "\n" + "{};{};{};{};{};{};{}".format(ctLinha,LenLinha,LenLinhaSemEspaco,LenLinhaSemPonto,LenLinhaEspacada,LinhaUpper,LinhaLower)

            # aqui somamos de todo o texto
            LenMsg = LenMsg + LenLinha
            LenMsgSemEspaco = LenMsgSemEspaco + LenLinhaSemEspaco
            LenMsgSemPonto = LenMsgSemPonto + LenLinhaSemPonto
            LenMsgEspacada = LenMsgEspacada + LenLinhaEspacada
            MsgUpper = MsgUpper + LinhaUpper
            MsgLower = MsgLower + LinhaLower

        MsgEnv = MsgEnv + "\n" + "{};{};{};{};{};{};{}".format("Total",LenMsg,LenMsgSemEspaco,LenMsgSemPonto,LenMsgEspacada,MsgUpper,MsgLower)
        MsgEnv = MsgEnv + "\n</pre>"
        if MsgUpper > 0  :
            strUpper = ''.join([x for x in Msg if x.isupper()])
            MsgEnv = MsgEnv + "\n\nAh, separei as maiusculas para voce: " + strUpper
        if MsgUpper * 0.4 > MsgLower :
            strLower = ''.join([x for x in Msg if x.islower()])
            MsgEnv = MsgEnv + "\nNesse caso pareceu ser interessante separar as minusculas, aqui: " + strLower
    x = {
        "mensagem" : MsgEnv ,
        "id" : id ,
        "formato" : "html"
    }
    jhon = json.dumps(x)
    botTalk(jhon)

def botTalk(LambdaTalks):
    
    entrada = json.loads(LambdaTalks) ## pegamos a entrada

    mensagem = entrada.get("mensagem") # a msg
    id = int(entrada.get("id")) # a id
    formato = entrada.get("formato") # o formato   
    bot = configure_telegram() # criamos uma instancia de bot ;)

    if formato == 'texto' :
        logger.info ('enviado um texto')
        bot.sendMessage(chat_id=id, text=mensagem)
    if formato == 'imagem' :
        logger.info ('enviado uma imagem')
        bot.sendPhoto(chat_id=id, photo=mensagem)
    if formato == 'documento':
        logger.info ('enviado um documento')
        bot.sendDocument(chat_id=id, document=mensagem)  
    if formato == 'html':
        logger.info ('enviado um texto markdown')
        bot.sendMessage(chat_id=id, text = mensagem, parse_mod=ParseMode.HTML)
    if formato == 'audio':
        logger.info ('enviado um audio')
        bot.sendAudio(chat_id=id, audio = mensagem)
    

## nosso main, aqui nosso robo inicia e fica rodando em loop
def hello(event, context):
    """
   Aqui é onde entramos através do webhook
    """

    bot = configure_telegram() ## configuramos o bot
    logger.info('Event: {}'.format(event)) ## vamos logar a confirugracao

    if event.get('httpMethod') == 'POST' and event.get('body'): 
        logger.info('Message received')
        update = Update.de_json(json.loads(event.get('body')), bot)
        chat_id = update.message.chat.id
        text = update.message.text

        if text and text.startswith ('/start'):
            logger.info('Entrou no iF')
            x = {
                "id" : chat_id
            }
            jhon = json.dumps(x)
            start(jhon)
        if text and text.startswith ('/ajuda'):
            logger.info('Entrou na ajuda')
            x = {
                "id" : chat_id
            }
            jhon = json.dumps(x)
            help(jhon)
        if text and text.startswith('/contar'):
            logger.info('entrou no contar')
            x = {
                "mensagem" : text ,
                "id" : chat_id
            }
            jhon = json.dumps(x)
            contarCaracteres(jhon)
        if text and text.startswith('/texto'):
            logger.info('entrou no contar')
            x = {
                "mensagem" : text ,
                "id" : chat_id
            }
            jhon = json.dumps(x)
            TextoContar(jhon)
        if text and text.startswith('/imagem') :
            x = {
                "mesagem" : "https://lovehaswon.org/wp-content/uploads/2019/07/mother_nature_by_nocluse-db5z2sy.jpg",
                "id" : chat_id,
                "formato" : "imagem"
            }
            jhon = json.dumps(x)  
            botTalk(jhon)
        if text and text.startswith('/documento'):
            jhon = '''{ "mensagem": "https://www.pucpcaldas.br/graduacao/administracao/revista/artigos/v4n2/v4n2a5.pdf", 
"formato" : "documento" , 
"id": " ''' + str(chat_id) + '''" } '''  
            botTalk(jhon)
        if text and text.startswith('/tabela'):
            texto = '''<pre>First Header  | Second Header
  ------------- | -------------
  *Content Cell*  | <b>Content Cell </b>
  <code>Content Cell </code>  | Content Cell </pre>'''
            x = { 
                "mensagem" : texto ,
                "id" : chat_id,
                "formato" : "html"
            }
            jhon = json.dumps(x)
            botTalk(jhon)

        # bot.sendMessage(chat_id=chat_id, text=text)
        logger.info('Message sent')

        return OK_RESPONSE

    return ERROR_RESPONSE

