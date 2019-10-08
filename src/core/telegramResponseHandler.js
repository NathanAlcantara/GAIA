import { Bot } from "../utils/helpers";

export async function send(event) {
  console.log(`Recebendo para envio o evento: ${event}`);

  if (event.chatId) {
    if (event.message) {
      console.log(`Enviando mesagem: ${event.message}`);
      Bot.sendMessage(event.chatId, event.message);
    }
  }
}
