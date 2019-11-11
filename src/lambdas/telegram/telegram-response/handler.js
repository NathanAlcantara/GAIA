"use strict";

const { extractMessageOfEventSns } = require("/opt/utils/awsHelpers");
const { executeMethodBot } = require("/opt/utils/botHelpers");
const { generateError, generateSuccess } = require("/opt/utils/helpers");

module.exports.send = async (event, context, callback) => {
  const data = extractMessageOfEventSns(event);

  console.log(`Recebendo para envio o evento: ${JSON.stringify(data)}`);

  let command, bodyToSend;
  const { chatId: chat_id, messageType } = data;
  const { text, fileId } = data;

  if (chat_id && messageType) {
    console.log(`Enviando uma mensagem do tipo: ${messageType}`);
    switch (messageType) {
      case "text":
        command = "sendMessage";
        bodyToSend = { text };
        console.log(`Enviando texto: ${text}`);
        break;
      case "photo":
        command = "sendPhoto";
        bodyToSend = { photo: fileId };
        console.log(`Enviando photo com o fileId: ${fileId}`);
        break;
      case "audio":
        command = "sendAudio";
        bodyToSend = { audio: fileId };
        console.log(`Enviando audio com o fileId: ${fileId}`);
        break;
      case "document":
        command = "sendDocument";
        bodyToSend = { document: fileId };
        console.log(`Enviando documento com o fileId: ${fileId}`);
        break;
      default:
        return generateError(callback, "MessageType not found");
    }

    if (text || fileId) {
      executeMethodBot(command, { ...{ chat_id }, ...bodyToSend });
    } else {
      return generateError(callback, "Body to telegram is invalid");
    }

    return generateSuccess(callback);
  }

  return generateError(callback, "ChatId and MessageType are required");
};
