# GAIA

## Iniciativa Gaia

### Telegram Bot

#### Sobre a aplicação:

Cada serviço criado é totalmente agnóstico, cada um tem seu meio único e isolado de realizar deploy, o comando acima é apenas para inicializar o ambiente, a partir dai, sempre que for fazer qualquer mudança atente-se de executar apenas o deploy daquele serviço, casos a parte como layers que são dependências de todas as lambdas devem realizar o deploy de cada lambda dependente dela, ao criar um novo serviço lembre-se disso e de incluir ele no deploy principal ou no deploy de uma layer.

PS: Para depurar utilizando o serverless dashboard, basta você adicionar no serviço que deseja depurar as seguintes informações:

- org: é o seu username do serverless;
- app: é a aplicação que pedimos para criar no primeiro passo;

Aqui vai um [link](https://serverless.com/framework/docs/dashboard#enabling-the-dashboard-on-existing-serverless-framework-services) para ajudar a realizar a conexão;

PSS: Cada serviço é constituído de no minimo 2 arquivos, o `serverless.yml` que é onde é declarado o serviço e o `deploy.sh` que é o script de deploy do mesmo onde é recebido o nome do environment que irá ser deployado (por padrão usamos `dev`), para lambdas inclui-se mais um arquivo obrigatório que seria o arquivo contento a função que será executada (`handler.py` ou `handler.js`).

PSSS: O serviço de API Gateway é único para todos os tenants, inclusive com a produção, o que diferencia é o endpoint de cada um onde tem a informação do tenant no mesmo, e por isso ele não precisa ser deployado sempre, apenas quando houver alguma alteração/adição nele.

PSSSS: Temos uma pasta chamada `docs` onde lá fica definido os contratos de todas as nossas lambdas, caso venha a criar uma nova por favor adicionar o arquivo que representa o contrato dela respeitando o padrão:

```
{
  "SNS": "string", //SNS que a lambda fica inscrita
  "Input": "Object | {}", //Objeto de entrada essencial para execução da lambda
  "Output": "Description" //Breve descrição da saída da lambda (ex: publica em um sns, manda uma string direto para o telegram, salva um arquivo no s3, etc...)
}
```

#### Pre-requisitos:

1. [Node](https://nodejs.org/en/)
2. [Python](https://www.python.org)
3. Serverless, `npm i -g serverless`
4. Credenciais da [AWS](https://aws.amazon.com/pt/) (AccountId e SecretKey)
5. Token do Bot criado com o [BotFather](https://telegram.me/BotFather)

BONUS

1. Uma conta no [serverless](https://dashboard.serverless.com), caso deseje acessar os dashboards

#### Recomendados:

- [Prettier - Code formatter for VSCode](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)
- [Python for VSCode](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [GitLens for VSCode](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens)

#### For Dev:

(Leia tudo antes de executar, por favor, obrigado x3)

1. Primeiramente você precisa [configurar](https://serverless.com/framework/docs/providers/aws/cli-reference/config-credentials) a sua conta AWS no serverless.

   - Caso deseje usar o serverless dashboard para depuração você precisa adicionar parâmetros nos arquivos `serverless.yml` que deseja depurar, segue [exemplo](https://serverless.com/framework/docs/dashboard/#enabling-the-dashboard-on-existing-serverless-framework-services)

2. Para usar suas variáveis de ambiente, você precisa criar um arquivo chamado `environment.json` na raiz do projeto que vai conter as variáveis de ambiente:

   - `TENANT`, o nome do seu tenant, normalmente seu primeiro nome;
   - `AWS_ACCOUNT_ID`, o id da sua conta aws;
   - `TELEGRAM_TOKEN`, o token do bot criado;

   O arquivo deve seguir essa lógica (substituindo os placeholders por seus respectivos valores):

   ```
   {
     "TENANT": "{tenant}",
     "AWS_ACCOUNT_ID": "{accountId}",
     "TELEGRAM_TOKEN": "{token}",
     "END_FILE": "END_FILE"
   }
   ```

   (a última linha deve conter o `END_FILE` por complicações com virgulas no final da linha que em um futuro não tão distante será corrigido. xD)

   <strong>ATENÇÃO!! NÃO COMMITAR O ARQUIVO `ENVIRONMENT.JSON`!!</strong>

3. Sendo a primeira vez que o ambiente está sendo montado, deve-se criar o seu path com o nome do seu tenant no API Gateway e exporta-lo (não esqueça de commitar direto na branch principal logo ao criar para todos terem acesso), basta seguir o padrão que hoje já existe, por exemplo:

   Para criar o path (substitua `tenant` pelo nome do seu tenant):

   ```
   GAIApiPathTenant:
   Type: AWS::ApiGateway::Resource
   Properties:
     RestApiId: { Ref: "GAIApi" }
     ParentId: { Ref: "GAIApiPathTelegram" }
     PathPart: tenant
   ```

   Para exportar ele:

   ```
   apiGatewayRestApiPathTenant:
     Value:
       Ref: GAIApiPathTenant
     Export:
       Name: GAIApiGateway-tenantPath
   ```

4. Por fim, basta rodar `npm run deployDev` que o bash será executado criando a estrutura serverless totalmente do seu ambiente na aws.

5. Agora, para configurar o seu bot com a aplicação basta fazer uma chamada get (seja por Postman, Curl ou até mesmo pelo navegador) para a url `https://api.tribodosanjos87.com.br/gaia/dev/telegram/tenant` (lembrando de mudar `tenant` pelo nome do seu tenant) e voilá, seu bot está pronto para responder aos comandos!

6. Tente `/start` e veja a mágica acontecendo! xD

## Escopo:

- Extrair texto de imagens, áudio e PDF
- Pesquisar imagens que estão no arquivo
- Listar e contar maiúsculas, pontos e vírgulas
- Comparar textos, destacar partes removidas e inseridas
- Identificar palavras e verbos suspeitos
- Pesquisar ruas por código e nome (e demais infos do guia de ruas)
- Pesquisar objetos no acervo
- Check-List (por exemplo, se sao 8 números, então pode ser um CEP...)
- Identificar metadados (ex os nomes dos autores naqueles aquivos de áudio ou então as propriedades de um arquivo PDF)

## Leituras sugeridas:

[AWS](https://docs.aws.amazon.com) |
[Serverless](https://serverless.com/framework/docs/providers/aws/) |
[Bash script](https://www.devmedia.com.br/introducao-ao-shell-script-no-linux/25778) |
[API Telegram](https://core.telegram.org/bots/api) |
[Python telegram Bot](https://python-telegram-bot.org) |
[Making a telegram bot](https://www.sohamkamani.com/blog/2016/09/21/making-a-telegram-bot) |
[Distribute Messages effectively](epsagon.com/blog/distribute-messages-effectively-in-serverless-applications/) |
[Splitting your serverless framework api](https://www.gorillastack.com/news/splitting-your-serverless-framework-api-on-aws/) |
[10 passos para se criar um bot no telegram](https://medium.com/tht-things-hackers-team/10-passos-para-se-criar-um-bot-no-telegram-3c1848e404c4) |
[Building a chatbot using telegram and python](https://www.codementor.io/garethdwyer/building-a-chatbot-using-telegram-and-python-part-2-sqlite-databse-backend-m7o96jger)

## Exemplos:

[AWS Node Telegram Bot](https://github.com/serverless/examples/tree/9cdeee0e5694df595cde75acb03e33a5492ade8c/aws-node-telegram-echo-bot) |
[AWS Python Telegram Bot](https://github.com/serverless/examples/tree/cba47ffe0ef2ecf8180497db814ca8e40f9c1210/aws-python-telegram-bot) |
[Python Requirements Layer](https://github.com/serverless-components/python-requirements-layer)
