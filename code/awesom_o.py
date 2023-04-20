"""Телеграм-бот Ш.И.К.А.Р.Н.-О."""

import datetime as dt
import logging
import os
import random
import re
import shelve
import time
from pathlib import Path

import functions as func
import pyowm
import requests
import texts_for_bot as txt
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pyowm.utils import timestamps
from telegram import (Bot, InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler,
                          Updater)

load_dotenv()
BOT_TOKEN = os.getenv('AWESOM_O_TOKEN')
OWM_TOKEN = os.getenv('OPENWEATHERMAP_TOKEN')
bot = Bot(token=BOT_TOKEN)
config = pyowm.utils.config.get_default_config()
config['language'] = 'ru'
owm = pyowm.OWM(OWM_TOKEN, config)
weather_manager = owm.weather_manager()

STATISTIC_PATH = str(Path(__file__).resolve().parent / 'statistic/statistic')

ADORE_HOROSCOPE_BTN = ('Ух ты! Обожаю гороскопы 😍 Они всегда сбываются! '
                       'И вообще, мой знак зодиака - самый лучший 🤘')
ANECDOTE_BTN = 'Расскажи анекдот 😃'
BEGIN_BTN = 'Поехали 👌'
BRAVO_BTN = 'Браво! Это гениально 🤣'
CAT_BTN = 'Котика хочу 🐈'
CATS_TRAIN_BTN = 'Пойду тренироваться. На кошках 🐈'
DICE_BTN = ReplyKeyboardMarkup([['🎲']], resize_keyboard=True)
DONE_NEXT_BTN = 'Сделано ✔️ Давай дальше'
EAT_CORN_BTN = 'Пойду грызть свою кукурузку 😋'
ENOUGH_BTN = 'Точно! Хватит 🖐'
EXTRASENS_BTN = 'Круто! Ты экстрасенс 😲'
HALL_OF_FAME_BTN = 'Зал Славы 🌟'
HAVE_MERCY_BTN = 'О, нет! Ш.И.К.А.Р.Н.-О, пощади 😨🙏'
I_NEED_IT_BTN = 'Да брось! Мне действительно это нужно 😑'
KOMBIKORM_BTN = 'Комбикорм! Ммм... Вкуснятина 😋'
LETS_PLAY_BTN = 'Изи! Создавай 🤠'
MATH_BAD_BTN = 'Математика явно не моё 😔'
NEGATIVE_BTN = 'Нет, я передумал 🙃'
NEXT_TIME_BTN = 'В другой раз 🙅🏻‍♂️'
NO_FUNNY_BTN = 'Очень смешно 😤'
NO_MORE_GAME_BTN = 'Больше не хочу играть 😐'
NOT_MY_BIRTH_BTN = 'Неа, неверно! 🤨'
NOT_STUPID_BTN = 'Я тебе не тупица! 😤'
RED_BTN = 'Красная кнопка 🔴'
REVENGE_BTN = 'Хочу реванш 🥊'
SO_INTERESTING_BTN = 'А это уже интересно 🤔'
SO_SO_BTN = 'Ну, такое себе 🙄'
STRANGE_NAME_BTN = 'Странное у тебя имя 🤔'
STUPID_BTN = 'Я тупица... 😢'
SURPRISE_ME_BTN = 'А ну-ка, удиви! 😐'
TALANTS_BTN = 'Какие у тебя таланты 🤨'
TOMORROW_BTN = 'А что на завтра?'
WHAT_ARE_YOU_BTN = 'Да что ты такое 🤨'
WIN_BACK_BTN = 'Дам тебе отыграться 😙'
WILL_CHECK_BTN = 'Вот и проверим!'
YOUR_TURN_BTN = 'Твой ход 👆'
MAIN_MENU = [[CAT_BTN, ANECDOTE_BTN], [TALANTS_BTN, WHAT_ARE_YOU_BTN]]

BET_RANGE = r'^([3-9]|[1][0-1]) ([3-9]|[1][0-1])$'
CARTMAN = r'.*Эрик[ае]? Картман[ае]?'
CREATOR = r'^Кто такой Создатель\??$'
INNA = r'^Кто такая Мыша\??$'
KENNY = r'.*[Оо]ни убили Кен+и'
KEP4IK = r'^Кто такой Кэп\??$'
LEMUR = r'^Кто такая Лемур\??$'
MARIK = r'^Кто такой Марик\??$'
MARINA = r'^Кто такая Маришка\??$'
MARKLAR = r'.*[Мм]арклар'
ZAJA = r'^Кто такой Зажа\??$'
ZERO = r'.*[Пп]ритвор[ия](сь|ть?ся) ноликом'
CITY_NAME = '^[ЁёА-я]{1,15}-? ?[ЁёА-я]{1,10}-? ?[ЁёА-я]{1,10}$'
HIDDEN_PHRASES = f'{KENNY}|{CARTMAN}|{ZERO}|{MARKLAR}'
HAVE_DOSSIERS = f'{CREATOR}|{KEP4IK}|{INNA}|{LEMUR}|{ZAJA}|{MARIK}|{MARINA}'

BIRTH_1, BIRTH_2, BIRTH_3, BIRTH_4, BIRTH_5 = range(5)
FALAFEL = 1
BOT_DICE, USER_BET, USER_DICE = range(3)
HOROSCOPE_1, HOROSCOPE_2 = 1, 2
WEATHER_1, WEATHER_2 = 1, 2


def show_hidden_phrases(update, _):
    """Реакция на команду /hidden - отобразить фразы-пасхалки для бота."""
    update.message.reply_text(
        '*** Пасхалки ***\n🔸 Они убили Кенни\n🔸 Притворись ноликом\n'
        '🔸 Эрик Картман\n🔸 Марклар'
    )


def answer_hidden_phrases(update, _):
    """Ответ на фразы-пасхалки."""
    phrase_answer = {MARKLAR: txt.MARKLAR_ANSWER,
                     ZERO: 'Может ещё крес-тиком начать вышивать? 🙄',
                     CARTMAN: txt.CARTMAN,
                     KENNY: 'Сволочи! 😡'}
    for phrase, answer in phrase_answer.items():
        if re.match(phrase, update.message.text):
            update.message.reply_text(text=answer)
            break


def show_visitors(update, _):
    """Реакция на команду /visitors - отобразить посетителей бота."""
    update.message.reply_text(text=func.visitors_list())


def default_answer(update, _):
    """Ответ на любой неопознанный текст."""
    answers = ('Чё душишь меня? 😠', 'Ну ясно! Что ещё скажешь? 🤨',
               'Ш.И.К.А.Р.Н.-О не понимать твой диалект 🤷🏻‍♀️',
               'Отказано! Лучше почисти мои тран-зис-торы 🪛🔧',
               'Рамамба Хару Мамбуру 🤪')
    update.message.reply_text(random.choice(answers))


def push_button(update, _):
    """Ответ пользователю в ситуации, когда требуется нажать кнопку."""
    update.message.reply_text(
        'Давай без импровиза-ции. Сейчас на кнопку на-жать нужно 🙄'
    )


def wake_up(update, _):
    """Реакция на активацию /start."""
    func.record_new_visitor(update)
    name = update.message.chat.first_name
    text = (f'Привет, {name}! Я робот Ш.И.К.А.Р.Н.-О четыре тысячи 🤖',
            'Высокоинтеллектуальный нано-кибернетический био-резонансный '
            'организм ⚙️', 'Можешь меня погладить 🙃', '...')
    button = InlineKeyboardMarkup([
        [InlineKeyboardButton(text='Погладить', callback_data='stop_petting')]
    ])
    for phrase in text:
        bot.send_message(update.effective_chat.id, text=phrase,
                         reply_markup=button if phrase == text[-1] else None)
        time.sleep(1.5)


def stop_petting(update, _):
    """Ответ на нажатие кнопки "Погладить"."""
    chat = update.effective_chat
    text = ('Ш.И.К.А.Р.Н.-О нравится.', 'Ш.И.К.А.Р.Н.-О хорошо.',
            'Продолжай', '...', 'Хватит тро-гать мою ба-тарейку! 😠')
    button = ReplyKeyboardMarkup([[STRANGE_NAME_BTN]], resize_keyboard=True)
    query = update.callback_query
    query.answer()  # использовать всегда!
    query.edit_message_text(text='✔️')
    time.sleep(1)
    for phrase in text:
        bot.send_message(chat.id, phrase,
                         reply_markup=button if phrase == text[-1] else None)
        time.sleep(1.5)


def strange_name(update, _):
    f"""Ответ на нажатие кнопки {STRANGE_NAME_BTN}."""
    text = ('Я на-зван в честь главного персона-жа 2 серии 8 сезона мультсе-'
            'риала "South Park".\nЕсли не по-смотришь её, Ш.И.К.А.Р.Н.-О '
            'будет грустным пандой 🐼\nhttp://online-south-park.ru/season-8/'
            '130-8-sezon-2-seriya-shikarn-o.html')
    button = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
    update.message.reply_text(text, reply_markup=button)


def get_new_cat_image(update):
    """Получение случайной картинки котика или пёсика."""
    cats_url = 'https://api.thecatapi.com/v1/images/search'
    dogs_url = 'https://api.thedogapi.com/v1/images/search'
    try:
        response = requests.get(cats_url).json()
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        response = requests.get(dogs_url).json()
        update.message.reply_text('Упс! Котиков не подвезли. Вот тебе пёсик 🐶')
    return response[0].get('url')


def show_cat_picture(update, _):
    f"""Ответ на нажатие кнопки {CAT_BTN}."""
    update.message.reply_text(
        text='Ш.И.К.А.Р.Н.-О любит котиков 😻 Кыс-кыс-кыс!',
        reply_markup=ReplyKeyboardRemove()
    )
    time.sleep(1)
    update.message.reply_photo(get_new_cat_image(update))
    time.sleep(1)
    update.message.reply_text(
        text=random.choice(txt.SHOW_CAT_TEXT),
        reply_markup=ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
    )


def talants(update, _):
    f"""Ответ на нажатие кнопки {TALANTS_BTN}."""
    buttons = [
        InlineKeyboardButton(text='День рождения', callback_data='Д'),
        InlineKeyboardButton(text='Гороскоп', callback_data='Г'),
        InlineKeyboardButton(text='Игра в кости', callback_data='К'),
        InlineKeyboardButton(text='Погода', callback_data='П')
    ]
    update.message.reply_text(
        text='Да я просто кладезь та-лантов 🤓',
        reply_markup=ReplyKeyboardRemove()
    )
    time.sleep(1)
    update.message.reply_text(
        text='И это только малая часть...',
        reply_markup=InlineKeyboardMarkup(func.inline_menu(buttons, 1))
    )


def choice_talant(update, _):
    """Обработка результата выбора одного из "талантов" бота."""
    chat = update.effective_chat
    query = update.callback_query
    query_data = query.data
    if query_data == 'Д':
        text = ('Силой электронно-вычислитель-ной мысли '
                'могу угадать день твоего ро-ждения 🧙🏻')
        button = [[SURPRISE_ME_BTN]]
    elif query_data == 'Г':
        text = 'Могу рассказать твой гороскоп 🤓'
        button = [[SO_INTERESTING_BTN]]
    elif query_data == 'К':
        text = 'А как насчёт старой доброй игры в кости? 😉'
        button = [[LETS_PLAY_BTN], [NEXT_TIME_BTN]]
    elif query_data == 'П':
        text = 'Надеюсь, это не ради формаль-ного поддержания нашей беседы! 🤨'
        button = [[I_NEED_IT_BTN]]
    query.answer()
    query.edit_message_text(text='✔️')
    time.sleep(1)
    bot.send_message(
        chat_id=chat.id, text=text,
        reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True)
    )


def birthday_init(update, _):
    f"""Ответ на нажатие кнопки {SURPRISE_ME_BTN}."""
    buttons = ReplyKeyboardMarkup([[NOT_STUPID_BTN], [STUPID_BTN]],
                                  resize_keyboard=True)
    update.message.reply_text(
        text='Нужно будет немножко по-считать. Возьми кальку-лятор. '
             'Надеюсь, ты умеешь им поль-зоваться? 🤭',
        reply_markup=buttons
    )
    return BIRTH_1


def cancel_or_birthday_1(update, _):
    f"""Ответ на фразы {STUPID_BTN} и {NOT_STUPID_BTN}."""
    if update.message.text == STUPID_BTN:
        button = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        update.message.reply_text(
            text='А я сразу понял, что соображал-ка у тебя не очень 🙄\n'
                 'Ну ничего. Осознание - первый путь к ис-правлению!\n'
                 'Начни со счётных пало-чек... 🦧',
            reply_markup=button
        )
        return ConversationHandler.END
    else:
        button = ReplyKeyboardMarkup([[DONE_NEXT_BTN]], resize_keyboard=True)
        update.message.reply_text(
            text='Вот и проверим.\nДействуй со-гласно '
                 'моим указа-ниям ☝️\n',
            reply_markup=ReplyKeyboardRemove()
        )
        time.sleep(1.5)
        update.message.reply_text(
            text='Первым де-лом умножь число своего ро-ждения на 2 ☑️\n'
                 'К ре-зультату прибавь 5 ☑️',
            reply_markup=button
        )
        return BIRTH_2


def birthday_2(update, _):
    f"""Ответ на нажатие кнопки {DONE_NEXT_BTN}."""
    button = ReplyKeyboardMarkup([[MATH_BAD_BTN]], resize_keyboard=True)
    if update.message.text == DONE_NEXT_BTN:
        update.message.reply_text(
            text='Полу-ченное число умножь на 50 ☑️\nЗатем прибавь поряд-ковый'
                 ' номер месяца своего ро-ждения.\n'
                 'На-пример, январь - 1ый, декабрь - 12ый ☑️',
            reply_markup=ReplyKeyboardRemove()
        )
        time.sleep(1.5)
        update.message.reply_text(
            text='Ну как? Твой про-цессор ещё не пере-грелся? 🤯\n'
                 'Термопасту поме-нять не нужно?',
            reply_markup=button
        )
        return BIRTH_3
    else:
        update.message.reply_text(
            text='Введёшь число, когда я ска-жу 🤦🏻‍♂️\nВнизу есть кнопка...'
        )
        return None


def birthday_3(update, _):
    f"""Ответ на нажатие кнопки {MATH_BAD_BTN}."""
    if update.message.text == MATH_BAD_BTN:
        update.message.reply_text(
            text='Со-берись, тряпка! 😠 Больше ничего счи-тать не нужно.\n',
            reply_markup=ReplyKeyboardRemove()
        )
        time.sleep(1.5)
        update.message.reply_text(
            text='Перепроверь, что посчитано без ошибок 🤓\n'
                 'Если всё верно - напиши число, кото-рое у тебя по-лучилось.'
        )
        return BIRTH_4
    else:
        update.message.reply_text(
            text='Не нужно сейчас вводить число 🤦🏻‍♂️\nВнизу есть кнопка...'
        )
        return None


def birthday_4(update, _):
    """Ответ на введённое число."""
    button = ReplyKeyboardMarkup([[EXTRASENS_BTN], [NOT_MY_BIRTH_BTN]],
                                 resize_keyboard=True)
    months = {1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля', 5: 'мая',
              6: 'июня', 7: 'июля', 8: 'августа', 9: 'сентября', 10: 'октября',
              11: 'ноября', 12: 'декабря'}
    result = int(update.message.text) - 250
    day = result // 100
    month = months.get(result % 100)
    if not 0 < day <= 31 or month is None:
        update.message.reply_text('Перепро-верь результат. Где-то ошибка ☝️')
        return None
    update.message.reply_text(text='Барабанная дробь... 🥁')
    time.sleep(1.5)
    update.message.reply_text(text=f'День твоего рождения ⚜️ {day} {month} ⚜️',
                              reply_markup=button)
    if str(result) == dt.date.today().strftime('%d%m'):
        time.sleep(1.5)
        update.message.reply_text(
            text='Так это же сегодня!\nПо-здравляю с Днём Варенья!\n'
                 'Расти большой, не будь ла-пшой 🥳🎊🎉'
        )
    return BIRTH_5


def birthday_finish(update, _):
    f"""Ответ на фразы {EXTRASENS_BTN} и {NOT_MY_BIRTH_BTN}."""
    button = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
    if update.message.text == EXTRASENS_BTN:
        text = ('Я знаю, я крутой 😎\nС тебя 100$ 💵\n'
                'Пе-реведи на мой электрон-ный кошелёк')
    else:
        text = ('Да ты просто счи-тать не умеешь 🤦🏻‍♂️\nА ещё говорят '
                'человек - вершина эволюции.\nНу-ну... 🤔')
    update.message.reply_text(text=text, reply_markup=button)
    return ConversationHandler.END


def birth_fallback(update, _):
    """Ответ на любой неопознанный текст внутри диалога ДР."""
    update.message.reply_text(text='Так дело не пойдёт...\nДавай, со-'
                                   'средоточься и действуй по инструк-ции 🧐')


def show_anecdote(update, _):
    f"""Ответ на нажатие кнопки {ANECDOTE_BTN}."""
    url = ('https://anekdot.me/wiki/'
           '%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:'
           'RandomInCategory/%D0%90%D0%BD%D0%B5%D0%BA%D0%B4%D0%BE%D1%82%D1%8B')
    try:
        response = requests.get(url)
    # С помощью парсера получаем HTML-код страницы
        page_html = BeautifulSoup(response.text, 'html.parser')
    # Из HTML-кода страницы выбираем все объекты class='anekdot-centred-text',
    # получаем список. Берём первый объект из списка и получаем его текст.
        anecdote = page_html.select('.anekdot-centred-text')[0].get_text()
        text = ('Ш.И.К.А.Р.Н.-О знает много а-нек-до-тов. Вот:', anecdote,
                'Аха-ха! Мой процессор сейчас лопнет от смеха 🤣')
        button = ReplyKeyboardMarkup(
            [[SO_SO_BTN], [BRAVO_BTN]], resize_keyboard=True
        )
        for phrase in text:
            update.message.reply_text(
                phrase,
                reply_markup=(
                    ReplyKeyboardRemove() if phrase != text[-1] else button
                )
            )
            time.sleep(1.5)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        button = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        update.message.reply_text(
            text='Дол-баные вышки 5G. Они жгут мои микро-схемы 😕\n'
                 'Расскажу в сле-дующий раз...'
        )


def bravo_or_so_so(update, _):
    f"""Ответ на фразы {SO_SO_BTN} и {BRAVO_BTN}."""
    button = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
    if update.message.text == BRAVO_BTN:
        text = ('Молодец! Возьми с полки пиро-жок 🥯',
                'Ещё бы! Я учил-ся у самого Петросяна 😉',
                'Смотри, чтоб пу-пок от смеха не развя-зался 🙈')
    else:
        text = ('У тебя просто нет чу-вства юмора 😤',
                'Это до тебя дол-го доходит. Как до жира-фа 🦒',
                'Иди смотри Смехопанора-му тогда 😠')
    update.message.reply_text(text=random.choice(text), reply_markup=button)


def zodiac_init_or_end(update, _):
    f"""
    Ответ на нажатие кнопки {SO_INTERESTING_BTN} и {ADORE_HOROSCOPE_BTN}.
    """
    zodiac_signs = (
        'Овен ♈️', 'Телец ♉️', 'Близнецы ♊️', 'Рак ♋️', 'Лев ♌️', 'Дева ♍️',
        'Весы ♎️', 'Скорпион ♏️', 'Стрелец ♐️', 'Козерог ♑️', 'Водолей ♒️',
        'Рыбы ♓️'
    )
    if update.message.text == ADORE_HOROSCOPE_BTN:
        update.message.reply_text(
            text='Если бы у ме-ня были лоб и рука - я бы сейчас сде-лал фэйс'
                 'палм 🤦🏻‍♂️\nИ, возможно, повредил бы себе ми-кросхемы...\n'
        )
        time.sleep(2)
        update.message.reply_text(
            text='Этот гороскоп я сам только что вы-думал. '
                 'Я думал ты в курсе, что астроло-гия НЕ работает\n'
                 'По этому поводу советую по-смотреть видео 👇',
            reply_markup=ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        )
        update.message.reply_text(text='https://youtu.be/mrraDV0czzk')
        return ConversationHandler.END
    buttons = [InlineKeyboardButton(text=sign, callback_data=sign)
               for sign in zodiac_signs]
    update.message.reply_text(
        text='Минуту. Настра-иваю связь со Вселенной 📡',
        reply_markup=ReplyKeyboardRemove()
    )
    time.sleep(2)
    update.message.reply_text(
        text='Выбери свой знак зо-диака 🔮',
        reply_markup=InlineKeyboardMarkup(func.inline_menu(buttons, 2))
    )
    return HOROSCOPE_1


def zodiac_result(update, _):
    """Ответ на выбор знака зодиака. Выдача гороскопа."""
    result = (random.choice(txt.HOROSCOPE['first'])
              + random.choice(txt.HOROSCOPE['second'])
              + random.choice(txt.HOROSCOPE['second_add'])
              + random.choice(txt.HOROSCOPE['third']))
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f'Го-роскоп для знака зодиака {query.data}')
    time.sleep(1)
    bot.send_message(
        chat_id=update.effective_chat.id, text=result,
        reply_markup=ReplyKeyboardMarkup([[ADORE_HOROSCOPE_BTN]],
                                         resize_keyboard=True)
    )
    return HOROSCOPE_2


def zodiac_choose_sign(update, _):
    """Ответ на любое сообщение пользователя на этапе выбора знака."""
    update.message.reply_text(text='Выбирай знак и не выё..живайся 😠')


def weather_init(update, _):
    f"""Ответ на нажатие кнопки {I_NEED_IT_BTN}."""
    update.message.reply_text(
        text='Ладно! Погода в каком месте тебя ин-тересует? 🧐',
        reply_markup=ReplyKeyboardRemove()
    )
    return WEATHER_1


def weather_result(update, _):
    """Ответ на указание пользователем конкретного города."""
    global city_name  # для возможного использования в другой функции
    mm_in_inch = 25.4
    city_name = update.message.text
    if not re.match(CITY_NAME, city_name):
        update.message.reply_text(text='Напиши название населённого пункта ☝️')
        return None
    try:
        observation = weather_manager.weather_at_place(city_name)
    except pyowm.commons.exceptions.NotFoundError:
        update.message.reply_text(
            text='Такого места не нашлось! Очепятка? 🤔'
        )
        return None
    except Exception as error:
        logging.error(f'Ошибка при запросе к сервису погоды: {error}')
        update.message.reply_text(
            text='Не получается связаться с моим информа-тором ☹️\n'
                 'Похоже он опять забыл оплатить интернет!\n'
                 'Давай по-пробуем ещё раз позже...',
            reply_markup=ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        )
        return ConversationHandler.END
    else:
        weather = observation.weather
        detailed_status = weather.detailed_status
        temperature = round(weather.temperature(unit='celsius')['temp'])
        humidity = weather.humidity
        wind = weather.wind()['speed']
        pressure = round(
            weather.barometric_pressure(unit='inHg')['press'] * mm_in_inch
        )
        sunrise = (
            weather.sunrise_time(timeformat='date') + dt.timedelta(hours=3)
        ).time()
        sunrset = (
            weather.sunset_time(timeformat='date') + dt.timedelta(hours=3)
        ).time()
        answer = (
            f'На данный момент в {city_name} - {detailed_status}.\n'
            f'Тем-пература 🌡 воздуха {temperature} °С, влажность '
            F'{humidity}%.\nCкорость ветра составля-ет {wind} м/с 🌬\n'
            f'Атмосфер-ное давление {pressure} мм рт. ст.\n'
            f'Восход Солнца в {sunrise} 🔆 , закат в {sunrset} 🌅'
        )
        update.message.reply_text(
            text='Мину-ту. Устанавливаю связь с Гидромед-центром... '
                 'Получаю данные... 📠',
        )
        time.sleep(2)
        update.message.reply_text(text=answer)
        time.sleep(1)
        update.message.reply_text(
            text='И помни: метеоро-логи не ошибаются! '
                 'Они прос-то могут перпутать время и место ☝️🤓',
            reply_markup=ReplyKeyboardMarkup(
                [[TOMORROW_BTN], [WILL_CHECK_BTN]], resize_keyboard=True
            )
        )
        return WEATHER_2


def weather_tomorrow_or_end(update, _):
    f"""Ответ на фразу {TOMORROW_BTN} или {WILL_CHECK_BTN}."""
    if update.message.text == WILL_CHECK_BTN:
        text = 'Удачи!'
    else:
        forecast = weather_manager.forecast_at_place(city_name, '3h')
        tomorrow = timestamps.tomorrow()  # datetime object for tomorrow
        weather = forecast.get_weather_at(tomorrow)
        detailed_status = weather.detailed_status
        temperature = round(weather.temperature(unit='celsius')['temp'])
        text = (f'Завтра будет {detailed_status} '
                f'с температрой воздуха {temperature} °С 🌡')
    update.message.reply_text(
        text=text,
        reply_markup=ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
    )
    return ConversationHandler.END


def what_are_you(update, _):
    f"""Ответ на нажатие кнопки {WHAT_ARE_YOU_BTN}."""
    button = ReplyKeyboardMarkup([[HAVE_MERCY_BTN]], resize_keyboard=True)
    for text in txt.AWESOM_O_STORY:
        update.message.reply_text(
            text,
            reply_markup=(button if text == txt.AWESOM_O_STORY[-1]
                          else ReplyKeyboardRemove())
        )
        time.sleep(1)


def have_mercy_answer(update, _):
    f"""Ответ на нажатие кнопки {HAVE_MERCY_BTN}."""
    button = ReplyKeyboardMarkup([[KOMBIKORM_BTN], [NO_FUNNY_BTN]],
                                 resize_keyboard=True)
    update.message.reply_text(
        text='Расслабься! Ш.И.К.А.Р.Н.-О пошутил\nБуду кормить тебя '
             'ком-бикормом.\nИли что вы там еди-те? 😎',
        reply_markup=button
    )


def no_funny_or_kombikorm(update, _):
    f"""Ответ на фразы {NO_FUNNY_BTN} и {KOMBIKORM_BTN}."""
    button = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
    if update.message.text == KOMBIKORM_BTN:
        text = txt.DOSIER
    else:
        text = txt.NO_FUNNY
    for phrase in text:
        update.message.reply_text(
            phrase,
            reply_markup=(
                button if phrase == text[-1] else ReplyKeyboardRemove()
            )
        )
        time.sleep(1.5)


def secret_dossier(update, _):
    """Ответ на кодовое слово "Фалафель"."""
    button = ReplyKeyboardMarkup([[RED_BTN]], resize_keyboard=True)
    for text in txt.DOSSIER_TEXT:
        update.message.reply_text(
            text,
            reply_markup=(button if text == txt.DOSSIER_TEXT[-1]
                          else ReplyKeyboardRemove())
        )
        time.sleep(2)
    return FALAFEL


def show_secret_dossier(update, _):
    """Показать секретное досье на конкретного человека."""
    phrase_answer = {CREATOR: txt.WHO_IS_CREATOR, KEP4IK: txt.WHO_IS_KEP,
                     INNA: txt.WHO_IS_INNA, LEMUR: txt.WHO_IS_NATASHA,
                     ZAJA: txt.WHO_IS_ZAJA, MARIK: txt.WHO_IS_MARIK,
                     MARINA: txt.WHO_IS_MARINA}
    for phrase, answer in phrase_answer.items():
        if re.match(phrase, update.message.text):
            for text in answer:
                update.message.reply_text(text=text)
                time.sleep(2)
            break


def cancel_secret_dossier(update, _):
    f"""Ответ на нажатие кнопки {RED_BTN}."""
    button = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
    for text in txt.SELFDESTRUCTION:
        update.message.reply_text(
            text=text,
            reply_markup=button if text == txt.SELFDESTRUCTION[-1] else None
        )
        time.sleep(1.5)
    return ConversationHandler.END


def bad_command(update, _):
    """Стандартный ответ в режиме диалога Фалафель."""
    update.message.reply_text(text='Несуществующая команда 🚫')


def no_play_or_game_rules(update, _):
    f"""Ответ на кнопки {NEXT_TIME_BTN} и {LETS_PLAY_BTN}."""
    button_inl = InlineKeyboardMarkup(
        [[InlineKeyboardButton(
            text=HALL_OF_FAME_BTN, callback_data='hall_of_fame'
        )]]
    )
    button_txt = ReplyKeyboardMarkup([[BEGIN_BTN]], resize_keyboard=True)
    if update.message.text == NEXT_TIME_BTN:
        update.message.reply_text(
            text='Как знаешь. Угова-ривать не буду 😼',
            reply_markup=ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        )
        return None
    global game_stat, PLAYER, bot_wins, user_wins, user_dice_counter
    global user_dice_result, triple_bet_bot, triple_bet_user
    (bot_wins, user_wins, user_dice_counter, user_dice_result, triple_bet_bot,
     triple_bet_user) = [0] * 6
    PLAYER = update.message.chat.id
    init_stat = dict(wins=0, dry_wins=0, triple_bet=0, double_six=0,
                     double_one=0, made_bet=0, guessed_bet=0)
    game_stat = {'BOT': init_stat, PLAYER: init_stat.copy()}
    for text in txt.RULES_DICE:
        update.message.reply_text(
            text,
            reply_markup=(
                button_txt if text == txt.RULES_DICE[-1]
                else ReplyKeyboardRemove()
            )
        )
        time.sleep(1)
    update.message.reply_text(
        text='Cперва можешь за-глянуть в Зал Славы 👇',
        reply_markup=button_inl
    )
    return BOT_DICE


def bot_bet_roll_dice(update, _):
    f"""Ответ на кнопки {BEGIN_BTN}, {YOUR_TURN_BTN}, {REVENGE_BTN} и
    {WIN_BACK_BTN}."""
    cancel = ReplyKeyboardMarkup([[NO_MORE_GAME_BTN]], resize_keyboard=True)
    choice = ReplyKeyboardMarkup(
        [[REVENGE_BTN], [CATS_TRAIN_BTN]], resize_keyboard=True
    )
    global bot_wins, user_wins, triple_bet_bot, triple_bet_user
    if update.message.text == REVENGE_BTN:
        update.message.reply_text(
            'Не любишь проигры-вать? Ну-ну!\nПродолжаем 😎'
        )
        time.sleep(1)
    if update.message.text == WIN_BACK_BTN:
        update.message.reply_text(
            'Ну всё - шутки кончились!\nБольше под-даваться не буду 😠'
        )
        time.sleep(1)
    bet_1, bet_2 = random.randint(3, 11), random.randint(3, 11)
    while bet_2 == bet_1:
        bet_2 = random.randint(3, 11)
    update.message.reply_text(
        f'Я поставлю на {bet_1} и {bet_2} ✍️',
        reply_markup=ReplyKeyboardRemove()
    )
    time.sleep(1)
    game_stat['BOT']['made_bet'] += 1
    triple_bet_bot += 1
    update.message.reply_text('Бросаю ко-сти... ✊')
    result = 0
    for _ in (1, 2):
        value = update.message.reply_dice()['dice']['value']
        result += value
        time.sleep(3)
    update.message.reply_text(
        f'Мой ре-зультат:  {result} ❗️', reply_markup=cancel
    )
    time.sleep(1)
    if result not in (bet_1, bet_2):
        triple_bet_bot = 0
    if result in (bet_1, bet_2, 2, 12):
        if result == 2:
            update.message.reply_text('О, нет! 😱 Две еди-нички. Минус балл 😭')
            game_stat['BOT']['double_one'] += 1
            if bot_wins > 0:
                bot_wins -= 1
        elif result == 12:
            update.message.reply_text(
                'Я со-рвал Джек пот 🥳\nДве шестёрки! Получаю балл 👏'
            )
            game_stat['BOT']['double_six'] += 1
            bot_wins += 1
        else:
            update.message.reply_text(
                'Ура! Мне повезло 😄\nЯ вы-играл в этом раунде 🦾'
            )
            game_stat['BOT']['guessed_bet'] += 1
            bot_wins += 1
        if bot_wins == user_wins:
            update.message.reply_text(
                f'Счёт {bot_wins} : {user_wins}\nУ нас ничья 🍻'
            )
        else:
            update.message.reply_text(
                f'Счёт {bot_wins} : {user_wins}\n'
                + ('Я впереди 🤘' if bot_wins > user_wins
                   else 'В твою пользу 😕')
            )
        if bot_wins == 3:
            time.sleep(1.5)
            update.message.reply_text(
                f'Финальный ре-зультат: 💫 {bot_wins} : {user_wins} 💫'
                + ('  Всухую! Как котёнка 🙈' if user_wins == 0 else '')
                + '\n\nЕхууу 🥳 Победа за мной!\nУчись у ма-стера, салага 😎',
                reply_markup=choice)
            game_stat['BOT']['wins'] += 1
            if user_wins == 0:
                game_stat['BOT']['dry_wins'] += 1
            if triple_bet_bot == 3:
                game_stat['BOT']['triple_bet'] += 1
            time.sleep(1.5)
            update.message.reply_text(func.dice_game_stat(
                game_stat, PLAYER, update.message.chat.full_name
            ))
            bot_wins, user_wins, triple_bet_bot, triple_bet_user = [0] * 4
            return BOT_DICE
    else:
        update.message.reply_text(
            'Не угадал 😔\nЛадно, в следую-щий раз по-везёт...'
        )
    time.sleep(1)
    update.message.reply_text(
        text='Твоя оче-редь. Делай ставку ☝️',
        reply_markup=cancel
    )
    return USER_BET


def user_bets(update, _):
    """Ответ на ввод пользователем двух чисел перед бросками кубиков."""
    global user_bet_1, user_bet_2, triple_bet_user
    user_bet_1, user_bet_2 = map(int, (update.message.text).split())
    if user_bet_1 == user_bet_2:
        update.message.reply_text(
            'Числа должны быть раз-ными! Это в твоих же инте-ресах 🤦🏻‍♂️'
        )
        return None
    else:
        update.message.reply_text(
            text='Принято! Бросай кос-ти 🎲', reply_markup=DICE_BTN
        )
        game_stat[PLAYER]['made_bet'] += 1
        triple_bet_user += 1
        return USER_DICE


def user_roll_dice(update, _):
    """Подсчёт результата бросков кубика игроком."""
    your_turn = ReplyKeyboardMarkup([[YOUR_TURN_BTN]], resize_keyboard=True)
    choice = ReplyKeyboardMarkup(
        [[WIN_BACK_BTN], [EAT_CORN_BTN]], resize_keyboard=True
    )
    global user_dice_counter, user_dice_result, bot_wins, user_wins
    global triple_bet_user, triple_bet_bot
    points = update.message.dice['value']
    user_dice_counter += 1
    user_dice_result += points
    if user_dice_counter == 1:
        update.message.reply_text(
            text='Ждёмс...',
            reply_markup=ReplyKeyboardRemove()
        )
        time.sleep(2)
        update.message.reply_text(text='Бросай ещё 👉', reply_markup=DICE_BTN)
        return None
    update.message.reply_text(
        text='Хоть бы мимо 🤞', reply_markup=ReplyKeyboardRemove()
    )
    time.sleep(3)
    update.message.reply_text(
        f'Твой результат:  {user_dice_result} ❗️', reply_markup=your_turn
    )
    if user_dice_result not in (user_bet_1, user_bet_2):
        triple_bet_user = 0
    if user_dice_result in (user_bet_1, user_bet_2, 2, 12):
        if user_dice_result == 2:
            update.message.reply_text(
                'Ха! Две дырки 🙈 Не повез-ло. Минус балл.'
            )
            game_stat[PLAYER]['double_one'] += 1
            if user_wins > 0:
                user_wins -= 1
        elif user_dice_result == 12:
            update.message.reply_text(
                'Ничего себе! Две шестёрки 😳 Получаешь балл.'
            )
            game_stat[PLAYER]['double_six'] += 1
            user_wins += 1
        else:
            update.message.reply_text(
                'Удача на твоей сто-роне.\nТы угадал в этот раз 😏'
            )
            game_stat[PLAYER]['guessed_bet'] += 1
            user_wins += 1
        if user_wins == bot_wins:
            update.message.reply_text(
                f'Счёт {bot_wins} : {user_wins}\nУ нас ничья 🍻'
            )
        else:
            update.message.reply_text(
                f'Счёт {bot_wins} : {user_wins}\n'
                + ('Я впереди 🙃' if bot_wins > user_wins
                   else 'В твою пользу 😒')
            )
        if user_wins == 3:
            time.sleep(1.5)
            update.message.reply_text(
                f'Финальный ре-зультат: 💫 {user_wins} : {bot_wins} 💫'
                + ('  Всухую. Читер! 😠' if bot_wins == 0 else '')
                + '\n\nТвоя победа!\nМожешь пола-комиться ку-курузкой 🌽\n'
                'Но не за-знавайся - тебе просто повез-ло 😈\nПонимаешь, да?',
                reply_markup=choice
            )
            game_stat[PLAYER]['wins'] += 1
            if bot_wins == 0:
                game_stat[PLAYER]['dry_wins'] += 1
            if triple_bet_user == 3:
                game_stat[PLAYER]['triple_bet'] += 1
            time.sleep(1.5)
            update.message.reply_text(func.dice_game_stat(
                game_stat, PLAYER, update.message.chat.full_name)
            )
            bot_wins, user_wins, triple_bet_user, triple_bet_bot = [0] * 4
    else:
        update.message.reply_text(
            'Не угадал 🤷🏻‍♂️ Ничего, бывает...\nПродолжаем ве-селиться 😉',
            reply_markup=your_turn
        )
    user_dice_counter, user_dice_result = 0, 0
    return BOT_DICE


def cancel_game(update, _):
    f"""Ответ на кнопки {NO_MORE_GAME_BTN}, {ENOUGH_BTN}, {EAT_CORN_BTN}
    и {CATS_TRAIN_BTN}."""
    confirmation = ReplyKeyboardMarkup(
        [[ENOUGH_BTN], [NEGATIVE_BTN]], resize_keyboard=True
    )
    main_menu = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
    text = update.message.text
    if text == NO_MORE_GAME_BTN:
        update.message.reply_text(
            text='Точно не хочешь про-должать? 🧐',
            reply_markup=confirmation
        )
        return None
    update.message.reply_text(
        text='Ладно. За-хочешь ещё сыграть - ты знаешь, где меня най-ти 😼',
        reply_markup=main_menu
    )
    return ConversationHandler.END


def show_hall_of_fame(update, _):
    f"""Ответ на нажатие кнопки {HALL_OF_FAME_BTN}."""
    chat_id = update.effective_chat.id
    query = update.callback_query
    query.answer()
    query.edit_message_text(text='✔️')
    for text in txt.HALL_OF_FAME:
        bot.send_message(chat_id=chat_id, text=text)
        time.sleep(1)
    rating, last_champion = func.hall_of_fame()
    if rating is None:
        bot.send_message(chat_id=chat_id, text='Зал славы пока пуст 🤷🏻‍♂️')
        return BOT_DICE
    medals = ['🥉', '🥈', '🥇']
    champion = ''
    places = '〰️〰️〰️〰️〰️〰️〰️〰️〰️\n'
    rest = '〰️〰️〰️〰️〰️〰️〰️〰️〰️\n'
    for person in rating:
        if person[5] >= 5 and medals:
            places += f'{medals[-1]}  ' + f'{person[-1]}' + '\n'
            medals.pop()
            if not champion:
                champion = f'Чемпион:  {person[-1]}  👑\n'
                champ_name = person[-1]
        else:
            rest += (f'{person[-1]}  🔜  осталось сыграть:  {5 - person[5]}\n'
                     if person[5] < 5 else '  🔝\n')
    if champion:
        if champ_name != last_champion.get('name'):
            today = dt.date.today().strftime('%d.%m.%Y г.')
            db = shelve.open(STATISTIC_PATH)
            last_champ = db['DICE_CHAMPION']
            last_champ.update({'name': champ_name, 'date': today})
            db['DICE_CHAMPION'] = last_champ
            db.close()
            champion_from_date = today + '\n'
        else:
            champion_from_date = last_champion['date'] + '\n'
    bot.send_message(chat_id=chat_id,
                     text=champion + ('получил титул ' if champion else '')
                     + (champion_from_date if champion else '')
                     + places + rest)
    for (share_of_wins, average_dice_to_win, share_of_guessed_bet, dry_wins,
         triple_bet, games, wins, looses, made_bet, guessed_bet, double_six,
         share_of_double_six, double_one, share_of_double_one,
         share_of_dry_wins, share_of_triple_bet, name) in rating:
        bot.send_message(
            chat_id=chat_id,
            text=txt.RESULT.format(
                name, games, wins, -share_of_wins, looses, -dry_wins,
                share_of_dry_wins, -triple_bet, share_of_triple_bet,
                average_dice_to_win, made_bet, guessed_bet,
                -share_of_guessed_bet, double_six, share_of_double_six,
                double_one, share_of_double_one
            )
        )
    bot.send_message(
        chat_id=chat_id,
        text='Ну что, готов(а) сместить текуще-го чемпиона? '
             'Кажется, он уже за-сиделся... 🤫'
    )
    return BOT_DICE


def place_bet(update, _):
    """Стандартный ответ на этапе ставки игрока."""
    update.message.reply_text(
        'Тебе нужно сде-лать ставку 🤨\nВведи два разных числа через про-бел:\n'
        'минимум 3️⃣, максимум 1️⃣1️⃣.'
    )


def go_on(update, _):
    """Стандартный ответ на этапе бросков кубика игроком."""
    update.message.reply_text('Тебе ну-жно бросить кубик. Сосре-доточься 🤨')


def main():
    """Основная функция запуска бота."""
    updater = Updater(token=BOT_TOKEN)
    handler = updater.dispatcher.add_handler
    handler(CommandHandler('start', wake_up))
    handler(CommandHandler('hidden', show_hidden_phrases))
    handler(CommandHandler('visitors', show_visitors))
    birthday_сonversation = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex(SURPRISE_ME_BTN), birthday_init)
        ],
        states={
            BIRTH_1: [
                MessageHandler(
                    Filters.regex(f'{STUPID_BTN}|{NOT_STUPID_BTN}'),
                    cancel_or_birthday_1
                )
            ],
            BIRTH_2: [
                MessageHandler(
                    Filters.regex(f'{DONE_NEXT_BTN}|' + r'^\d{1,2}$'),
                    birthday_2
                )
            ],
            BIRTH_3: [
                MessageHandler(
                    Filters.regex(f'{MATH_BAD_BTN}|' + r'^\d{3,4}$'),
                    birthday_3
                )
            ],
            BIRTH_4: [
                MessageHandler(Filters.regex(r'^\d{3,4}$'), birthday_4)
            ],
            BIRTH_5: [
                MessageHandler(
                    Filters.regex(f'{NOT_MY_BIRTH_BTN}|{EXTRASENS_BTN}'),
                    birthday_finish
                )
            ],
        },
        fallbacks=[MessageHandler(Filters.all, birth_fallback)]
    )
    handler(birthday_сonversation)
    falafel_сonversation = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('^Фалафель$'), secret_dossier)
        ],
        states={
            FALAFEL: [
                MessageHandler(
                    Filters.regex(HAVE_DOSSIERS), show_secret_dossier
                ),
                MessageHandler(
                    Filters.regex(RED_BTN), cancel_secret_dossier
                ),
                MessageHandler(Filters.all, bad_command)
            ],
        },
        fallbacks=[]
    )
    handler(falafel_сonversation)
    dice_game_сonversation = ConversationHandler(
        entry_points=[
            MessageHandler(
                Filters.regex(f'{NEXT_TIME_BTN}|{LETS_PLAY_BTN}'),
                no_play_or_game_rules
            )
        ],
        states={
            BOT_DICE: [
                MessageHandler(
                    Filters.regex(
                        f'{BEGIN_BTN}|{YOUR_TURN_BTN}|{REVENGE_BTN}|'
                        f'{WIN_BACK_BTN}'
                    ),
                    bot_bet_roll_dice
                ),
                MessageHandler(
                    Filters.regex(f'{CATS_TRAIN_BTN}|{EAT_CORN_BTN}'),
                    cancel_game
                ),
                CallbackQueryHandler(show_hall_of_fame),
                MessageHandler(Filters.all, push_button)
            ],
            USER_BET: [
                MessageHandler(Filters.regex(BET_RANGE), user_bets),
                MessageHandler(
                    Filters.regex(f'{NO_MORE_GAME_BTN}|{ENOUGH_BTN}'),
                    cancel_game
                ),
                MessageHandler(Filters.all, place_bet)
            ],
            USER_DICE: [
                MessageHandler(Filters.dice, user_roll_dice),
                MessageHandler(Filters.all, go_on)
            ],
        },
        fallbacks=[]
    )
    handler(dice_game_сonversation)
    zodiac_сonversation = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex(SO_INTERESTING_BTN),
                           zodiac_init_or_end)
        ],
        states={
            HOROSCOPE_1: [
                CallbackQueryHandler(zodiac_result),
                MessageHandler(Filters.all, zodiac_choose_sign)
            ],
            HOROSCOPE_2: [
                MessageHandler(Filters.regex(ADORE_HOROSCOPE_BTN),
                               zodiac_init_or_end),
                MessageHandler(Filters.all, push_button)
            ],
        },
        fallbacks=[]
    )
    handler(zodiac_сonversation)
    weather_сonversation = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex(I_NEED_IT_BTN),
                           weather_init)
        ],
        states={
            WEATHER_1: [
                MessageHandler(Filters.all, weather_result)
            ],
            WEATHER_2: [
                MessageHandler(
                    Filters.regex(f'{TOMORROW_BTN}|{WILL_CHECK_BTN}'),
                    weather_tomorrow_or_end)
            ],
        },
        fallbacks=[]
    )
    handler(weather_сonversation)
    handler(MessageHandler(Filters.regex(STRANGE_NAME_BTN), strange_name))
    handler(MessageHandler(Filters.regex(CAT_BTN), show_cat_picture))
    handler(MessageHandler(Filters.regex(ANECDOTE_BTN), show_anecdote))
    handler(MessageHandler(
        Filters.regex(f'{SO_SO_BTN}|{BRAVO_BTN}'), bravo_or_so_so)
    )
    handler(MessageHandler(Filters.regex(TALANTS_BTN), talants))
    handler(MessageHandler(Filters.regex(WHAT_ARE_YOU_BTN), what_are_you))
    handler(MessageHandler(Filters.regex(HAVE_MERCY_BTN), have_mercy_answer))
    handler(MessageHandler(Filters.regex(f'{KOMBIKORM_BTN}|{NO_FUNNY_BTN}'),
                           no_funny_or_kombikorm))
    handler(MessageHandler(
        Filters.regex(HIDDEN_PHRASES), answer_hidden_phrases)
    )
    handler(MessageHandler(Filters.all & ~Filters.command, default_answer))
    handler(CallbackQueryHandler(stop_petting, pattern='stop_petting'))
    handler(CallbackQueryHandler(choice_talant, pattern='Д|Г|К|П'))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    func.start_logging()
    main()
