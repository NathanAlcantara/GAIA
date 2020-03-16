"use strict";

const { extractMessageOfEventSns } = require("/opt/utils/awsHelpers");
const { generateError, generateSuccess } = require("/opt/utils/helpers");

module.exports.write = async (event, ctx, callback) => {
  const data = extractMessageOfEventSns(event);

  console.log(`Recebendo para escrita de contexto o evento: ${JSON.stringify(data)}`);



  return generateSuccess(callback);
};
