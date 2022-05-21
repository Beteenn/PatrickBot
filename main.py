import telegram

def main():
    bot = telegram.Bot("5386118823:AAFwlYtjxLk8xDDB-ToyZSLXpG5A0fB3vBw")
    update = bot.get_updates()[-1]
    chat_id = update['message']['chat']['id']
    command_text = update['message']['text']
    reply_text: str
if 'listartarefa' in command_text:
    reply_text = 'listando tarefas...'
else:
    reply_text = 'voce precisa cadastrar outros comandos'

bot.send_message(chat_id=chat_id, text=reply_text)

main()