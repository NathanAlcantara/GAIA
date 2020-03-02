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
    console.log(`Telegram se comunicando com o corpo: ${JSON.stringify(body)}`);

    const { message } = body;

    if (message) {
      const { text } = message;
      let messageType;

      if (text) {
        messageType = "text";

        if (text.isCommandExist("start")) {
          const { from, chat } = message;
          console.log(`Iniciando conversa com o ${from.first_name}`);

          const chatId = chat.id;

          const text = `Bem vindo, eu sou Gaia, o Cacique dos bots!
Duvidas? Por favor, utilize o comando /ajuda, nele voce encontra um guia rápido e tudo o que voce precisa saber sobre mim ;)`;

          publishSnsTopic(chatId, { text, messageType });
        }

        if (text.isCommandExist("ajuda")) {
          const characters = text.getValueCommand("ajuda");
          const { from, chat } = message;

          console.log(`O usuário ${from.first_name} solicitou ajuda`);

          const chatId = chat.id;

          publishSnsTopic(chatId, { characters, messageType }, "help");
        }

        if (text.isCommandExist("contar")) {
          const characteres = text.getValueCommand("contar");
          const { from, chat } = message;

          console.log(`O usuário ${from.first_name} solicitou uma contagem`);

          const chatId = chat.id;

          publishSnsTopic(
            chatId,
            { characters, messageType },
            "count-characters"
          );
        }

        if (text.isCommandExist("numeros")) {
          const characters = text.getValueCommand("numeros");
          const { from, chat } = message;
          console.log(
            `O usuário ${from.first_name} solicitou uma conversão de letra para números`
          );

          const chatId = chat.id;

          publishSnsTopic(
            chatId,
            { characters, messageType },
            "alphabet-number"
          );
        }

        if (text.isCommandExist("letras")) {
          const characters = text.getValueCommand("letras");
          const { from, chat } = message;

          console.log(
            `O usuário ${from.first_name} solicitou uma conversão de números para letras`
          );

          const chatId = chat.id;

          publishSnsTopic(
            chatId,
            { characters, messageType },
            "number-alphabet"
          );
        }
        
        if (text.isCommandExist("iniciais")) {
          const characters = text.getValueCommand("iniciais");
          const { from, chat } = message;

          console.log(
            `O usuário ${from.first_name} solicitou uma extração de iniciais e finais`
          );

          const chatId = chat.id;

          publishSnsTopic(chatId, { characters, messageType }, "get-initials");
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
