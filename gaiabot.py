import json
import logging
import unicodedata
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./vendored"))

import requests

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot, Update

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
def start(update, context, id, bot):
    """Envia uma mensagem qdo o comando star ocorre"""
    logger.info('Entramos no Start')
    MsgEnv = """Bem vindo, eu sou Gaia, o Cacique dos bots!
Duvidas? Por favor, utilize o comando /ajuda  nele voce encontra um guia rápido e tudo o que voce precisa saber sobre mim ;)"""
    bot.sendMessage(chat_id=id, text=MsgEnv) ## usamos a funca de bot sendmessage 
    logger.info('Bot evviado')

#Comando Ajuda em ação ;)
def help(update, context, id, bot):
    logger.info('Entramos na ajuda')
    MsgEnv = """Nothing to do here, move along.....
Um dia nos vamos fazer um menu de ajuda dahora, mas por enquanto, só sei contar, use /contar e veja por si mesmo'"""
    bot.sendMessage(chat_id=id, text= MsgEnv)

#esse é o echo, por enquanto, ele repete ou faz um calcul de fomrula... bem inutil
def echo(update, context):
    """Echo the user message."""
    mensagem2 = update.message.text
    try:
        update.message.reply_text(eval(mensagem2))  
    except Exception as e:
      update.message.reply_text(update.message.text) 
    #update.message.reply_text(update.message.text)

## funcao para contar caracteres num texto, usamos como padrao o comando em minusculo, preciso avaliar isso melhor
def contarCaracteres(update, context, id, bot):
    Msg = str(update.message.text)
    lenComando = len ("/contar ")
    lenMsg = len(Msg) - lenComando
    lenMsgSemEspaco = len(Msg.replace(" ","")) - 7  # subtrai sete devido a '/contar'

    MsgSemPonto = Msg.replace(" ","") ## msg sem espaco
    tbl = dict.fromkeys(i for i in range(sys.maxunicode)
                        if unicodedata.category(chr(i)).startswith('P')) ## tabela para pontuacao unicode
    MsgSemPonto =  MsgSemPonto.translate(tbl) ## msg sem ponto e espaco, removendo pontuacao
    lenMsgSemPonto = len(MsgSemPonto) - 6 # subtrai seis devido a palavra 'contar'
    lenMsgSemPontoEspacada = (lenMsg - lenMsgSemEspaco) + lenMsgSemPonto
    qtdUpper = sum(map(str.isupper, Msg))
    qtdLower = sum(map(str.islower, Msg))-6 # subtrai seis devido a palavra contar
    MsgEnv = "Total: " + str(lenMsg)
    MsgEnv = MsgEnv + "\nSem espaços: " + str(lenMsgSemEspaco ) 
    MsgEnv = MsgEnv + "\nSem pontuação: "+ str(lenMsgSemPonto) 
    MsgEnv = MsgEnv + "\nSem pontuação e com espaço: "+ str(lenMsgSemPontoEspacada)
    MsgEnv = MsgEnv + "\nMinusculas: " + str(qtdLower)
    MsgEnv = MsgEnv + "\nMaiusculas: " + str(qtdUpper)
    if qtdUpper > 0  :
        strUpper = ''.join([x for x in Msg if x.isupper()])
        MsgEnv = MsgEnv + "\nAh, separei as maiusculas para voce: " + strUpper
    if qtdUpper > qtdLower :
        MsgPura = Msg.replace("/contar", "")
        strLower = ''.join([x for x in MsgPura if x.islower()])
        MsgEnv = MsgEnv + "\nNesse caso pareceu ser interessante separar as minusculas, aqui: " + strLower
    bot.sendMessage(chat_id=id, text=MsgEnv)


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
            start(event.update, context, chat_id, bot)
        if text and text.startswith ('/ajuda'):
            logger.info('Entrou na ajuda')
            help(event.update, context, chat_id, bot)
        if text and text.startswith('/contar'):
            logger.info('entrou no contar')
            contarCaracteres(update,context,chat_id,bot)


        # bot.sendMessage(chat_id=chat_id, text=text)
        logger.info('Message sent')

        return OK_RESPONSE

    return ERROR_RESPONSE

