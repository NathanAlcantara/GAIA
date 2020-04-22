import json
from awsHelper import publishSnsTopic


def lambda_handler(event, ctx):
    sns_message = json.loads(event['Records'][0]['Sns']['Message'])
    chat_id = sns_message['chat_id']
    context = sns_message['context']
    # Caso não exista contexto, então se trata de uma nova inscrição
    status = context['status']
    swticher = convo_switcher()
    swticher.switch(status, context)
    if context['status'] == {}:
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


class convo_switcher(object):
    def switch(self, status, context):
        method_name = 'case_' + status
        method = getattr(self, method_name, lambda: 'Erro')
        return method(context)

    def case_start(self, context):
        text_message = "Muito bem, vamos fazer sua inscrição. /n" + ...
        "Me diga seu nome completo"
        context['Status'] = "name"
        self.dispatch(text_message, context)

    def case_name(self, context):
        # TODO receber a informação do nome e gravar no DynamoDB
        text_message = "Beleza, agora me envia seu CPF por favor"
        context['status'] = "cpf"
        self.dispatch(text_message, context)

    def case_cpf(self, context):
        # TODO receber e validar a informação de CPF e gravar no Dynamo DB
        text_message = "Agora vou precisar do seu endereço nesse formato: /n" + ...
        "Rua, número, complemento, bairro e CEP"
        context['status'] = "address"
        self.dispatch(text_message, context)

    def case_address(self, context):
        # TODO receber e validar a informação do endereço e gravar no Dynamo DB
        text_message = "Qual sua data de nascimento? =D /n" + ...
        "por favor use o formato dd/mm/aaaa"
        context['status'] = "birth_date"
        self.dispatch(text_message, context)

    def case_birth_date(self, context):
        # TODO receber e validar a informação da data de nascimento e gravar no Dynamo DB
        # TODO personalizar mensagem com o nome do usuário
        text_message = "Ótimo! Obrigado pelas informações, sua inscrição está feita!"
        self.dispatch(text_message, context)

    def case_finished(self, context):
        text_message = "Hey, sua inscrição já está feita! Por enquanto não é possível editar ela =("
        self.dispatch(text_message, context)

    def dispatch(self, text_message, context):
        # TODO confirmar se será possível obter o chat_id dessa forma (provavelmente não)
        chat_id = context['chat_id']
        publishSnsTopic(chat_id, text_message)
        # TODO atualizar contexto no Dynamo DB
        return True