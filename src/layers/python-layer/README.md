## Layer Python- Bibliotecas e uso

## Uso

Para utilizar as funcoes do layer basta importar das bibliotecas listadas abaixo as funçoes desejadas.
Como por exemplo

    from awsHelper import OK_RESPONSE

## Bibliotecas

awsHelper - Biblioteca com as funçoes de helper para a AWS, e respostas padroes, composta de:

    1. OK_RESPONSE - Resposta OK qdo codigo executado
    2. ERROR_RESPONSE - Resposta de Erro qdo codigo executado
    3. publishSnsTopic (chatId, payload, snsName="send-telegram-response")   - Publica num SNS, onde:
        chatId = Chat ID da conversa
        payload = Mensagem a ser enviada, conforme contrato do sns
        snsName = Nome do SNS a ser enviado, por padrao o send-telegram-response

textHelper - Biblioteca com as funcoes de helper para texto, composta de:

    1. alphabet_position(text) - diz a posicao no alfabeto de uma serie de caracteres
    2. remover_especiais(text) - remove caracteres especiais (acentuacao, cedilha, etc)
    3. alphabet_reverse(text) - diz as letras correspondentes aos numero de 1 a 26.
    4. removePontuacao(text) - remove a pontuacao de um texto dado.
