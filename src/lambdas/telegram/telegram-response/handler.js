"use strict";

const { extractMessageOfEventSns } = require("/opt/utils/awsHelpers");
const { executeMethodBot } = require("/opt/utils/botHelpers");
const { generateError, generateSuccess } = require("/opt/utils/helpers");

module.exports.send = async (event, context, callback) => {
  const data = extractMessageOfEventSns(event);

  console.log(`Recebendo para envio o evento: ${JSON.stringify(data)}`);

  const { chatId: chat_id, message, messageType } = data;

  if (chat_id && message) {
    console.log(`Enviando mesagem: ${message}`);
    switch (messageType) {
      case "text":
        executeMethodBot("sendMessage", { chat_id, text: message });
        break;
      default:
        return generateError(callback, "MessageType not found");
    }

    return generateSuccess(callback);
  }

  return generateError(callback, "ChatId and Message are required");
};
