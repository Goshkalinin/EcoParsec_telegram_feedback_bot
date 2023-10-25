"""Просто напиши python3 main.py."""

import logging
from dataclasses import dataclass

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Filters, MessageHandler, Updater

from replies import reply_machinen
from teletoken import TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    )

# кажется, это надо заменить на cvs, например
USERS = {}


@dataclass
class UserInfo(object):
    """
    Собираем информацию о пользователе.

    Делаем это на каждое входящее сообщение.
    """

    id: int
    state: str
    mail: str
    lang: str

    message: list


def get_user_info(update):
    """
    Проверяем, приходил ли уже пользователь.

    Если не приходил — создаём нового, и записываем.

    Args:
        update (???): што эта

    Returns:
        user_id (int): literally tg user id
    """
    user_id = update.message.from_user.id

    if user_id not in USERS:
        user = UserInfo(
            id=user_id,
            state='START',
            mail='',
            lang='RU',

            message=[],
            )

        USERS[user_id] = user

    return user_id


def generate_keyboard(buttons_list):
    """
    Генерируем кнопки для пользователя.

    Если список пустой — удаляем текущую клавиатуру.

    Args:
        buttons_list (list of lists): список кнопков.

    Returns:
        reply_markup — разметка кнопок для сообщения.
    """
    reply_markup = ReplyKeyboardMarkup(
        buttons_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        )
    if buttons_list == [[]]:
        reply_markup = ReplyKeyboardRemove()
    return reply_markup


def request_donate(txt, button, url, update, context):
    """
    Выкатываем пользователю кнопку со ссылкой на донатошную.

    Args:
        txt (str): потому что разные языки
        button (str): имя кнопки
        url (str): финальный урл донатошной
        update (obj): чо пришло, от кого пришло, тип сообщения, тп.
        context (obj): объект c методами для чата.
    """
    keyboard_buttons = [
        [InlineKeyboardButton(button, url=url)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard_buttons)

    update.message.reply_text(txt, reply_markup=reply_markup)


def request_geo(txt, btns, update, context):
    """
    Запрашиваем геолокацию чувака.

    Args:
        txt (str): потому что разные языки
        btns (str): список кнопок
        update (obj): чо пришло, от кого пришло, тип сообщения, тп.
        context (obj): объект c методами для чата.
    """
    request_geo = btns[0]
    abort = btns[1]
    keyboard = [[KeyboardButton(request_geo, request_location=True)], [abort]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=txt,
        reply_markup=reply_markup,
        )


def send_message(message, buttons, update, context):
    """
    Генерируем клаву, отправляем сообщеньку.

    Args:
        message (str): тушка сообщения
        buttons (list of lists): список кнопков
        update (obj): чо пришло, от кого пришло, тип сообщения, тп.
        context (obj): объект c методами для чата.
    """
    keyboard = generate_keyboard(buttons)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
        reply_markup=keyboard,
        )


def new_request(user, message):
    user.message.append(message)
    print(user)


def handle_message(update, context):
    """
    Хендлер сообщений.

    Args:
        update (obj): чо пришло, от кого пришло, тип сообщения, тп.
        context (obj): объект c методами для чата.
    """
    message = update.message

    user_id = get_user_info(update)
    user = USERS[user_id]

    print(user.state)

    # Эту шляпу надо переписать в стейт-машину!
    if message.text in {'EN', 'HY', 'RU'}:
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

    print(user.state, '\n')


def bot():
    """Запуск и настройка бота."""
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.all, handle_message))
    updater.start_polling()


if __name__ == '__main__':
    bot()
