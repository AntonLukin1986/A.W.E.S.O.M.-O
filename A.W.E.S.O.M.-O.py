"""Телеграм-бот A.W.E.S.O.M.-0."""
import datetime as dt
import logging
import os
import random
import time

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from telegram import Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (CommandHandler, ConversationHandler, Filters, MessageHandler, Updater)
import requests

import text_for_bot as txt
import functions as func


load_dotenv()
token = os.getenv('AWESOM_O_TOKEN')
bot = Bot(token=token)


def start_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s, %(levelname)s, %(message)s, '
               '%(funcName)s, %(lineno)s',
        handlers=[logging.StreamHandler(),
                  logging.handlers.RotatingFileHandler(
                      __file__ + '.log', maxBytes=2100000,
                      backupCount=2, encoding='utf-8')]
    )


ANECDOTE_BTN = 'Расскажи анекдот 😃'
BRAVO_BTN = 'Браво! Это гениально 🤣'
CAT_BTN = 'Котика хочу 🐈'
CATS_TRAIN_BTN = 'Пойду тренироваться. На кошках 🐈'
DONE_NEXT_BTN = 'Сделано ✔️ Давай дальше'
EAT_CORN_BTN = 'Пойду грызть свою кукурузку 😋'
ENOUGH_BTN = 'Точно! Хватит 🖐'
EXTRASENS_BTN = 'Круто! Ты экстрасенс 😲'
BEGIN_BTN = 'Поехали 👌'
HANDS_UP_BTN = 'Я вообще Руки Вверх люблю 🙌'
HAVE_MERCY_BTN = 'О, нет! Ш.И.К.А.Р.Н.-О, пощади 😨🙏'
KOMBIKORM_BTN = 'Комбикорм! Ммм... Вкуснятина 😋'
LETS_PLAY = 'Изи! Создавай 🤠'
MATH_BAD_BTN = 'Математика явно не моё 😔'
MORE_TALANTS_BTN = 'А какие у тебя ещё таланты 😏'
NEXT_TIME = 'В другой раз 🙅🏻‍♂️'
NO_FUNNY_BTN = 'Очень смешно 😤'
NO_MORE_GAME_BTN = 'Больше не хочу играть 😐'
NOT_MY_BIRTH_BTN = 'Неа, неверно! 🤨'
NOT_STUPID_BTN = 'Я тебе не тупица! 😤'
PETTING_BTN = 'Давай поглажу 🤗'
RED_BTN = 'Красная кнопка 🔴'
REVENGE_BTN = 'Хочу реванш 🥊'
SO_SO_BTN = 'Ну, такое себе 🙄'
SONG_BTN = 'Спой песенку 🎤'
STRANGE_NAME_BTN = 'Странное у тебя имя 🤔'
STUPID_BTN = 'Я тупица! 😢'
SURPRISE_ME = 'А ну-ка, удиви! 😐'
WHAT_ARE_YOU_BTN = 'Да что ты такое 🤨'
WIN_BACK_BTN = 'Дам тебе отыграться 😙'
YOUR_TURN_BTN = 'Твой ход 👆'

BET_RANGE = r'^([3-9]|[1][0-1]) ([3-9]|[1][0-1])$'
CARTMAN = r'Эрик[ае]? Картман[ае]?'
CREATOR = r'^Кто такой Создатель\??$'
INNA = r'^Кто такая Няшка\??$'
KENNY = r'^Они убили Кен+и$'
KEP4IK = r'^Кто такой Кэп\??$'
LEMUR = r'^Кто такая Лемур\??$'
MARIK = r'^Кто такой Марик\??$'
MARINA = r'^Кто такая Маришка\??$'
UNKNOWN = r'^Кто так(ой|ая) [А-я]{3,20}\??$'
ZAJA = r'^Кто такой Зажа\??$'
ZERO = r'[Пп]ритвор[ия](сь|ть?ся) ноликом'

BIRTH_1, BIRTH_2, BIRTH_3, BIRTH_4, BIRTH_5 = range(5)
FALAFEL = 1
BOT_DICE, USER_BET, USER_DICE = range(3)
BOT_WINS = 0
USER_DICE_COUNTER = 0
USER_DICE_RESULT = 0
USER_WINS = 0


def wake_up(update, context):
    """Реакция бота на активацию "/start"."""
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([[PETTING_BTN]], resize_keyboard=True)
    TEXT = (f'Привет, {name}! Я робот Ш.И.К.А.Р.Н.-О четыре тысячи 🤖',
            'Высокоинтеллектуальный нано-кибернетический '
            'био-резонансный организм ⚙️', 'Можешь меня погладить 🙃')
    context.bot.send_message(chat.id, TEXT[0])
    time.sleep(1.5)
    context.bot.send_message(chat.id, TEXT[1])
    time.sleep(1.5)
    context.bot.send_message(chat.id, TEXT[2], reply_markup=button)


def stop_petting(update, _):
    """Ответ бота на нажатие кнопки "Давай поглажу 🤗"."""
    TEXT = ('Ш.И.К.А.Р.Н.-О нравится.', 'Ш.И.К.А.Р.Н.-О хорошо.',
            'Продолжай', '...', 'Хватит тро-гать мою ба-тарейку!')
    button = ReplyKeyboardMarkup([[STRANGE_NAME_BTN]], resize_keyboard=True)
    for text in TEXT[:-1]:
        update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
        time.sleep(1.5)
    update.message.reply_text(TEXT[-1], reply_markup=button)


def strange_name(update, _):
    """Ответ бота на нажатие кнопки "Странное у тебя имя 🤔"."""
    TEXT = ('Я на-зван в честь главного персона-жа 2 серии 8 сезона мультсе-'
            'риала "South Park".\nЕсли не по-смотришь её, Ш.И.К.А.Р.Н.-О '
            'будет грустным пандой 🐼\nhttp://online-south-park.ru/season-8/'
            '130-8-sezon-2-seriya-shikarn-o.html')
    button = ReplyKeyboardMarkup([[CAT_BTN, ANECDOTE_BTN],
                                  [SONG_BTN, WHAT_ARE_YOU_BTN]],
                                 resize_keyboard=True)
    update.message.reply_text(TEXT, reply_markup=button)


def default_answer(update, _):
    """Ответ бота на любой неопознанный текст."""
    ANSWERS = ('Чё душишь меня? 😠', 'Ну ясно! Что ещё скажешь? 🤨',
               'Ш.И.К.А.Р.Н.-О не понимать твой диалект 🤷🏻‍♀️',
               'Отказано! Лучше почисти мои тран-зис-торы 🪛🔧',
               'Рамамба Хару Мамбуру 🤪')
    update.message.reply_text(random.choice(ANSWERS))


def get_new_cat_image(update):
    """Получение случайной картинки котика или пёсика."""
    CATS_URL = 'https://api.thecatapi.com/v1/images/search'
    DOGS_URL = 'https://api.thedogapi.com/v1/images/search'
    try:
        response = requests.get(CATS_URL).json()
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        response = requests.get(DOGS_URL).json()
        update.message.reply_text('Упс! Котиков не подвезли. Вот тебе пёсик 🐶')
    random_cat = response[0].get('url')
    return random_cat


def show_cat_picture(update, _):
    """Ответ бота на нажатие кнопки "Котика хочу 🐈"."""
    button = ReplyKeyboardMarkup([[NEXT_TIME], [LETS_PLAY]], resize_keyboard=True)
    update.message.reply_text(text='Ш.И.К.А.Р.Н.-О любит котиков 😻 Кыс-кыс-кыс!', reply_markup=ReplyKeyboardRemove())
    time.sleep(1)
    update.message.reply_photo(get_new_cat_image(update))
    time.sleep(1)
    update.message.reply_text(random.choice(txt.SHOW_CAT_TEXT))
    time.sleep(1)
    update.message.reply_text('Котики это хо-рошо. А как насчёт переки-нуться в кости? 😉', reply_markup=button)


def some_song(update, _):
    """Ответ бота на нажатие кнопки "Спой песенку 🎤"."""
    SONG = random.choice((txt.SONG_1, txt.SONG_2, txt.SONG_3,
                          txt.SONG_4, txt.SONG_5, txt.SONG_6))
    button = ReplyKeyboardMarkup([[HANDS_UP_BTN], [MORE_TALANTS_BTN]],
                                 resize_keyboard=True)
    update.message.reply_text(text=SONG, reply_markup=ReplyKeyboardRemove())
    time.sleep(1.5)
    update.message.reply_text(random.choice(txt.SOME_SONG_TEXT), reply_markup=button)


def song_reaction(update, _):
    """Ответ бота на фразы "Я вообще Руки Вверх люблю 🙌" и
    "А какие у тебя ещё таланты 😏"."""
    if update.message.text == HANDS_UP_BTN:
        button = ReplyKeyboardMarkup([[CAT_BTN, ANECDOTE_BTN],
                                      [SONG_BTN, WHAT_ARE_YOU_BTN]],
                                     resize_keyboard=True)
        text = 'Хорошо хоть не Ногу Свело 🦵'
    else:
        button = ReplyKeyboardMarkup([[SURPRISE_ME]], resize_keyboard=True)
        text = ('Силой электронно-вычислитель-ной мысли '
                'могу угадать день твоего ро-ждения 🧙🏻')
    update.message.reply_text(text=text, reply_markup=button)


def birthday_init(update, _):
    """Ответ бота на нажатие кнопки "А ну-ка, удиви! 😐"."""
    button = ReplyKeyboardMarkup([[NOT_STUPID_BTN], [STUPID_BTN]],
                                 resize_keyboard=True)
    update.message.reply_text(
        text='Нужно будет немножко по-считать. Возьми кальку-лятор. '
             'Надеюсь, ты умеешь им поль-зоваться? 🤭',
        reply_markup=button)
    return BIRTH_1


def cancel_or_birthday_1(update, _):
    """Ответ бота на фразы "Я тупица! 😢" и "Я тебе не тупица! 😤"."""
    if update.message.text == STUPID_BTN:
        button = ReplyKeyboardMarkup([[CAT_BTN, ANECDOTE_BTN],
                                      [SONG_BTN, WHAT_ARE_YOU_BTN]],
                                     resize_keyboard=True)
        update.message.reply_text(
            text='А я сразу понял, что соображал-ка у тебя не очень 🙄\n'
                 'Ну ничего. Осознание - первый путь к ис-правлению!\n'
                 'Начни со счётных пало-чек... 🦧',
            reply_markup=button)
        return ConversationHandler.END
    else:
        button = ReplyKeyboardMarkup([[DONE_NEXT_BTN]], resize_keyboard=True)
        update.message.reply_text(text='Вот и проверим.\nДействуй со-гласно '
                                       'моим указа-ниям ☝️\n')
        time.sleep(1.5)
        update.message.reply_text(
            text='Первым де-лом умножь число своего ро-ждения на 2 ☑️\n'
                 'К ре-зультату прибавь 5 ☑️',
            reply_markup=button)
        return BIRTH_2


def birthday_2(update, _):
    """Ответ бота на нажатие кнопки "Сделано ✔️ Давай дальше"."""
    button = ReplyKeyboardMarkup([[MATH_BAD_BTN]], resize_keyboard=True)
    if update.message.text == DONE_NEXT_BTN:
        update.message.reply_text(
            text='Полу-ченное число умножь на 50 ☑️\nЗатем прибавь поряд-ковый'
                 ' номер месяца своего ро-ждения.\n'
                 'На-пример, январь - 1ый, декабрь - 12ый ☑️',
            reply_markup=ReplyKeyboardRemove())
        time.sleep(1.5)
        update.message.reply_text(
            text='Ну как? Твой про-цессор ещё не пере-грелся? 🤯\n'
                 'Термопасту поме-нять не нужно?',
            reply_markup=button)
        return BIRTH_3
    else:
        update.message.reply_text(
            text='Введёшь число, когда я ска-жу 🤦🏻‍♂️\nВнизу есть кнопка...')


def birthday_3(update, _):
    """Ответ бота на нажатие кнопки "Математика явно не моё 😔"."""
    if update.message.text == MATH_BAD_BTN:
        update.message.reply_text(
            text='Со-берись, тряпка! 😠 Больше ничего счи-тать не нужно.\n',
            reply_markup=ReplyKeyboardRemove())
        time.sleep(1.5)
        update.message.reply_text(
            text='Перепроверь, что посчитано без ошибок 🤓\n'
                 'Если всё верно - напиши число, кото-рое у тебя по-лучилось.')
        return BIRTH_4
    else:
        update.message.reply_text(
            text='Не нужно сейчас вводить число 🤦🏻‍♂️\nВнизу есть кнопка...')


def birthday_4(update, _):
    """Ответ бота на введённое число."""
    button = ReplyKeyboardMarkup([[EXTRASENS_BTN], [NOT_MY_BIRTH_BTN]],
                                 resize_keyboard=True)
    MONTHS = {1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля', 5: 'мая',
              6: 'июня', 7: 'июля', 8: 'августа', 9: 'сентября', 10: 'октября',
              11: 'ноября', 12: 'декабря'}
    try:
        result = int(update.message.text) - 250
        day = result // 100
        month = MONTHS[result % 100]
        update.message.reply_text(text='Барабанная дробь... 🥁')
        time.sleep(1.5)
        update.message.reply_text(text=f'День твоего рождения ⚜️ {day} {month} ⚜️',
                                  reply_markup=button)
        if str(result) == dt.datetime.today().strftime('%d%m'):
            time.sleep(1.5)
            update.message.reply_text(
                text='Так это же сегодня!\nПо-здравляю с Днём Варенья!\n'
                     'Расти большой, не будь ла-пшой 🥳🎊🎉')
        return BIRTH_5
    except KeyError:
        update.message.reply_text('Перепро-верь результат. Где-то ошибка ☝️')


def birthday_finish(update, _):
    """Ответ бота на фразы "Круто! Ты экстрасенс 😲" и "Неа, неверно! 🤨"."""
    button = ReplyKeyboardMarkup([[CAT_BTN, ANECDOTE_BTN],
                                  [SONG_BTN, WHAT_ARE_YOU_BTN]],
                                 resize_keyboard=True)
    if update.message.text == EXTRASENS_BTN:
        text = ('Я знаю, я крут 😎\nС тебя 100$ 💵\n'
                'Пе-реведи на мой электрон-ный кошелёк')
    else:
        text = ('Да ты просто счи-тать не умеешь 🤦🏻‍♂️\nА ещё говорят '
                'человек - вершина эволюции. Ну-ну... 🤔')
    update.message.reply_text(text=text, reply_markup=button)
    return ConversationHandler.END


def birth_fallback(update, _):
    """Ответ бота на любой неопознанный текст внутри диалога ДР."""
    update.message.reply_text(text='Так дело не пойдёт...\nДавай, со-'
                                   'средоточься и действуй по инструк-ции 🧐')


def show_anecdote(update, _):
    """Ответ бота на нажатие кнопки "Расскажи анекдот 😃"."""
    try:
        response = requests.get('http://anekdotme.ru/random/')
        # С помощью парсера получаем HTML-код страницы
        page_html = BeautifulSoup(response.text, 'html.parser')
        # Из HTML-кода страницы выбираем все объекты class='anekdot_text',
        # получаем список. Берём первый объект из списка и получаем его текст.
        anecdote = page_html.select('.anekdot_text')[0].get_text()
        TEXT = ('Ш.И.К.А.Р.Н.-О знает много а-нек-до-тов. Вот:', anecdote,
                'Аха-ха! Мой процессор сейчас лопнет от смеха 🤣')
        button = ReplyKeyboardMarkup([[SO_SO_BTN], [BRAVO_BTN]],
                                     resize_keyboard=True)
        for text in TEXT:
            update.message.reply_text(text, reply_markup=ReplyKeyboardRemove() if text != TEXT[-1] else button)
            time.sleep(1.5)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        button = ReplyKeyboardMarkup([[CAT_BTN, ANECDOTE_BTN],
                                      [SONG_BTN, WHAT_ARE_YOU_BTN]],
                                     resize_keyboard=True)
        update.message.reply_text(
            text='Дол-баные вышки 5G. Они жгут мои микро-схемы 😕\n'
                 'Расскажу в сле-дующий раз...',
            reply_markup=button)


def bravo_or_so_so(update, _):
    """Ответ бота на фразы "Ну такое себе 🤨" и "Браво! Это гениально 🤣"."""
    button = ReplyKeyboardMarkup([[CAT_BTN, ANECDOTE_BTN],
                                  [SONG_BTN, WHAT_ARE_YOU_BTN]],
                                 resize_keyboard=True)
    if update.message.text == BRAVO_BTN:
        TEXT = ('Молодец! Возьми с полки пиро-жок 🥯', 'Ещё бы! Я учил-ся у самого '
                'Ви-нокура 😉', 'Смотри, чтоб пу-пок от смеха не развя-зался 🙈')
    else:
        TEXT = ('У тебя просто нет чу-вства юмора 😤', 'До тебя просто дол-го доход'
                'ит. Как до жира-фа 🦒', 'Иди смотри Смехопанора-му тогда 😠')
    update.message.reply_text(text=random.choice(TEXT), reply_markup=button)


def what_are_you(update, _):
    """Ответ бота на нажатие кнопки "Да что ты такое 🤨"."""
    button = ReplyKeyboardMarkup([[HAVE_MERCY_BTN]],
                                 resize_keyboard=True)
    for text in txt.AWESOM_O_STORY[:-1]:
        update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
        time.sleep(1)
    update.message.reply_text(txt.AWESOM_O_STORY[-1], reply_markup=button)


def have_mercy_answer(update, _):
    """Ответ бота на нажатие кнопки "О, нет! Ш.И.К.А.Р.Н.-О, пощади 😨🙏"."""
    button = ReplyKeyboardMarkup([[KOMBIKORM_BTN], [NO_FUNNY_BTN]],
                                 resize_keyboard=True)
    update.message.reply_text(
        text='Расслабься! Ш.И.К.А.Р.Н.-О пошутил\nБуду кормить тебя '
             'ком-бикормом.\nИли что вы там еди-те? 😎',
        reply_markup=button)


def no_funny_or_kombikorm(update, _):
    """Ответ бота на фразы "Очень смешно 😤" и "Комбикорм! Ммм... Вкуснятина 😋"."""
    button = ReplyKeyboardMarkup([[CAT_BTN, ANECDOTE_BTN],
                                  [SONG_BTN, WHAT_ARE_YOU_BTN]],
                                 resize_keyboard=True)
    if update.message.text == KOMBIKORM_BTN:
        TEXT = txt.DOSIER
    else:
        TEXT = txt.NO_FUNNY
    for text in TEXT[:-1]:
        update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
        time.sleep(1.5)
    update.message.reply_text(TEXT[-1], reply_markup=button)


def secret_dossier(update, _):
    """Ответ бота на слово "Фалафель"."""
    button = ReplyKeyboardMarkup([[RED_BTN]], resize_keyboard=True)
    for text in txt.DOSSIER_TEXT[:-1]:
        update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
        time.sleep(2)
    update.message.reply_text(text=txt.DOSSIER_TEXT[-1], reply_markup=button)
    return FALAFEL


def cancel_secret_dossier(update, _):
    """Ответ бота на нажатие кнопки "Красная кнопка 🔴"."""
    button = ReplyKeyboardMarkup([[CAT_BTN, ANECDOTE_BTN],
                                  [SONG_BTN, WHAT_ARE_YOU_BTN]],
                                 resize_keyboard=True)
    for text in txt.SELFDESTRUCTION[:-1]:
        update.message.reply_text(text=text)
        time.sleep(1.5)
    update.message.reply_text(txt.SELFDESTRUCTION[-1], reply_markup=button)
    return ConversationHandler.END


def who_is_creator(update, _):
    """Ответ бота на вопрос "Кто такой Создатель?"."""
    for text in txt.WHO_IS_CREATOR:
        update.message.reply_text(text=text)
        time.sleep(2)


def who_is_kep4ik(update, _):
    """Ответ бота на вопрос "Кто такой Кэп?"."""
    for text in txt.WHO_IS_KEP:
        update.message.reply_text(text=text)
        time.sleep(2)


def who_is_inna(update, _):
    """Ответ бота на вопрос "Кто такая Няшка?"."""
    for text in txt.WHO_IS_INNA:
        update.message.reply_text(text=text)
        time.sleep(2)


def who_is_natasha(update, _):
    """Ответ бота на вопрос "Кто такая Лемур?"."""
    for text in txt.WHO_IS_NATASHA:
        update.message.reply_text(text=text)
        time.sleep(2)


def who_is_zaja(update, _):
    """Ответ бота на вопрос "Кто такой Зажа?"."""
    for text in txt.WHO_IS_ZAJA:
        update.message.reply_text(text=text)
        time.sleep(2)


def who_is_marik(update, _):
    """Ответ бота на вопрос "Кто такой Марик?"."""
    for text in txt.WHO_IS_MARIK:
        update.message.reply_text(text=text)
        time.sleep(2)


def who_is_marishka(update, _):
    """Ответ бота на вопрос "Кто такая Маришка?"."""
    for text in txt.WHO_IS_MARISHKA:
        update.message.reply_text(text=text)
        time.sleep(2)


def bad_command(update, _):
    """Стандартный ответ в режиме диалога Фалафель."""
    update.message.reply_text(text='Несуществующая команда 🚫')


def they_killed_kenny(update, _):
    """Ответ бота на сообщение "Они убили Кенни"."""
    for text in txt.KENNY:
        update.message.reply_text(text=text)
        time.sleep(2)


def eric_cartman(update, _):
    """Ответ бота на любое упоминание Эрика Картмана."""
    update.message.reply_text(text=txt.CARTMAN)


def pretend_zero(update, _):
    """Ответ бота на сообщение "Притворись ноликом"."""
    update.message.reply_text(text='Может мне ещё крес-тиком начать выши-вать? 🙄')


def marklar(update, _):
    """Ответ бота на сообщение "Марклар"."""
    update.message.reply_text(text=txt.MARKLAR_ANSWER)


def hidden_phrases(update, _):
    """Реакция на команду /hidden - cкрытые фразы для бота."""
    update.message.reply_text('*** Пасхалки ***\n🔸 Они убили Кенни\n🔸 Притворись ноликом\n'
                              '🔸 Эрик Картман\n🔸 Марклар')


def no_play_or_game_rules(update, _):
    """Ответ на кнопки "В другой раз 🙅🏻‍♂️" и "Изи! Доставай 🤠"."""
    if update.message.text == NEXT_TIME:
        main = ReplyKeyboardMarkup([[CAT_BTN, ANECDOTE_BTN], [SONG_BTN, WHAT_ARE_YOU_BTN]], resize_keyboard=True)
        update.message.reply_text('Как знаешь. Угова-ривать не буду 😼', reply_markup=main)
    else:
        global GAME_STAT, PLAYER
        GAME_STAT = {'BOT': dict(wins=0, double_six=0, double_one=0, made_bet=0, guessed_bet=0)}
        PLAYER = update.message.chat.full_name
        GAME_STAT[f'{PLAYER}'] = dict(wins=0, double_six=0, double_one=0, made_bet=0, guessed_bet=0)
        button = ReplyKeyboardMarkup([[BEGIN_BTN]], resize_keyboard=True)
        for text in txt.RULES_DICE:
            update.message.reply_text(text, reply_markup=button if text == txt.RULES_DICE[-1] else ReplyKeyboardRemove())
            time.sleep(1)
        return BOT_DICE


def bot_bet_roll_dice(update, _):
    """Ответ на кнопки "Поехали 👌", "Твой ход 👆", "Хочу реванш 🥊" и "Дам тебе отыграться 😙"."""
    cancel = ReplyKeyboardMarkup([[NO_MORE_GAME_BTN]], resize_keyboard=True)
    choise = ReplyKeyboardMarkup([[REVENGE_BTN], [CATS_TRAIN_BTN]], resize_keyboard=True)
    global BOT_WINS, USER_WINS
    bet_1, bet_2 = random.randint(3, 11), random.randint(3, 11)
    while bet_2 == bet_1:
        bet_2 = random.randint(3, 11)
    update.message.reply_text(f'Я поставлю на {bet_1} и {bet_2} ✍️', reply_markup=ReplyKeyboardRemove())
    time.sleep(1)
    GAME_STAT['BOT']['made_bet'] += 1
    update.message.reply_text('Бросаю ко-сти... ✊')
    result = 0
    for _ in (1, 2):
        value = update.message.reply_dice()['dice']['value']
        result += value
        time.sleep(1.5)
    update.message.reply_text(f'Мой ре-зультат:  {result} ❗️', reply_markup=cancel)
    time.sleep(1)
    if result in (bet_1, bet_2, 2, 12):
        if result == 2:
            update.message.reply_text('О, нет! 😱 Две еди-нички. Минус балл 😭')
            GAME_STAT['BOT']['double_one'] += 1
            if BOT_WINS > 0: BOT_WINS -= 1
        elif result == 12:
            update.message.reply_text('Я со-рвал Джек пот 🥳\nДве шестёрки! Получаю балл 👏')
            GAME_STAT['BOT']['double_six'] += 1
            BOT_WINS += 1
        else:
            update.message.reply_text('Ура! Удача на моей сто-роне 😄\nЯ вы-играл в этом раунде 🦾')
            GAME_STAT['BOT']['guessed_bet'] += 1
            BOT_WINS += 1
        if BOT_WINS == USER_WINS:
            update.message.reply_text(f'Счёт {BOT_WINS} : {USER_WINS}\nУ нас ничья 🍻')
        else:
            update.message.reply_text(
                f'Счёт {BOT_WINS} : {USER_WINS}\n' + ('Я впереди 🤘' if BOT_WINS > USER_WINS else 'В твою пользу 😕'))
        if BOT_WINS == 3:
            time.sleep(1.5)
            update.message.reply_text(
                f'Финальный ре-зультат: 💫 {BOT_WINS} : {USER_WINS} 💫' + ('  Всухую 🙈' if abs(BOT_WINS - USER_WINS) == 3 else '') +
                '\n\n' + 'Ехууу 🥳 Победа за мной!\nУчись у мастера, салага 😎',
                reply_markup=choise)
            GAME_STAT['BOT']['wins'] += 1
            time.sleep(1.5)
            update.message.reply_text(func.dice_game_stat(GAME_STAT, PLAYER))
            BOT_WINS = 0
            USER_WINS = 0
            return BOT_DICE
    else:
        update.message.reply_text('Не угадал 😔\nЛадно, в следую-щий раз повезёт...')
    time.sleep(1)
    update.message.reply_text('Твоя оче-редь. Делай ставку ☝️ и бросай ко-сти.', reply_markup=cancel)
    return USER_BET


def user_bets(update, _):
    """Ответ на ввод пользователем двух чисел перед бросками кубиков."""
    global USER_BET_1, USER_BET_2
    button = ReplyKeyboardMarkup([['🎲']], resize_keyboard=True)
    USER_BET_1, USER_BET_2 = map(int, (update.message.text).split())
    if USER_BET_1 == USER_BET_2:
        update.message.reply_text('Числа должны быть раз-ными! Это в твоих же ин-тересах 🤦🏻‍♂️')
    else:
        update.message.reply_text('Принято! Бросай ко-сти 🎲', reply_markup=button)
        GAME_STAT[f'{PLAYER}']['made_bet'] += 1
        return USER_DICE


def user_roll_dice(update, _):
    """Подсчёт результата бросков кубика игроком."""
    your_turn = ReplyKeyboardMarkup([[YOUR_TURN_BTN]], resize_keyboard=True)
    choice = ReplyKeyboardMarkup([[WIN_BACK_BTN], [EAT_CORN_BTN]], resize_keyboard=True)
    global BOT_WINS, USER_DICE_COUNTER, USER_DICE_RESULT, USER_WINS
    points = update.message.dice['value']
    USER_DICE_COUNTER += 1
    USER_DICE_RESULT += points
    if USER_DICE_COUNTER != 2:
        update.message.reply_text('Бросай ещё 👉')
        return None
    time.sleep(1.5)
    update.message.reply_text(f'Твой результат:  {USER_DICE_RESULT} ❗️', reply_markup=your_turn)
    if USER_DICE_RESULT in (USER_BET_1, USER_BET_2, 2, 12):
        if USER_DICE_RESULT == 2:
            update.message.reply_text('Ха! Две дырки 🙈 Не повез-ло. Минус балл.')
            GAME_STAT[f'{PLAYER}']['double_one'] += 1
            if USER_WINS > 0: USER_WINS -= 1
        elif USER_DICE_RESULT == 12:
            update.message.reply_text('Ничего себе! Две шестёрки 😳 Получаешь балл.')
            GAME_STAT[f'{PLAYER}']['double_six'] += 1
            USER_WINS += 1
        else:
            update.message.reply_text('Удача на твоей сто-роне.\nТы угадал в этот раз 😠')
            GAME_STAT[f'{PLAYER}']['guessed_bet'] += 1
            USER_WINS += 1
        if USER_WINS == BOT_WINS:
            update.message.reply_text(f'Счёт {BOT_WINS} : {USER_WINS}\nУ нас ничья 🍻')
        else:
            update.message.reply_text(
                f'Счёт {BOT_WINS} : {USER_WINS}\n' + ('Я впереди 🙃' if BOT_WINS > USER_WINS else 'В твою пользу 😒'))
        if USER_WINS == 3:
            time.sleep(1.5)
            update.message.reply_text(
                f'Финальный ре-зультат: 💫 {BOT_WINS} : {USER_WINS} 💫' + ('  Всухую 🙈' if abs(BOT_WINS - USER_WINS) == 3 else '') +
                '\n\n' + 'Твоя победа!\nМожешь пола-комиться ку-курузкой 🌽😏\nНо не за-знавайся - тебе просто повез-ло 😈\nПонимаешь, да?',
                reply_markup=choice)
            GAME_STAT[f'{PLAYER}']['wins'] += 1
            time.sleep(1.5)
            update.message.reply_text(func.dice_game_stat(GAME_STAT, PLAYER))
            BOT_WINS = 0
            USER_WINS = 0
    else:
        update.message.reply_text('Не угадал 🤷🏻‍♂️ Ничего, бывает...\nПродолжаем ве-селиться 😉', reply_markup=your_turn)
    USER_DICE_COUNTER, USER_DICE_RESULT = 0, 0
    return BOT_DICE


def cancel_game(update, _):
    """Ответ на кнопки "Больше не хочу играть 😐", "Точно! Хватит 🖐",
    "Пойду грызть свою кукурузку 😋" и "Пойду тренироваться. На кошках 🐈"."""
    global BOT_WINS, USER_BET_1, USER_BET_2, USER_DICE_COUNTER, USER_DICE_RESULT, USER_WINS
    confirm = ReplyKeyboardMarkup([[ENOUGH_BTN], ['Нет, я передумал 🙃']], resize_keyboard=True)
    main = ReplyKeyboardMarkup([[CAT_BTN, ANECDOTE_BTN], [SONG_BTN, WHAT_ARE_YOU_BTN]], resize_keyboard=True)
    if update.message.text == NO_MORE_GAME_BTN:
        update.message.reply_text('Точно не хочешь про-должать?\nВесь прогресс сбросит-ся 🧐', reply_markup=confirm)
    if update.message.text == CATS_TRAIN_BTN or update.message.text == EAT_CORN_BTN or update.message.text == ENOUGH_BTN:
        update.message.reply_text('Ладно. За-хочешь ещё сыграть - ты знаешь, где меня най-ти 😼',
                                  reply_markup=main)
        BOT_WINS = 0
        USER_DICE_COUNTER = 0
        USER_DICE_RESULT = 0
        USER_WINS = 0
        return ConversationHandler.END


def place_bet(update, _):
    """Стандартный ответ на этапе ставки игрока."""
    update.message.reply_text('Тебе нужно сде-лать ставку 🤨\nВведи два разных числа через про-бел:\nминимум 3️⃣, максимум 1️⃣1️⃣.')


def go_on(update, _):
    """Стандартный ответ на этапе бросков кубика игроком."""
    update.message.reply_text('Тебе ну-жно бросить кубик. Сосре-доточься 🤨')


def dice_fallback(update, _):
    """Стандартный ответ внутри диалога игры в кости."""
    update.message.reply_text('У нас игра. Не отвле-кайся 🤨')


def main():
    """Основная функция запуска бота."""
    updater = Updater(token=token)
    handler = updater.dispatcher.add_handler
    handler(CommandHandler('start', wake_up))
    birthday_сonversation = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(SURPRISE_ME), birthday_init)],
        states={
            BIRTH_1: [MessageHandler(Filters.regex(STUPID_BTN + '|' + NOT_STUPID_BTN), cancel_or_birthday_1)],
            BIRTH_2: [MessageHandler(Filters.regex(DONE_NEXT_BTN + '|' + r'^\d{1,2}$'), birthday_2)],
            BIRTH_3: [MessageHandler(Filters.regex(MATH_BAD_BTN + '|' + r'^\d{3,4}$'), birthday_3)],
            BIRTH_4: [MessageHandler(Filters.regex(r'^\d{3,4}$'), birthday_4)],
            BIRTH_5: [MessageHandler(Filters.regex(NOT_MY_BIRTH_BTN + '|' + EXTRASENS_BTN), birthday_finish)],
        },
        fallbacks=[MessageHandler(Filters.all, birth_fallback)]
    )
    handler(birthday_сonversation)
    falafel_сonversation = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^Фалафель$'), secret_dossier)],
        states={
            FALAFEL: [MessageHandler(Filters.regex(CREATOR), who_is_creator),
                      MessageHandler(Filters.regex(KEP4IK), who_is_kep4ik),
                      MessageHandler(Filters.regex(INNA), who_is_inna),
                      MessageHandler(Filters.regex(LEMUR), who_is_natasha),
                      MessageHandler(Filters.regex(ZAJA), who_is_zaja),
                      MessageHandler(Filters.regex(MARIK), who_is_marik),
                      MessageHandler(Filters.regex(MARINA), who_is_marishka),
                      MessageHandler(Filters.regex(RED_BTN), cancel_secret_dossier)],
        },
        fallbacks=[MessageHandler(Filters.all, bad_command)]
    )
    handler(falafel_сonversation)
    dice_game_сonversation = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(NEXT_TIME + '|' + LETS_PLAY), no_play_or_game_rules)],
        states={
            BOT_DICE: [MessageHandler(Filters.regex(BEGIN_BTN + '|' + YOUR_TURN_BTN + '|' + REVENGE_BTN + '|' + WIN_BACK_BTN),
                                      bot_bet_roll_dice),
                       MessageHandler(Filters.regex(CATS_TRAIN_BTN + '|' + EAT_CORN_BTN), cancel_game)],
            USER_BET: [MessageHandler(Filters.regex(BET_RANGE), user_bets),
                       MessageHandler(Filters.regex(NO_MORE_GAME_BTN + '|' + ENOUGH_BTN), cancel_game),
                       MessageHandler(Filters.all, place_bet)],
            USER_DICE: [MessageHandler(Filters.dice, user_roll_dice),
                        MessageHandler(Filters.all, go_on)],
        },
        fallbacks=[MessageHandler(Filters.all, dice_fallback)]
    )
    handler(dice_game_сonversation)
    handler(MessageHandler(Filters.regex(PETTING_BTN), stop_petting))
    handler(MessageHandler(Filters.regex(STRANGE_NAME_BTN), strange_name))
    handler(MessageHandler(Filters.regex(CAT_BTN), show_cat_picture))
    handler(MessageHandler(Filters.regex(ANECDOTE_BTN), show_anecdote))
    handler(MessageHandler(Filters.regex(SO_SO_BTN + '|' + BRAVO_BTN), bravo_or_so_so))
    handler(MessageHandler(Filters.regex(SONG_BTN), some_song))
    handler(MessageHandler(Filters.regex(HANDS_UP_BTN + '|' + MORE_TALANTS_BTN), song_reaction))
    handler(MessageHandler(Filters.regex(WHAT_ARE_YOU_BTN), what_are_you))
    handler(MessageHandler(Filters.regex(HAVE_MERCY_BTN), have_mercy_answer))
    handler(MessageHandler(Filters.regex(KOMBIKORM_BTN + '|' + NO_FUNNY_BTN), no_funny_or_kombikorm))
    handler(MessageHandler(Filters.regex(KENNY), they_killed_kenny))
    handler(MessageHandler(Filters.regex(CARTMAN), eric_cartman))
    handler(MessageHandler(Filters.regex(ZERO), pretend_zero))
    handler(MessageHandler(Filters.regex('Марклар'), marklar))
    handler(MessageHandler(Filters.all & ~Filters.command, default_answer))
    handler(CommandHandler('hidden', hidden_phrases))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    # start_logging()
    main()
