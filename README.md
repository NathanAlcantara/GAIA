# GAIA

## Iniciativa Gaia

### Telegram Bot

#### Pre-requisitos:

1. [Node](https://nodejs.org/en/)
2. [Python](https://www.python.org)
3. Serverless, `npm i -g serverless`
4. Credenciais da AWS (AccountId e SecretKey)
5. Token do Bot criado com o [BotFather](https://telegram.me/BotFather)
6. Uma conta no [serverless](https://dashboard.serverless.com), para acessar os dashboards

#### Recomendados:

- [Prettier - Code formatter for VSCode](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)
- [Python for VSCode](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [GitLens for VSCode](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens)

#### For Dev:

1. Primeiramente, na sua conta serverless você deve criar uma aplicação com o seu nome, ex: `david`;

- Após isso, podemos ver que no projeto temos uma pasta de scripts, onde existe um bash script chamado `deployDev.sh` onde será usado para testar nossos ambientes de desenvolvimento.

2. Para isso, você precisa alterar as 3 variável hoje lá existentes:

   - `name`, naturalmente atribuindo o nome da aplicação criada no primeiro passo;
   - `serverlessUser`, o usuario que foi usado na criação da conta serverless;
   - `telegramToken`, o token do bot criado;

      #### ATENÇÃO!! NÃO COMMITAR O SCRIPT ALTERADO!!

3. Então é só rodar no terminal `npm install` para instalar as dependencias.

4. Por fim, basta rodar `npm run deployDev` que o bash será executado criando a estrutura serverless totalmente do seu ambiente na aws.

- Sempre que for fazendo qualquer mudança basta executar esse comando novamente e a mágia continuará acontecendo!!

PS: Temos uma pasta chamada `docs` onde lá fica definido os contratos de todas as nossas lambdas, caso venha a criar uma nova por favor adicionar o arquivo que representa o contrato dela respeitando o padrão:

```
{
  "SNS": "string", //SNS que a lambda fica inscrita
  "Input": "Object | {}", //Objeto de entrada essencial para execução da lambda
  "Output": "Description" //Breve descrição da saída da lambda (ex: publica em um sns, manda uma string direto para o telegram, salva um arquivo no s3, etc...)
}
```

## Escopo:

- Extrair texto de imagens, áudio e PDF
- Pesquisar imagens que estão no arquivo
- Listar e contar maiúsculas, pontos e vírgulas
- Comparar textos, destacar partes removidas e inseridas
- Identificar palavras e verbos suspeitos
- Pesquisar ruas por código e nome (e demais infos do guia de ruas)
- Pesquisar objetos no acervo
- Check-List (por exemplo, se sao 8 numeros, então pode ser um CEP...)
- Indentificar metadados (ex os nomes dos autores naqueles aquivos de áudio ou então as propriedades de um arquivo PDF)

## Leituras sugeridas:

https://python-telegram-bot.org/ <br>
https://medium.com/tht-things-hackers-team/10-passos-para-se-criar-um-bot-no-telegram-3c1848e404c4/ <br>
https://www.sohamkamani.com/blog/2016/09/21/making-a-telegram-bot/ <br>
https://www.codementor.io/garethdwyer/building-a-chatbot-using-telegram-and-python-part-2-sqlite-databse-backend-m7o96jger/
