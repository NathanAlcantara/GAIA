"use strict";

module.exports.generateSuccess = (
  callback,
  payload = "Successfuly to send message",
  code = 200
) => {
  const body = JSON.stringify(payload);

  console.log(body);

  const response = {
    statusCode: code,
    body
  };

  return callback(null, response);
};

module.exports.generateError = (
  callback,
  payload = "Oops, something went wrong",
  code = 500
) => {
  const body = JSON.stringify(payload);

  console.error(body);

  const response = {
    statusCode: code,
    body
  };

  return callback(null, response);
};
