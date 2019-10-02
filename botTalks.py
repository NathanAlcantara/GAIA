import json
import logging
import unicodedata
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./vendored"))

import requests

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

## vamos configurar o bot
def configure_telegram():
    """
    Configures the bot with a Telegram Token.
    Returns a bot instance.
    """
    ## vamos adaptar a linha abaixo para pegar uma variavel da aws?
    ## TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')  
    TELEGRAM_TOKEN = '971659403:AAG3mMqJaTrljyM89KObckBYu8GDyVdqkOA'
    if not TELEGRAM_TOKEN:
        logger.error('The TELEGRAM_TOKEN must be set')
        raise NotImplementedError

    return Bot(TELEGRAM_TOKEN)

logger = logging.getLogger()
logger.setLevel(logging.INFO)


## json { mensagem : x , id =  yyyy , formato:  ssss}
## mensagem como sendo texto ou url do arquivo/foto, a id é a chat_id e o formato pode ser
# texto = mensagem de texto
# imagem = imagem
# documento = documento
# audio = msg de audio
# markdown = texto com formatacao
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

    
    
