"use strict";

const request = require("request-promise-native");
const enviroments = require("../enviroments.json");

const { TELEGRAM_TOKEN } = enviroments;

module.exports.TELEGRAM_TOKEN = TELEGRAM_TOKEN;

module.exports.getValueCommandPrototype = function(command) {
  command = `/${command}`;
  const regex = new RegExp(command);
  const { input } = this.match(regex);
  return input.substring(input.indexOf(command) + command.length);
};

module.exports.isCommandExistPrototype = function(command) {
  command = `/${command}`;
  const regex = new RegExp(command);
  return Boolean(this.match(regex));
};

module.exports.executeMethodBot = async (methodName, methodBody) => {
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
