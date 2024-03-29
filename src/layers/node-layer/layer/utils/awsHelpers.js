"use strict";

const aws = require("aws-sdk");
const environment = require("../environment.json");

const { AWS_REGION } = process.env;
const { AWS_ACCOUNT_ID, TENANT } = environment;

module.exports.TENANT = TENANT.toLowerCase();

module.exports.extractMessageOfEventSns = event => {
  return JSON.parse(event.Records[0].Sns.Message);
};

module.exports.publishSnsTopic = (
  chatId,
  payload,
  snsName = "send-telegram-response"
) => {
  const sns = new aws.SNS({ region: AWS_REGION });

  if (payload && payload.messageType) {
    payload.messageType = payload.messageType.toLowerCase();
  }

  const body = JSON.stringify({ ...{ chatId }, ...payload });

  console.log(`Publicando mensagem: ${body} no sns: "${TENANT}-${snsName}"`);

  const arnSNS = `arn:aws:sns:${AWS_REGION}:${AWS_ACCOUNT_ID}:${TENANT}-${snsName}`;

  const params = {
    Message: body,
    TopicArn: arnSNS
  };

  return sns
    .publish(params)
    .promise()
    .catch(error => console.error("Error ao publicar mensagem no sns", error));
};