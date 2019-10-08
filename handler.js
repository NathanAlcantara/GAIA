import {
  Bot,
  generateError,
  generateResponse,
  publishSnsTopic,
  TELEGRAM_TOKEN
} from "./src/utils/helpers";

export function telegram(event) {
  console.log(`Event: ${event}`);

  if (event.body) {
    const data = JSON.parse(event.body);

    console.log(`Telegram se comunicando com o corpo: ${data}`);

    Bot.onText(/\/start/, ({ from, chat }) => {
      console.log(`Iniciando conversa com o ${from.username}`);

      const chatId = chat.id;

      const data = `Bem vindo, eu sou Gaia, o Cacique dos bots! \n
        Duvidas? Por favor, utilize o comando /ajuda, \n
        nele voce encontra um guia rápido e tudo o que voce precisa saber sobre mim ;)`;

      publishSnsTopic(chatId, data);
    });

    Bot.onText(/\/ajuda/, ({ from, chat }) => {
      console.log(`O usuário ${from.username} pediu por ajuda`);

      const chatId = chat.id;

      const data = `Nothing to do here, move along... \n
      Um dia nos vamos fazer um menu de ajuda dahora, \n
      mas por enquanto, só sei contar, use /contar e veja por si mesmo`;

      publishSnsTopic(chatId, data);
    });

    Bot.onText(/\/contar (.+)/, ({ from, chat }, match) => {
      console.log(`O usuário ${from.username} solicitou uma contagem`);

      const chatId = chat.id;

      publishSnsTopic(chatId, "Contando...");
      publishSnsTopic(chatId, { characteres: match[1] }, "count-characteres");
    });

    return generateResponse();
  }

  return generateError("Não foi possível localizar o corpo da mesagem");
}

export async function setWebhook(event) {
  const url = `https://${event.host}/${event.stage}/telegram/${TELEGRAM_TOKEN}`;

  console.log(`Setando webhook na url: ${url}}`);

  let code = 200;
  let body = { successMessage: `Webhook setado na url: ${url}` };

  await Bot.setWebHook(url).catch(error => {
    code = 500;
    body = { errorMessage: "Ocorreu um erro ao setar o webhook", error };
  });

  return {
    statusCode: code,
    body: JSON.stringify({ body })
  };
}
