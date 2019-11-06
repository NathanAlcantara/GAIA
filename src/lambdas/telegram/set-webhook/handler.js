"use strict";

const { TENANT } = require("/opt/utils/awsHelpers");
const { executeMethodBot, TELEGRAM_TOKEN } = require("/opt/utils/botHelpers");
const { generateError, generateSuccess } = require("/opt/utils/helpers");

module.exports.setWebhook = async (event, context, callback) => {
  console.log("Iniciando configuração do bot");

  const requestContext = event.requestContext;
  const telegramTokenId = TELEGRAM_TOKEN.split(":")[0];

  const url = `https://${requestContext.domainName}/${requestContext.stage}/telegram/${TENANT}${telegramTokenId}`;

  console.log(`Setando webhook na url: ${url}}`);

  let body = { successMessage: `Webhook setado na url: ${url}` };

  await executeMethodBot("setWebhook", { url }).catch(error => {
    body = { errorMessage: "Ocorreu um erro ao setar o webhook", error };
  });

  if (body.errorMessage) {
    return generateError(callback, body);
  }

  return generateSuccess(callback, body);
};
