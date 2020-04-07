"use strict";

const aws = require("aws-sdk");

const { writeContext, ConditionBuilder, ExpressionBuilder, ParamsBuilder } = require("/opt/utils/dynamodbHelpers");
const { extractMessageOfEventSns, publishSnsTopic } = require("/opt/utils/awsHelpers");
const { generateError, generateSuccess } = require("/opt/utils/helpers");

module.exports.read = async (event, ctx, callback) => {
  const data = extractMessageOfEventSns(event);

  console.log(`Recebendo para leitura de contexto o evento: ${JSON.stringify(data)}`);

  const { command, message, contextDefault } = data;

  if (message) {
    const { chat } = message;
    const chatId = chat.id;

    const dynamoDB = new aws.DynamoDB();

    const chatIdConditionBuilder = new ConditionBuilder()
      .withProperty("chatId")
      .withOperator("=")
      .withVariable({ chatId });

    let expressionBuilder = new ExpressionBuilder()
      .withConditions([chatIdConditionBuilder])
      .withOperator("AND");

    if (command) {
      const commandConditionBuilder = new ConditionBuilder()
        .withProperty("command")
        .withOperator("=")
        .withVariable({ command });

      expressionBuilder = new ExpressionBuilder()
        .withConditions([chatIdConditionBuilder, commandConditionBuilder])
        .withOperator("AND");
    };

    const params = new ParamsBuilder()
      .withTableName(`Context-${process.env.STAGE}`)
      .thatReturnFields(["command", "context", "modifiedDate"])
      .withExpression(expressionBuilder)
      .build();

    console.log(`Procurando contextos usando os parâmetros: ${JSON.stringify(params)}`)

    const { Items } = await dynamoDB.query(params).promise()
      .catch(error => generateError(callback, "Error ao pegar o contexto", error));

    console.log("Items encontrados:", JSON.stringify(Items));

    if (Items && Items.length) {
      console.log(`Encontrado ${Items.length} contextos`);

      let recentItem;

      if (Items.length > 1) {
        const convertedItems = Items.map(convertAwsItemToObjetReadable).sort((a, b) => compareDateDesc(a.modifiedDate, b.modifiedDate));

        recentItem = convertedItems[0];
      } else {
        recentItem = Items.map(convertAwsItemToObjetReadable)[0];
      }

      const { context, command } = recentItem;

      publishSnsTopic(chatId, { message, context, command }, "handle-telegram-command");

      return generateSuccess(callback);
    } else if (command) {

      console.log(`Contexto não encontrado para o comando ${command}, criando um padrão: ${JSON.stringify(contextDefault)}`);

      writeContext(chatId, command, contextDefault);

      setTimeout(() => {
        publishSnsTopic(chatId, { message, command, contextDefault }, "read-telegram-context");
      }, 500);
    };

    return generateError(callback, "Contexto não encontrado");
  };

  return generateError(callback, "Mensagem não encontrada");
};

function convertAwsItemToObjetReadable(item) {
  let convertedItem = {};

  Object.entries(item)
    .forEach(entry => {
      const entryName = entry[0];
      let entryValue = Object.values(entry[1])[0];

      if (typeof entryValue === "object") {
        entryValue = convertAwsItemToObjetReadable(entryValue);
      }

      convertedItem = { ...convertedItem, [entryName]: entryValue };
    });

  return convertedItem;
};

function compareDateDesc(dirtyDateLeft, dirtyDateRight) {
  const dateLeft = new Date(dirtyDateLeft);
  const dateRight = new Date(dirtyDateRight);

  const diff = dateLeft.getTime() - dateRight.getTime();

  if (diff > 0) {
    return -1;
  } else if (diff < 0) {
    return 1;
    // Return 0 if diff is 0; return NaN if diff is NaN
  } else {
    return diff;
  }
};