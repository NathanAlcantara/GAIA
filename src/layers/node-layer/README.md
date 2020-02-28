## Layer Node - Bibliotecas e uso

## Uso

Para utilizar as funções do layer basta importar das bibliotecas listadas abaixo as funções desejadas.
<br>
Como por exemplo:

    const { publishSnsTopic } = require("/opt/utils/awsHelpers");

## Bibliotecas

### **helper**

#### Biblioteca com as funções de helper gerais, composta por:

`generateSuccess(callback, payload, code)`:

- Gera uma mensagem de sucesso da requisição na lambda:
  - callback = Callback da lambda
  - payload = Mensagem de sucesso
  - code = Código da requisição

`generateError(callback, payload, code)`:

- Gera uma mensagem de erro da requisição na lambda:
  - callback = Callback da lambda
  - payload = Mensagem de erro
  - code = Código da requisição

### **awsHelper**

#### Biblioteca com as funções de helper para a AWS, composta por:

`extractMessageOfEventSns(event)`:

- Recebe o evento da lambda e extrai a mensagem do sns;

`publishSnsTopic(chatId, payload, snsName?)`:

- Publica em um SNS, onde:
  - chatId = Chat ID da conversa
  - payload = Mensagem a ser enviada, conforme contrato do sns
  - snsName = Nome do SNS a ser enviado, por padrão é o **send-telegram-response**

### **botHelper**

#### Biblioteca com as funções de helper para o bot, composta por:

`TELEGRAM_TOKEN`:

- Constante do token do telegram

`executeMethodBot(methodName, methodBody)`:

- Envia uma requisição para o telegram executar o método em questão, onde:
  - methodName = Nome do método;
  - methodBody = Objeto a ser enviado no corpo da requisição;

`isCommandExistPrototype(command)`:

- Função auxiliar de uma string para validar se a string é o comando, onde:
  - command = Comando a ser validado

`getValueCommandPrototype(command)`:

- Função auxiliar de uma string para pegar o valor contido depois do comando, onde:
  - command = Comando a ser verificado e removido para pegar seu valor
