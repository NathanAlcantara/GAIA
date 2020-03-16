"use strict";

const request = require("request-promise-native");
const environment = require("../environment.json");

const { TELEGRAM_TOKEN } = environment;

module.exports.TELEGRAM_TOKEN = TELEGRAM_TOKEN;

module.exports.COMMANDS = Object.freeze({
  START: "start",
  AJUDA: "ajuda",
  CONTAR: "contar",
  NUMEROS: "numeros",
  LETRAS: "letras",
  INICIAIS: "iniciais"
});

module.exports.hasAnyCommandOnText = (text) => {
  return Object.values(this.COMMANDS).some(command => this.isCommandExistOnText(command, text));
}

module.exports.getAllCommandsOnText = (text) => {
  return Object.values(this.COMMANDS).filter(command => this.isCommandExistOnText(command, text));
}

module.exports.getCommandValueOnText = (command, text) => {
  command = `/${command}`;
  const regex = new RegExp(command);
  const { input } = text.match(regex);
  return input.substring(input.indexOf(command) + command.length);
};

module.exports.isCommandExistOnText = (command, text) => {
  command = `/${command}`;
  const regex = new RegExp(command);
  return Boolean(text.match(regex));
};

module.exports.executeMethodBot = async (methodName, methodBody) => {
  console.log(
    `Chamando API ${methodName} com o corpo ${JSON.stringify(methodBody)}`
  );

  const options = {
    method: "POST",
    uri: `https://api.telegram.org/bot${TELEGRAM_TOKEN}/${methodName}`,
    body: methodBody,
    json: true
  };

  return request(options).catch(err =>
    console.error(`Error trying execute method ${methodName}`, err)
  );
};
