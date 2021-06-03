import os
import logging

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.utils.helpers import mention_markdown

from database import BotDatabase

TOKEN = os.getenv('TGBOT_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

db = BotDatabase('database.db')


def start_command(update, context):
    message = 'Hey! Birinin ihtiyacı olduğunda gruptaki herkese 📢 bildirimde bulunmaya yardımcı olabilirim. ' kullanılarak belirtilebilir.
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def in_command(update, context):
    chat_id = update.effective_chat.id
    user = update.effective_user
    user_name = user.username or user.first_name or 'anonim'
    db.add_user(user.id, user_name)
    db.add_user_to_chat(chat_id, user.id)
    message = f'Thanks for opting in {user_name}'
    context.bot.send_message(chat_id=chat_id, text=message)


def out_command(update, context):
    chat_id = update.effective_chat.id
    user = update.effective_user
    user_name = user.username or user.first_name or 'anonim'
    db.delete_user_from_chat(chat_id, user.id)
    message = f'You\' ve been opted out {user_name}'
    context.bot.send_message(chat_id=chat_id, text=message)


def chunks(elements, size):
    n = max(1, size)
    return (elements[i:i + n] for i in range(0, len(elements), n))


def unicode_truncate(s, length, encoding='utf-8'):
    encoded = s.encode(encoding)[:length]
    return encoded.decode(encoding, 'ignore')


def all_command(update, context):
    chat_id = update.effective_chat.id
    user_list = db.get_users_from_chat(chat_id)
    if not user_list:
        message = 'Kullanıcı yok. Seçmek için /in komutunu yazın'
        context.bot.send_message(chat_id=chat_id, text=message)
    else:
        mentions = [mention_markdown(user_id, unicode_truncate(user_name, 100), version=2)
                    for user_id, user_name in user_list]
        for chunk in chunks(mentions, 4):
            message = ' '.join(chunk)
            context.bot.send_message(
                chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.MARKDOWN_V2)


def stats_command(update, context):
    message = f'user_count: {db.count_users()[0]}\n' \
              f'chat_count: {db.count_chats()[0]}\n' \
              f'group_count: {db.count_groups()[0]}'
    context.bot.send_message(update.effective_chat.id, text=message)


def unknown_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Üzgünüm, bu komutu anlamadım.")


updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

handlers = [
    CommandHandler('in', in_command),
    CommandHandler('all', all_command),
    CommandHandler('out', out_command),
    CommandHandler('start', start_command),
    CommandHandler('stats', stats_command),
    MessageHandler(Filters.command, unknown_command),
]

for handler in handlers:
    dispatcher.add_handler(handler)

updater.start_polling()
updater.idle()

db.close()
