''' туть мы храним кнопки и ответы пользователю '''

RU = {
    "START": {
        "/start": [" — Привет! Я бот команды YRVN.AM.\nСообщи мне о проблеме с точкой раздельного сбора, или о появлении новой!\nТы получишь всю информацию о статусе заявки (если хочешь :))",
        [["Проблема с точкой"],["EN", "HY"]],
        "START"],

        "/point_issue_get_geo": [" — Вы хотели сдать мусор, а по адресу никто ничего не принимает? Давайте разбираться.",
        [[]],
        "POINT_ISSUE_GET_GEO",
        "request_geo(' — Для начала, пришлите геолокацию точки', 'Отправить гео',  update, context)"]},

    "POINT_ISSUE_GET_GEO": {
        "/point_issue_get_photo": [" — Отлично! Теперь сделайте фотку точки, и пришлите её.",
        [[]],
        "POINT_ISSUE_GET_PHOTO"]},

    "POINT_ISSUE_GET_PHOTO": {
        "/choose_feedback": [" — Осталась самая малость. Прислать ли вам результат обработки заявки?",
        [["Не надо"], ["На почту"], ["Сюда, в чат"]],
        "CHOOSE_FEEDBACK"]},

    "CHOOSE_FEEDBACK": {
        "/finally": [
        " — Окс! Ещё заявочку?",
        [["Проблема с точкой"],["EN", "HY"]],
        "START"],

        "/finally_mail": [
        " — Тогда пришлите почту.",
        [[]],
        "CHOOSE_FEEDBACK"]},

    }

EN = {}
HY = {}

BUTTONS_TRANSLATOR = (
    ("/start", "/start"),
    ("/point_issue_get_geo", "Проблема с точкой"),
    ("/finally", "Не надо"),
    ("/finally_mail", "На почту"),
    )

def reply_machinen(state, message, lang):
    replies = {"EN": EN, "RU": RU, "HY": HY}

    text = message.text
    location = message.location
    photos = message.photo

    for buttons in BUTTONS_TRANSLATOR:
        if text in buttons:
            text = buttons[0]
        elif location is not None:
            text = "/point_issue_get_photo"
        elif photos != []:
            text = "/choose_feedback"
        elif "@" in text:
            text = "/finally"

    print(text)
    return replies[lang][state][text]
