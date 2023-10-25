"""Тут у нас конечный автомат для робота."""
from dataclasses import dataclass


# пустой набор кнопков
EMPTY_BTNS = [[]]
RU_DECLINE_BTN = ['Я передумал']


# словарь исходящих сообщений стейта START
RU_MSGS_START = {
    '/start': """
— Привет! Я бот команды YRVN.AM.
Сообщи мне о проблеме с точкой раздельного сбора, или о появлении новой!
Ты получишь всю информацию о статусе заявки (если хочешь :))
""",

    '/point_issue_get_geo': """
 — Вы хотели сдать мусор, а по адресу никто ничего не принимает? Давайте разбираться.
""",

    '/new_point': """
 — Вы нашли классное место? Мы с радостью добавим на карту:
• ремонт обуви
• ремонт и пошив одежды (ателье)
• ремонт разной бытовой техники (не сетевые магазины)
• приём цветных и черных металлов
• прием шин и покрышек
• приём стеклотары
• прием макулатуры

Если за приём проводится оплата — напишите об этом.
Ответным сообщением ждём адрес точки, сопроводительную информацию, и фотку.
Фотку необязательно, но хотелось бы.
""",

    '/write_us': """
 — Вот прям сюда и напишите ответным сообщением.
""",

    '/donate': """
 — Для того, чтобы дать нам денег, надо перейти на наш сайт. \n Не пугайтесь! Мы бережём персональные данные.
""",

    '/wrong_value': """
 — Не могу поддержать разговор на эту тему, увы. Выбери из предложенных кнопок!
""",
    }


RU_MSGS_POINT_ISSUE_GET_GEO = {
    '/point_issue_get_photo': """
 — Отлично! Теперь сделайте фотку точки, и пришлите её.
""",

'/wrong_value': """
 — Как будто бы это не координаты.
""",
    }


RU_BTNS_START = {
    'main': [['Проблема с точкой', 'Новая точка'], ['Написать нам', 'Донат'], ['EN', 'HY']],
    }


# STATE : {COMMAND (FSM SYMBOL) : [MSG, BTNS, NEW_STATE, FN]}
RU = {
    # юзер выбрал что-то со стартового экрана
    'START': {
        '/start': [
            RU_MSGS_START['/start'],
            RU_BTNS_START['main'],
            'START',
            ],

        '/point_issue_get_geo': [
            RU_MSGS_START['/point_issue_get_geo'],
            EMPTY_BTNS,
            'POINT_ISSUE_GET_GEO',
            'request_geo(" — Для начала, пришлите геолокацию точки.", ["Отправить гео", "Я передумал"],  update, context)',
            ],

        '/new_point': [
            RU_MSGS_START['/new_point'],
            RU_BTNS_START['main'],
            'NEW_POINT',
            ],

        '/write_us': [
            RU_MSGS_START['/write_us'],
            RU_BTNS_START['main'],
            'WRITE_US',
            ],

        '/donate': [
            RU_MSGS_START['/donate'],
            RU_BTNS_START['main'],
            'START',
            'request_donate(" — А там можно выбрать удобный способ задонатить.", "Перейти", "https://yrvn.am/ru/payment/",  update, context)',
            ],

        '/wrong_value': [
            RU_MSGS_START['/wrong_value'],
            RU_BTNS_START['main'],
            'START',
            ],
        },

    # юзер отправил координаты
    'POINT_ISSUE_GET_GEO': {
        '/point_issue_get_photo': [
            RU_MSGS_POINT_ISSUE_GET_GEO['/point_issue_get_photo'],
            [RU_DECLINE_BTN],
            'POINT_ISSUE_GET_PHOTO',
            ],

        '/wrong_value': [
            RU_MSGS_POINT_ISSUE_GET_GEO['/wrong_value'],
            EMPTY_BTNS,
            'POINT_ISSUE_GET_GEO',
            'request_geo(" — Пришлите геолокацию точки.", ["Отправить гео", "Я передумал"],  update, context)',
            ],
        },

    # юзер отправил фото кривой точки
    'POINT_ISSUE_GET_PHOTO': {
        '/choose_feedback': [
            ' — Осталась самая малость. Прислать ли вам результат обработки заявки?',
            [['Не надо'], ['На почту'], ['Сюда, в чат']],
            'CHOOSE_FEEDBACK',
            ],


        '/wrong_value': [
            ' — Как будто бы это не фотка. Сделайте фотку точки, и пришлите её.',
            [RU_DECLINE_BTN],
            'POINT_ISSUE_GET_PHOTO',
            ],
        },

    # юзер выбрал способ обратной связи
    'CHOOSE_FEEDBACK': {
        '/finally': [
            ' — Окс! Ещё заявочку?',
            RU_BTNS_START['main'],
            'START',
            ],

        '/finally_mail': [
            ' — Тогда пришлите почту.',
            EMPTY_BTNS,
            'GETTING_MAIL',
            ],

        '/wrong_value': [
            ' — Просто сделай выбор, умоляю.',
            [['Не надо'], ['На почту'], ['Сюда, в чат']],
            'CHOOSE_FEEDBACK',
            ],
        },

    # юзер отправил мейл
    'GETTING_MAIL': {
        '/finally_mail_error': [
            ' — Я точно знаю, это — не почта! Давайте попробуем ещё раз.',
            EMPTY_BTNS,
            'GETTING_MAIL',
            ],

        '/finally': [
            ' — Окс! Ещё заявочку?',
            RU_BTNS_START['main'],
            'START',
            ],
        },

    # юзер отменил операцию
    'BACK_TO_THE_ROOTS': {
        '/back_to_the_roots': [
            ' — Хорошо, я сбросил все изменения. Но всегда можно начать с чистого листа!',
            RU_BTNS_START['main'],
            'START',
            ],
        },

    # юзер отправил новую точку
    'NEW_POINT': {
        '/new_point_info': [
            ' - Отлично! Что-то добавим, или отправим?',
            [['Отправить!'], RU_DECLINE_BTN],
            'NEW_POINT',
            ],

        '/confirm': [
            ' — Принято!',
            RU_BTNS_START['main'],
            'START',
            ],
        },

    # юзер написал нам
    'WRITE_US': {
        '/write_us_add': [
            ' - Отлично! Что-то добавим, или отправим?',
            [['Отправить!'], RU_DECLINE_BTN],
            'WRITE_US',
            ],

        '/confirm': [
            ' — Принято!',
            RU_BTNS_START['main'],
            'START',
            ],
        },
    }

EN = {}
HY = {}

BUTTONS_TRANSLATOR = (
    ('/start', '/start'),
    ('/point_issue_get_geo', 'Проблема с точкой'),
    ('/finally', 'Не надо'),
    ('/finally_mail', 'На почту'),
    ('/finally', 'Сюда, в чат'),
    ('/back_to_the_roots', 'Я передумал'),
    ('/new_point', 'Новая точка'),
    ('/donate', 'Донат'),
    ('/write_us', 'Написать нам'),
    ('/confirm', 'Отправить!'),
    )


def is_email(text):
    """
    Тупая проверка на мейл.

    Надо бы сделать не тупой.

    Args:
        text (str): e-mail

    Returns:
        symbol for FSM
    """
    if '@' in text:
        return '/finally'
    return '/finally_mail_error'


def reply_machinen(state, message, lang):
    """
    Функция-переводчик.

    Дело в том, что когда юзер присылает что-то непонятное,
    нужно как-то это обработать. Пользовательский текст
    воспринимаем как символ алфавита для КА,
    дешифруем об BUTTONS_TRANSLATOR

    Args:
        state (str): текущее состояние юзера
        message (obj): сообщение от юзера
        land (str): на каком языке мы общаемся

    Returns:
        [MSG, BTNS, NEW_STATE, FN]
    """
    replies = {'EN': EN, 'RU': RU, 'HY': HY}

    symbol = message.text
    location = message.location
    photos = message.photo

    symbol_matched = False  # Переменная для отслеживания совпадения текста
    for buttons in BUTTONS_TRANSLATOR:
        if symbol in buttons:
            symbol = buttons[0]
            symbol_matched = True
            break
    # Проверка наличия геолокации и фотографий только если текст не совпал
    if not symbol_matched:
        if location is not None and state == 'POINT_ISSUE_GET_GEO':
            symbol = '/point_issue_get_photo'
        elif photos and state == 'POINT_ISSUE_GET_PHOTO':
            symbol = '/choose_feedback'
        elif state == 'GETTING_MAIL':
            symbol = is_email(symbol)
        elif state == 'WRITE_US':
            symbol = '/write_us_add'
        elif state == 'NEW_POINT':
            symbol = '/new_point_info'
        else:
            symbol = '/wrong_value'

    if symbol == '/back_to_the_roots':
        state = 'BACK_TO_THE_ROOTS'

    print(symbol)
    print(state)
    return replies[lang][state][symbol]
