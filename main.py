from teletoken import TOKEN
import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import Updater, MessageHandler, Filters
from dataclasses import dataclass
from pprint import pprint
from PIL import Image

from replies import reply_machinen


logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

USERS = {}


@dataclass
class UserRequest:
    id: str
    chat_id: str
    mail: str
    photo: list
    location: str

@dataclass
class UserInfo:
    id: int
    state: str
    mail: str
    lang: str


def get_user_info(update):
    user_id = update.message.from_user.id

    if user_id not in USERS:
        user = UserInfo(id=user_id, state="START", mail="", lang="RU")
        USERS[user_id] = user

    return user_id


def generate_keyboard(buttons_list):
    reply_markup = ReplyKeyboardMarkup(
        buttons_list,
        resize_keyboard=True,
        one_time_keyboard=True,)
    if buttons_list == [[]]:
        reply_markup = ReplyKeyboardRemove()
    return reply_markup


def request_geo(txt, btns, update, context):
    keyboard = [[KeyboardButton(btns, request_location=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=txt,
        reply_markup=reply_markup)


def send_message(message, buttons, update, context):
    keyboard = generate_keyboard(buttons)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=keyboard)


def user_lang(user, message):
    if message in ["EN", "HY", "RU"]:
        user.lang = message


def handle_message(update, context):
    message = update.message


    user_id = get_user_info(update)
    user = USERS[user_id]

    print(user.state)

    if message.text in ["EN", "HY", "RU"]:
        user.lang = message.text
    else:
        reply = reply_machinen(user.state, message, user.lang)
        user.state = reply[2]
        commands = reply[3:]
        txt = reply[0]
        buttons = reply[1]

        send_message(txt, buttons, update, context)
        for command in commands:
            eval(command)

    print(user.state, "\n")
def bot():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.all, handle_message))
    updater.start_polling()

if __name__ == "__main__":
    bot()
