"use strict";

const { publishSnsTopic } = require("/opt/utils/awsHelpers");

module.exports.writeContext = (chatId, command, context) => {
    const tableName = `Context-${process.env.STAGE}`;

    const modifiedDate = new Date().toISOString();

    const item = {
        chatId,
        command,
        context,
        modifiedDate
    }

    console.log("Escrevendo o contexto:", item);

    publishSnsTopic(chatId, { tableName, item }, "write-dynamo");
};

class Util {
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
    static convertObjectToAwsReadable(json) {
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
                                        values = value.map(data => ({ L: this.convertObjectToAwsReadable(data) }));
                                    } else {
                                        values = value.map(data => ({ M: this.convertObjectToAwsReadable(data) }));
                                    };

                                    jhon = createProperty({ L: values });
                                    break;
                            };
                        } else {
                            jhon = createProperty({ M: this.convertObjectToAwsReadable(value) });
                        };
                };
            };

            obj = { ...obj, ...jhon };
        })

        return obj;
    }
}

class ConditionBuilder {
    constructor() { }

    withProperty(property) {
        if (typeof property !== "string" || property == "") {
            throw "Must be a valid string"
        }
        this.property = property;
        return this;
    }
    withOperator(operator) {
        if (typeof operator !== "string" || operator == "") {
            throw "Must be a valid string"
        }
        this.operator = operator;
        return this;
    }
    withVariable(variable) {
        if (typeof variable !== "object" || !Object.entries(variable).length) {
            throw "Variable must be a valid object"
        }
        this.variable = variable;
        return this;
    }
    build() {
        if (!this.property || !this.operator || !this.variable) {
            throw "Property, Operator and variable are required"
        }
        const variableName = Object.keys(this.variable)[0];
        const variableValue = Object.values(this.variable)[0];
        const aliasValue = `:${variableName}Value`;
        this.values = { ...this.values, ...{ [aliasValue]: variableValue } };
        return `${this.property} ${this.operator} ${aliasValue}`;
    }
}

class ExpressionBuilder {
    constructor() { }

    withConditions(conditions) {
        if (!conditions || !conditions.length || (conditions && conditions.some(cond => !cond || !(cond instanceof ConditionBuilder)))) {
            throw "Parameter must be an Array of ConditionBuilder with at least one condition"
        }
        this.values = {};
        this.conditions = conditions.map(conditionBuilder => {
            const condition = conditionBuilder.build();
            this.values = { ...this.values, ...conditionBuilder.values };
            return condition;
        });
        return this;
    }
    withOperator(operator) {
        if (operator !== "AND" && operator !== "OR") {
            throw "Operator is wrong, choose AND or OR"
        }
        this.operator = ` ${operator} `;
        return this;
    }
    build() {
        if (this.conditions.length > 1 && !this.operator) {
            throw "You must inform an operator since you have more than one condition"
        }
        return this.conditions.join(this.operator);
    }
}

class Param {
    constructor(build) {
        this.TableName = build.tableName;
        if (build.fieldsToReturn) {
            this.ProjectionExpression = build.fieldsToReturn;
        }
        this.ExpressionAttributeValues = build.values;
        this.KeyConditionExpression = build.expression;
    }
}

class ParamsBuilder {
    constructor() { }

    withTableName(name) {
        this.tableName = name;
        return this;
    }

    thatReturnFields(fieldsToReturn) {
        if (typeof fieldsToReturn !== "object" || fieldsToReturn.some(field => typeof field !== "string" || field === "")) {
            throw "Parameter must be an Array of string with at least one field"
        }
        this.fieldsToReturn = fieldsToReturn.join(", ");
        return this;
    }

    withExpression(expression) {
        if (!(expression instanceof ExpressionBuilder)) {
            throw "Parameter must be a Builder"
        }
        this.values = Util.convertObjectToAwsReadable(expression.values);
        this.expression = expression.build();
        return this;
    }

    build() {
        if (!this.tableName || !this.values || !this.expression) {
            throw "TableName, Values and Expression are required"
        }
        return new Param(this);
    }
}

module.exports.convertObjectToAwsReadable = (json) => Util.convertObjectToAwsReadable(json);
module.exports.ConditionBuilder = ConditionBuilder;
module.exports.ExpressionBuilder = ExpressionBuilder;
module.exports.ParamsBuilder = ParamsBuilder;