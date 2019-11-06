"use strict";

const { publishSnsTopic } = require("/opt/utils/awsHelpers");
const {
  getValueCommandPrototype,
  isCommandExistPrototype
} = require("/opt/utils/botHelpers");
const { generateError, generateSuccess } = require("/opt/utils/helpers");

String.prototype.isCommandExist = isCommandExistPrototype;
String.prototype.getValueCommand = getValueCommandPrototype;

module.exports.main = (event, context, callback) => {
  console.log(`Event: ${JSON.stringify(event)}`);

  let { body } = event;

  body = JSON.parse(body);

  if (body) {
    console.log(`Telegram se comunicando com o corpo: ${body}`);

    const { message } = body;

    console.log(message);

    if (message) {
      const { text } = message;

      console.log(text);

      if (text) {
        if (text.isCommandExist("start")) {
          const { from, chat } = message;
          console.log(`Iniciando conversa com o ${from.first_name}`);

          const chatId = chat.id;

          const data = `Bem vindo, eu sou Gaia, o Cacique dos bots!
          Duvidas? Por favor, utilize o comando /ajuda,
          nele voce encontra um guia rápido e tudo o que voce precisa saber sobre mim ;)`;

          publishSnsTopic(chatId, "text", data);
        }

        if (text.isCommandExist("ajuda")) {
          const { from, chat } = message;
          console.log(`O usuário ${from.first_name} pediu por ajuda`);

          const chatId = chat.id;

          const data = `Nothing to do here, move along...
          Um dia nos vamos fazer um menu de ajuda dahora,
          mas por enquanto, só sei contar, use /contar e veja por si mesmo`;

          publishSnsTopic(chatId, "text", data);
        }

        if (text.isCommandExist("contar")) {
          const left = text.getValueCommand("contar");
          const { from, chat } = message;

          console.log(`O usuário ${from.first_name} solicitou uma contagem`);

          const chatId = chat.id;

          publishSnsTopic(chatId, "text", "Contando...");
          publishSnsTopic(
            chatId,
            "text",
            { characteres: left },
            "count-characteres"
          );
        }
      }
    }

    return generateSuccess(callback);
  }

  return generateError(
    callback,
    "Não foi possível localizar o corpo da mesagem"
  );
};
