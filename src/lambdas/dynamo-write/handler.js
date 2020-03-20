"use strict";

const aws = require("aws-sdk");

const { convertObjectToAwsReadable } = require("/opt/utils/dynamodbHelpers");
const { extractMessageOfEventSns } = require("/opt/utils/awsHelpers");
const { generateError, generateSuccess } = require("/opt/utils/helpers");

module.exports.write = async (event, ctx, callback) => {
  const data = extractMessageOfEventSns(event);

  console.log(`Recebendo para escrita do item, o evento: ${JSON.stringify(data)}`);

  const { tableName, item } = data;

  const dynamoDB = new aws.DynamoDB();

  const params = {
    TableName: tableName,
    Item: convertObjectToAwsReadable(item)
  };

  console.log(`Parâmetros para criação/atualização do item: ${JSON.stringify(params)}`)

  return dynamoDB
    .putItem(params)
    .promise()
    .then(() => generateSuccess(callback, "Sucesso ao criar/atualizar o item"))
    .catch(error => generateError(callback, "Error ao criar/atualizar o item", error));
};