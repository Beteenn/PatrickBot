import os
import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import telegram
from models import MultiItems, User
import config

# Actions

def teste(update, context):
    print('Reply user')
    add_typing(update, context)

    buttons = MultiItems("What would you like to receive?", ["Felinha", "Projetinho"])
    add_suggested_actions(update, context, buttons)

def add_suggested_actions(update, context, response):
    options = []

    for item in response.items:
        options.append(InlineKeyboardButton(item, callback_data=item))

    reply_markup = InlineKeyboardMarkup([options])

    # update.message.reply_text(response.message, reply_markup=reply_markup)
    context.bot.send_message(chat_id=get_chat_id(update, context), text=response.message, reply_markup=reply_markup)

# Sent messages
def add_typing(update, context):
    context.bot.send_chat_action(chat_id=get_chat_id(update, context), action=telegram.ChatAction.TYPING, timeout=1)
    time.sleep(1)

def add_text_message(update, context, message):
    if update.message is not None:
        update.message.reply_text(message)
    elif update.callback_query is not None:
        update.callback_query.message.edit_text(message)

# Get info chat
def get_text_from_message(update):
    return update.message.text
    
def get_text_from_callback(update):
    return update.callback_query.data

def get_chat_id(update, context):
    chat_id = -1

    if update.message is not None:
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        chat_id = context.bot_data[update.poll.id]

    return chat_id

def get_user(update):
    user: User = None

    _from = None

    if update.message is not None:
        _from = update.message.from_user
    elif update.callback_query is not None:
        _from = update.callback_query.from_user

    if _from is not None:
        user = User()
        user.id = _from.id
        user.first_name = _from.first_name if _from.first_name is not None else ''
        user.last_name = _from.last_name if _from.last_name is not None else ''
        user.lang = _from.language_code if _from.language_code is not None else 'n/a'

    print.info(f'from {user}')

    return user

# Handler
def main_handler(update, context):
    print(f'update : {update}')

    if update.message is not None:
        user_input = get_text_from_message(update)
        print(f'user_input : {user_input}')

        # reply
        add_typing(update, context)
        add_text_message(update, context, f"You said: {user_input}")

    elif update.callback_query is not None:
        user_input = get_text_from_callback(update)
        print(f'user_input : {user_input}')

        if user_input == 'Felinha':
            add_typing(update, context)
            add_text_message(update, context, "Fala felinhaa 😎")
        elif user_input == 'Projetinho':
            add_typing(update, context)
            add_text_message(update, context, "Bora sacar o shape fella 😎")

def main():
    print('Start')
    updater = Updater(config.DefaultConfig.TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher
    print('Listening')

    # command handlers
    dp.add_handler(CommandHandler("listartarefa", teste))

    # message handler
    dp.add_handler(MessageHandler(Filters.text, main_handler))

    # suggested_actions_handler
    dp.add_handler(CallbackQueryHandler(main_handler, pass_chat_data=True, pass_user_data=True))

    # Start the Bot
    updater.start_polling()

    updater.idle()

main()
