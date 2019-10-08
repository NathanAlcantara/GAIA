import aws from "aws-sdk";
import TelegramBot from "node-telegram-bot-api";

const AWS_REGION = process.env.REGION;
const AWS_ACCOUNT_ID = process.env.ACCOUNT_ID;
export const TELEGRAM_TOKEN = process.env.TELEGRAM_TOKEN;

export const Bot = new TelegramBot(TELEGRAM_TOKEN);

export function generateResponse(
  payload = "Successfuly to send message",
  code = 200
) {
  console.log(payload);
  return {
    statusCode: code,
    body: JSON.stringify(payload)
  };
}

export function generateError(err = "Oops, something went wrong", code = 500) {
  console.error(err);
  return generateResponse(
    {
      message: err.message
    },
    code
  );
}

export function extractMessageOfEventSns(event) {
  return event.Records[0].Sns.Message;
}

export function publishSnsTopic(
  chatId,
  message,
  snsName = "send-telegram-response"
) {
  const sns = new aws.SNS({ region: "us-east-1" });

  const body = JSON.stringify({
    chatId,
    message
  });

  console.log(`Publicando mensagem: ${body}, no sns: "${snsName}"`);

  const arnSNS = `arn:aws:sns:${AWS_REGION}:${AWS_ACCOUNT_ID}:${snsName}`;

  const params = {
    Message: body,
    TopicArn: arnSNS
  };
  sns.setPlatformApplicationAttributes({
    Attributes: {
      SuccessFeedbackRoleArn: "arn:aws:iam::111122223333:role/SNS_CWlogs",
      SuccessFeedbackSampleRate: 5
    },
    PlatformApplicationArn: arnSNS
  });

  return sns.publish(params).promise();
}
