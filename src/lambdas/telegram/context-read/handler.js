"use strict";

const { extractMessageOfEventSns } = require("/opt/utils/awsHelpers");
const { generateError, generateSuccess } = require("/opt/utils/helpers");

module.exports.read = async (event, ctx, callback) => {
  const data = extractMessageOfEventSns(event);

  console.log(`Recebendo para leitura de contexto o evento: ${JSON.stringify(data)}`);

  

  return generateSuccess(callback);
};
