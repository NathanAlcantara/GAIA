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
          const { from, chat } = message;
          console.log(`O usuário ${from.first_name} pediu por ajuda`);

          const chatId = chat.id;

          const text = `Nothing to do here, move along...
Um dia nos vamos fazer um menu de ajuda dahora, mas por enquanto, só sei contar, use /contar e veja por si mesmo`;

          publishSnsTopic(chatId, { text, messageType });
        }

        if (text.isCommandExist("contar")) {
          const characteres = text.getValueCommand("contar");
          const { from, chat } = message;

          console.log(`O usuário ${from.first_name} solicitou uma contagem`);

          const chatId = chat.id;

          const chatId2 = chatId.toString();

          //const text2 = "Contando...";
          // publishSnsTopic(chatId, { text, messageType });
          publishSnsTopic(
            chatId2,
            { characteres, messageType },
            "count-characteres"
          );
        }
        if (text.isCommandExist("numeros")) {
          const characteres = text.getValueCommand("numeros");
          const { from, chat } = message;

          console.log(
            `O usuário ${from.first_name} solicitou uma conversao de letra para numeros`
          );

          const chatId = chat.id;

          const chatId2 = chatId.toString();

          //const text2 = "Contando...";
          // publishSnsTopic(chatId, { text, messageType });
          publishSnsTopic(
            chatId2,
            { characteres, messageType },
            "alphabet-number"
          );
        }
        if (text.isCommandExist("letras")) {
          const characteres = text.getValueCommand("letras");
          const { from, chat } = message;

          console.log(
            `O usuário ${from.first_name} solicitou uma conversao de numeros para letras`
          );

          const chatId = chat.id;

          const chatId2 = chatId.toString();

          //const text2 = "Contando...";
          // publishSnsTopic(chatId, { text, messageType });
          publishSnsTopic(
            chatId2,
            { characteres, messageType },
            "number-alphabet"
          );
        }
        if (text.isCommandExist("iniciais")) {
          const characteres = text.getValueCommand("iniciais");
          const { from, chat } = message;

          console.log(
            `O usuário ${from.first_name} solicitou uma extracao de iniciais e finais`
          );

          const chatId = chat.id;

          const chatId2 = chatId.toString();

          //const text2 = "Contando...";
          // publishSnsTopic(chatId, { text, messageType });
          publishSnsTopic(
            chatId2,
            { characteres, messageType },
            "get-initials"
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
