"use strict";

const { extractMessageOfEventSns, publishSnsTopic } = require("/opt/utils/awsHelpers");
const { COMMANDS, getCommandValueOnText } = require("/opt/utils/botHelpers");
const { generateError, generateSuccess } = require("/opt/utils/helpers");

module.exports.command = (event, ctx, callback) => {

  const data = extractMessageOfEventSns(event);

  console.log(`Recebendo a mensagem do telegram: ${JSON.stringify(data)}`);

  const { command, message, context } = data;

  if (message) {
    const { text } = message;

    if (text) {
      switch (command) {
        case COMMANDS.START:
          handleStartCommand(message, context);
          break;
        case COMMANDS.AJUDA:
          handleHelpCommand(text, message);
          break;
        case COMMANDS.CONTAR:
          handleCountCommand(text, message);
          break;
        case COMMANDS.NUMEROS:
          handleNumberCommand(text, message);
          break;
        case COMMANDS.LETRAS:
          handleLettersCommand(text, message);
          break;
        case COMMANDS.INICIAIS:
          handleInitialsCommand(text, message);
          break;
      };
    };

    return generateSuccess(callback);
  }

  return generateError(
    callback,
    "Não foi possível localizar o corpo da mensagem"
  );
};

function handleStartCommand(message, context) {
  const { from, chat } = message;
  const command = COMMANDS.START;
  const chatId = chat.id;

  console.log(`Context: ${context}`)

  if (context) {
    const messageType = "text";

    console.log(`Iniciando conversa com o ${from.first_name}`);

    const textAgain = `Olá ${from.first_name}, ainda com alguma dúvida?
Experimente usar /ajuda, você pode descobrir do que sou capaz xD`;

    const text = context.alreadyWelcome
      ? textAgain
      : `Bem vindo, eu sou Gaia, o Cacique dos bots!
Duvidas? Por favor, utilize o comando /ajuda, nele voce encontra um guia rápido e tudo o que voce precisa saber sobre mim ;)`;

    publishSnsTopic(chatId, { command, context: { alreadyWelcome: true } }, "write-telegram-context");

    publishSnsTopic(chatId, { text, messageType });
  } else {
    publishSnsTopic(chatId, { message, command }, "read-telegram-context");
  }
};

function handleHelpCommand(text, message) {
  const messageType = "text";
  const { from, chat } = message;
  const chatId = chat.id;

  const characters = getCommandValueOnText(COMMANDS.AJUDA, text);

  console.log(`O usuário ${from.first_name} solicitou ajuda`);

  publishSnsTopic(chatId, { characters, messageType }, "help");
};

function handleCountCommand(text, message) {
  const messageType = "text";
  const { from, chat } = message;
  const chatId = chat.id;

  const characters = getCommandValueOnText(COMMANDS.CONTAR, text);

  console.log(`O usuário ${from.first_name} solicitou uma contagem`);

  publishSnsTopic(
    chatId,
    { characters, messageType },
    "count-characters"
  );
};

function handleNumberCommand(text, message) {
  const messageType = "text";
  const { from, chat } = message;
  const chatId = chat.id;

  const characters = getCommandValueOnText(COMMANDS.NUMEROS, text);

  console.log(
    `O usuário ${from.first_name} solicitou uma conversão de letra para números`
  );

  publishSnsTopic(
    chatId,
    { characters, messageType },
    "alphabet-number"
  );
};

function handleLettersCommand(text, message) {
  const messageType = "text";
  const { from, chat } = message;
  const chatId = chat.id;

  const characters = getCommandValueOnText(COMMANDS.LETRAS, text);

  console.log(
    `O usuário ${from.first_name} solicitou uma conversão de números para letras`
  );

  publishSnsTopic(
    chatId,
    { characters, messageType },
    "number-alphabet"
  );
};

function handleInitialsCommand(text, message) {
  const messageType = "text";
  const { from, chat } = message;
  const chatId = chat.id;

  const characters = getCommandValueOnText(COMMANDS.INICIAIS, text);

  console.log(
    `O usuário ${from.first_name} solicitou uma extração de iniciais e finais`
  );

  publishSnsTopic(
    chatId,
    { characters, messageType },
    "get-initials"
  );
};