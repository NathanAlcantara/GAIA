## Layer Python - Bibliotecas e uso

## Uso

Para utilizar as funções do layer basta importar das bibliotecas listadas abaixo as funções desejadas.
Como por exemplo

    from awsHelper import OK_RESPONSE

## Bibliotecas

awsHelper - Biblioteca com as funções de helper para a AWS, e respostas padrões, composta de:

    1. OK_RESPONSE - Resposta OK qdo código executado
    2. ERROR_RESPONSE - Resposta de Erro qdo código executado
    3. publishSnsTopic (chatId, payload, snsName="send-telegram-response")   - Publica num SNS, onde:
        chatId = Chat ID da conversa
        payload = Mensagem a ser enviada, conforme contrato do sns
        snsName = Nome do SNS a ser enviado, por padrão o send-telegram-response

textHelper - Biblioteca com as funções de helper para texto, composta de:

    1. alphabet_position(text) - diz a posição no alfabeto de uma serie de caracteres
    2. remover_especiais(text) - remove caracteres especiais (acentuação, cedilha, etc)
    3. alphabet_reverse(text) - diz as letras correspondentes aos numero de 1 a 26.
    4. removePontuação(text) - remove a pontuação de um texto dado.
