import json


def lambda_handler(event, ctx):
    message = json.loads(event['Records'][0]['Sns']['Message'])
    chat_id = message['chat_id']
    context = message['context']
    # Caso não exista contexto, então se trata de uma nova inscrição
    if context == {}:
        return True
    # Caso contrário, segue uma lógica de inscrição
    else:
        return True

        # Caso especial para quando o usuário enviar a imagem. Necessário fazer o download da imagem

        # Download da imagem se dá através de uma lambda separada, que é instruída a chamar essa de volta quando
        # concluir

    # Gravar dados no DynamoDB

    # Envio de mensagem para o usuário

    return True
