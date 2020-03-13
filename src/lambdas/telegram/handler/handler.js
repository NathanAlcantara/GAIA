"use strict";

const { publishSnsTopic } = require("/opt/utils/awsHelpers");
const { getAllCommandsOnText, hasAnyCommandOnText } = require("/opt/utils/botHelpers");
const { generateError, generateSuccess } = require("/opt/utils/helpers");

module.exports.main = (event, ctx, callback) => {
  console.log(`Event: ${JSON.stringify(event)}`);

  let { body } = event;

  body = JSON.parse(body);

  if (body) {
    console.log(`Telegram se comunicando com o corpo: ${JSON.stringify(body)}`);

    const { message } = body;

    if (message) {
      const { text, from, chat } = message;
      const chatId = chat.id;

      console.log(`Iniciando conversa com o ${from.first_name}`);

      if (text) {
        if (hasAnyCommandOnText(text)) {
          const commands = getAllCommandsOnText(text);

          console.log(`Esses comandos foram encontrados no texto: ${commands.join(", ")}`);

          commands.forEach(command => {
            publishSnsTopic(chatId, { message, command }, "handle-telegram-command");
          })
        } else {
          console.log("Nenhum comando encontrado, iniciando busca de contexto");

          publishSnsTopic(chatId, { message }, "context-read");
        }
      }
    }

    return generateSuccess(callback);
  }

  return generateError(
    callback,
    "Não foi possível localizar o corpo da mensagem"
  );
};
