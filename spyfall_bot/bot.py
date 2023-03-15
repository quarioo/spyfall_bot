import os
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

import message_texts
import db

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TYPING_PLAYERS_NUMBER, TYPING_ROOM_NAME, ROOM_ALREADY_EXISTS, \
    INPUT_PLAYERS_NUMBER, INPUT_DURATION, START_GAME = range(6)
DB, ROOM_NAME, NUM_OF_PLAYERS, DURATION = range(4)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    exit('Specify TELEGRAM_BOT_TOKEN env variable')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_chat = update.effective_chat
    if effective_chat is None:
        logger.warning('effective_chat is None in /start')

    if update.message.from_user.id == 1057396264:
        await context.bot.send_message(chat_id=effective_chat.id,
                                       text=message_texts.GREETINGS + '\n~creator loves you')
    else:
        await context.bot.send_message(chat_id=effective_chat.id,
                                       text=message_texts.GREETINGS)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    effective_chat = update.effective_chat
    if effective_chat is None:
        logger.warning('effective_chat is None in /help')

    await context.bot.send_message(chat_id=effective_chat.id,
                                   text=message_texts.HELP)


async def createroom(update: Update, context: ContextTypes.user_data):
    effective_chat = update.effective_chat
    if effective_chat is None:
        logger.warning('effective_chat is None in /createroom')

    user = update.message.from_user
    logger.info("User %s started the conversation.", user.id)

    await update.message.reply_text(text=message_texts.CREATING_GAME_1)

    return TYPING_ROOM_NAME


async def save_room_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save input room name and returns to next function"""
    user_data = context.user_data
    user_data[ROOM_NAME] = update.message.text

    if await db.is_room_in_db(user_data[ROOM_NAME]) is True:
        return await input_duration(update, context)
    else:
        return await room_already_exists(update, context)


async def room_already_exists(update: Update, context: ContextTypes.user_data):
    await update.message.reply_text(text=message_texts.ROOM_ALREADY_EXISTS)

    return TYPING_ROOM_NAME


async def input_duration(update: Update, context: ContextTypes.user_data):
    buttons = [
        [
            InlineKeyboardButton(text='5 min', callback_data=str('5')),
            InlineKeyboardButton(text='10 min', callback_data=str('10')),
            InlineKeyboardButton(text='15 min', callback_data=str('15'))
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(text=message_texts.CHOOSE_TIME, reply_markup=keyboard)

    return START_GAME


async def start_game(update: Update, context: ContextTypes.user_data):
    user_data = context.user_data
    user_data[DURATION] = update.callback_query.data

    await update.callback_query.answer()
    await update.callback_query.message.edit_text(
        message_texts.ROOM_INFORMATION.format(user_data[ROOM_NAME], user_data[DURATION])
    )

    return START_GAME


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)

    conv_handler_create_room = ConversationHandler(
        entry_points=[CommandHandler('createroom', createroom)],
        states={
            TYPING_ROOM_NAME: [
                MessageHandler(filters.TEXT, save_room_name)
            ],
            ROOM_ALREADY_EXISTS: [
                CallbackQueryHandler(room_already_exists, pattern=str(ROOM_ALREADY_EXISTS))
            ],
            INPUT_DURATION: [
                CallbackQueryHandler(input_duration, pattern=str(INPUT_DURATION))
            ],
            START_GAME: [
                CallbackQueryHandler(start_game, pattern=str(START_GAME))
            ]
        },
        fallbacks=[CommandHandler("start", start)]
    )

    application.add_handler(conv_handler_create_room)

    application.run_polling()
