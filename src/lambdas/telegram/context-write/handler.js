"use strict";

const aws = require("aws-sdk");

const { extractMessageOfEventSns } = require("/opt/utils/awsHelpers");
const { generateError, generateSuccess } = require("/opt/utils/helpers");

module.exports.write = async (event, ctx, callback) => {
  const data = extractMessageOfEventSns(event);

  console.log(`Recebendo para escrita de contexto o evento: ${JSON.stringify(data)}`);

  const { chatId, command, context = {} } = data;

  const dynamoDB = new aws.DynamoDB();
  const modifiedDate = new Date().toISOString();

  const item = {
    chatId,
    command,
    context,
    modifiedDate
  }

  const params = {
    TableName: `Context-${process.env.STAGE}`,
    Item: convertObjectToAwsReadable(item)
  };

  console.log(`Parâmetros para criação/atualização do item: ${JSON.stringify(params)}`)

  return dynamoDB
    .putItem(params)
    .promise()
    .then(() => generateSuccess(callback, "Sucesso ao criar/atualizar o context"))
    .catch(error => generateError(callback, "Error ao criar/atualizar o contexto", error));
};

/**
 * Converte um objeto json comum para um objeto em que a aws consiga ler
 * 
 * @param json Objeto a ser convertido 
 * @returns {AttributeValue} Objecto AWS Readable
 * 
 *@example
 * Input: 
 *  {
 *    step: 1,
 *    name: "Começando"
 *  }
 * 
 * Output:
 *  {
 *    step: {
 *      N: "1"
 *    },
 *    name: {
 *      S: "Começando"
 *    }
 *  }
 */
function convertObjectToAwsReadable(json) {
  let obj = {};

  Object.entries(json).forEach(entry => {
    const property = entry[0];
    const value = entry[1];
    let jhon;

    function createProperty(value) {
      return { [property]: value }
    }

    if (value === null) {
      jhon = createProperty({ NULL: true });
    } else {
      switch (typeof value) {
        case "string":
          jhon = createProperty({ S: value });
          break;
        case "number":
          jhon = createProperty({ N: value.toString() });
          break;
        case "boolean":
          jhon = createProperty({ BOOL: value });
          break;
        case "object":
          if (value.length) {
            const firstValue = value[0];

            switch (typeof firstValue) {
              case "string":
                jhon = createProperty({ SS: value });
                break;
              case "number":
                jhon = createProperty({ NS: value.map(data => data.toString()) });
                break;
              case "object":
                let values;

                if (firstValue.length) {
                  values = value.map(data => ({ L: convertObjectToAwsReadable(data) }));
                } else {
                  values = value.map(data => ({ M: convertObjectToAwsReadable(data) }));
                };

                jhon = createProperty({ L: values });
                break;
            };
          } else {
            jhon = createProperty({ M: convertObjectToAwsReadable(value) });
          };
      };
    };

    obj = { ...obj, ...jhon };
  })

  return obj;
}