"""Телеграм-бот Ш.И.К.А.Р.Н.-О"""
import datetime as dt
import logging
import os
import random
import re
import shelve
import time

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from telegram import Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)
import requests

import functions as func
import texts_for_bot as txt

load_dotenv()
TOKEN = os.getenv('AWESOM_O_TOKEN')
bot = Bot(token=TOKEN)

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
BEGIN_BTN = 'Поехали 👌'
BRAVO_BTN = 'Браво! Это гениально 🤣'
CAT_BTN = 'Котика хочу 🐈'
CATS_TRAIN_BTN = 'Пойду тренироваться. На кошках 🐈'
DONE_NEXT_BTN = 'Сделано ✔️ Давай дальше'
EAT_CORN_BTN = 'Пойду грызть свою кукурузку 😋'
ENOUGH_BTN = 'Точно! Хватит 🖐'
EXTRASENS_BTN = 'Круто! Ты экстрасенс 😲'
HALL_OF_FAME_BTN = 'Покажи зал славы игроков 🤩'
HANDS_UP_BTN = 'Я вообще Руки Вверх люблю 🙌'
HAVE_MERCY_BTN = 'О, нет! Ш.И.К.А.Р.Н.-О, пощади 😨🙏'
KOMBIKORM_BTN = 'Комбикорм! Ммм... Вкуснятина 😋'
LETS_PLAY_BTN = 'Изи! Создавай 🤠'
MATH_BAD_BTN = 'Математика явно не моё 😔'
MORE_TALANTS_BTN = 'А какие у тебя ещё таланты 😏'
NEXT_TIME_BTN = 'В другой раз 🙅🏻‍♂️'
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
STUPID_BTN = 'Я тупица... 😢'
SURPRISE_ME_BTN = 'А ну-ка, удиви! 😐'
WHAT_ARE_YOU_BTN = 'Да что ты такое 🤨'
WIN_BACK_BTN = 'Дам тебе отыграться 😙'
YOUR_TURN_BTN = 'Твой ход 👆'
MAIN_MENU = [[CAT_BTN, ANECDOTE_BTN], [SONG_BTN, WHAT_ARE_YOU_BTN]]

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
OR = '|'
HIDDEN_PHRASES = KENNY + OR + CARTMAN + OR + ZERO + OR + 'Марклар'
HAVE_DOSSIERS = (CREATOR + OR + KEP4IK + OR + INNA + OR + LEMUR +
                 OR + ZAJA + OR + MARIK + OR + MARINA)

BIRTH_1, BIRTH_2, BIRTH_3, BIRTH_4, BIRTH_5 = range(5)
FALAFEL = 1
BOT_DICE, USER_BET, USER_DICE = range(3)


def wake_up(update, context):
    """Реакция на активацию "/start"."""
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([[PETTING_BTN]], resize_keyboard=True)
    text = (f'Привет, {name}! Я робот Ш.И.К.А.Р.Н.-О четыре тысячи 🤖',
            'Высокоинтеллектуальный нано-кибернетический '
            'био-резонансный организм ⚙️', 'Можешь меня погладить 🙃')
    context.bot.send_message(chat.id, text[0])
    time.sleep(1.5)
    context.bot.send_message(chat.id, text[1])
    time.sleep(1.5)
    context.bot.send_message(chat.id, text[2], reply_markup=button)


def stop_petting(update, _):
    """Ответ на нажатие кнопки "Давай поглажу 🤗"."""
    text = ('Ш.И.К.А.Р.Н.-О нравится.', 'Ш.И.К.А.Р.Н.-О хорошо.',
            'Продолжай', '...', 'Хватит тро-гать мою ба-тарейку!')
    button = ReplyKeyboardMarkup([[STRANGE_NAME_BTN]], resize_keyboard=True)
    for phrase in text[:-1]:
        update.message.reply_text(phrase, reply_markup=ReplyKeyboardRemove())
        time.sleep(1.5)
    update.message.reply_text(text[-1], reply_markup=button)


def strange_name(update, _):
    """Ответ на нажатие кнопки "Странное у тебя имя 🤔"."""
    text = ('Я на-зван в честь главного персона-жа 2 серии 8 сезона мультсе-'
            'риала "South Park".\nЕсли не по-смотришь её, Ш.И.К.А.Р.Н.-О '
            'будет грустным пандой 🐼\nhttp://online-south-park.ru/season-8/'
            '130-8-sezon-2-seriya-shikarn-o.html')
    button = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
    update.message.reply_text(text, reply_markup=button)


def default_answer(update, _):
    """Ответ на любой неопознанный текст."""
    answers = ('Чё душишь меня? 😠', 'Ну ясно! Что ещё скажешь? 🤨',
               'Ш.И.К.А.Р.Н.-О не понимать твой диалект 🤷🏻‍♀️',
               'Отказано! Лучше почисти мои тран-зис-торы 🪛🔧',
               'Рамамба Хару Мамбуру 🤪')
    update.message.reply_text(random.choice(answers))


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
    """Ответ на нажатие кнопки "Котика хочу 🐈"."""
    button = ReplyKeyboardMarkup([[LETS_PLAY_BTN], [NEXT_TIME_BTN]], resize_keyboard=True)
    update.message.reply_text(text='Ш.И.К.А.Р.Н.-О любит котиков 😻 Кыс-кыс-кыс!', reply_markup=ReplyKeyboardRemove())
    time.sleep(1)
    update.message.reply_photo(get_new_cat_image(update))
    time.sleep(1)
    update.message.reply_text(random.choice(txt.SHOW_CAT_TEXT))
    time.sleep(1)
    update.message.reply_text('Котики это хо-рошо. А как насчёт переки-нуться в кости? 😉', reply_markup=button)


def some_song(update, _):
    """Ответ на нажатие кнопки "Спой песенку 🎤"."""
    song = random.choice((txt.SONG_1, txt.SONG_2, txt.SONG_3,
                          txt.SONG_4, txt.SONG_5, txt.SONG_6))
    button = ReplyKeyboardMarkup([[HANDS_UP_BTN], [MORE_TALANTS_BTN]],
                                 resize_keyboard=True)
    update.message.reply_text(text=song, reply_markup=ReplyKeyboardRemove())
    time.sleep(1.5)
    update.message.reply_text(random.choice(txt.SOME_SONG_TEXT), reply_markup=button)


def song_reaction(update, _):
    """Ответ на фразы "Я вообще Руки Вверх люблю 🙌" и
    "А какие у тебя ещё таланты 😏"."""
    if update.message.text == HANDS_UP_BTN:
        button = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        text = 'Хорошо хоть не Ногу Свело 🦵'
    else:
        button = ReplyKeyboardMarkup([[SURPRISE_ME_BTN]], resize_keyboard=True)
        text = ('Силой электронно-вычислитель-ной мысли '
                'могу угадать день твоего ро-ждения 🧙🏻')
    update.message.reply_text(text=text, reply_markup=button)


def birthday_init(update, _):
    """Ответ на нажатие кнопки "А ну-ка, удиви! 😐"."""
    button = ReplyKeyboardMarkup([[NOT_STUPID_BTN], [STUPID_BTN]],
                                 resize_keyboard=True)
    update.message.reply_text(text='Нужно будет немножко по-считать. Возьми кальку-лятор. '
                                   'Надеюсь, ты умеешь им поль-зоваться? 🤭',
                              reply_markup=button)
    return BIRTH_1


def cancel_or_birthday_1(update, _):
    """Ответ на фразы "Я тупица... 😢" и "Я тебе не тупица! 😤"."""
    if update.message.text == STUPID_BTN:
        button = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        update.message.reply_text(text='А я сразу понял, что соображал-ка у тебя не очень 🙄\n'
                                       'Ну ничего. Осознание - первый путь к ис-правлению!\n'
                                       'Начни со счётных пало-чек... 🦧',
                                  reply_markup=button)
        return ConversationHandler.END
    else:
        button = ReplyKeyboardMarkup([[DONE_NEXT_BTN]], resize_keyboard=True)
        update.message.reply_text(text='Вот и проверим.\nДействуй со-гласно '
                                       'моим указа-ниям ☝️\n', reply_markup=ReplyKeyboardRemove())
        time.sleep(1.5)
        update.message.reply_text(text='Первым де-лом умножь число своего ро-ждения на 2 ☑️\n'
                                       'К ре-зультату прибавь 5 ☑️',
                                       reply_markup=button)
        return BIRTH_2


def birthday_2(update, _):
    """Ответ на нажатие кнопки "Сделано ✔️ Давай дальше"."""
    button = ReplyKeyboardMarkup([[MATH_BAD_BTN]], resize_keyboard=True)
    if update.message.text == DONE_NEXT_BTN:
        update.message.reply_text(text='Полу-ченное число умножь на 50 ☑️\nЗатем прибавь поряд-ковый'
                                       ' номер месяца своего ро-ждения.\n'
                                       'На-пример, январь - 1ый, декабрь - 12ый ☑️',
                                  reply_markup=ReplyKeyboardRemove())
        time.sleep(1.5)
        update.message.reply_text(text='Ну как? Твой про-цессор ещё не пере-грелся? 🤯\n'
                                       'Термопасту поме-нять не нужно?',
                                  reply_markup=button)
        return BIRTH_3
    else:
        update.message.reply_text(text='Введёшь число, когда я ска-жу 🤦🏻‍♂️\nВнизу есть кнопка...')


def birthday_3(update, _):
    """Ответ на нажатие кнопки "Математика явно не моё 😔"."""
    if update.message.text == MATH_BAD_BTN:
        update.message.reply_text(text='Со-берись, тряпка! 😠 Больше ничего счи-тать не нужно.\n',
                                  reply_markup=ReplyKeyboardRemove())
        time.sleep(1.5)
        update.message.reply_text(text='Перепроверь, что посчитано без ошибок 🤓\n'
                                       'Если всё верно - напиши число, кото-рое у тебя по-лучилось.')
        return BIRTH_4
    else:
        update.message.reply_text(text='Не нужно сейчас вводить число 🤦🏻‍♂️\nВнизу есть кнопка...')


def birthday_4(update, _):
    """Ответ на введённое число."""
    button = ReplyKeyboardMarkup([[EXTRASENS_BTN], [NOT_MY_BIRTH_BTN]],
                                 resize_keyboard=True)
    MONTHS = {1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля', 5: 'мая',
              6: 'июня', 7: 'июля', 8: 'августа', 9: 'сентября', 10: 'октября',
              11: 'ноября', 12: 'декабря'}
    result = int(update.message.text) - 250
    day = result // 100
    month = MONTHS.get(result % 100)
    if not 0 < day <= 31 or month is None:
        update.message.reply_text('Перепро-верь результат. Где-то ошибка ☝️')
        return
    update.message.reply_text(text='Барабанная дробь... 🥁')
    time.sleep(1.5)
    update.message.reply_text(text=f'День твоего рождения ⚜️ {day} {month} ⚜️',
                              reply_markup=button)
    if str(result) == dt.date.today().strftime('%d%m'):
        time.sleep(1.5)
        update.message.reply_text(text='Так это же сегодня!\nПо-здравляю с Днём Варенья!\n'
                                       'Расти большой, не будь ла-пшой 🥳🎊🎉')
    return BIRTH_5


def birthday_finish(update, _):
    """Ответ на фразы "Круто! Ты экстрасенс 😲" и "Неа, неверно! 🤨"."""
    button = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
    if update.message.text == EXTRASENS_BTN:
        text = ('Я знаю, я крутой 😎\nС тебя 100$ 💵\n'
                'Пе-реведи на мой электрон-ный кошелёк')
    else:
        text = ('Да ты просто счи-тать не умеешь 🤦🏻‍♂️\nА ещё говорят '
                'человек - вершина эволюции. Ну-ну... 🤔')
    update.message.reply_text(text=text, reply_markup=button)
    return ConversationHandler.END


def birth_fallback(update, _):
    """Ответ на любой неопознанный текст внутри диалога ДР."""
    update.message.reply_text(text='Так дело не пойдёт...\nДавай, со-'
                                   'средоточься и действуй по инструк-ции 🧐')


def show_anecdote(update, _):
    """Ответ на нажатие кнопки "Расскажи анекдот 😃"."""
    try:
        response = requests.get('http://anekdotme.ru/random/')
        # С помощью парсера получаем HTML-код страницы
        page_html = BeautifulSoup(response.text, 'html.parser')
        # Из HTML-кода страницы выбираем все объекты class='anekdot_text',
        # получаем список. Берём первый объект из списка и получаем его текст.
        anecdote = page_html.select('.anekdot_text')[0].get_text()
        text = ('Ш.И.К.А.Р.Н.-О знает много а-нек-до-тов. Вот:', anecdote,
                'Аха-ха! Мой процессор сейчас лопнет от смеха 🤣')
        button = ReplyKeyboardMarkup([[SO_SO_BTN], [BRAVO_BTN]],
                                     resize_keyboard=True)
        for phrase in text:
            update.message.reply_text(phrase, reply_markup=ReplyKeyboardRemove() if phrase != text[-1] else button)
            time.sleep(1.5)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        button = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        update.message.reply_text(text='Дол-баные вышки 5G. Они жгут мои микро-схемы 😕\n'
                                       'Расскажу в сле-дующий раз...')


def bravo_or_so_so(update, _):
    """Ответ на фразы "Ну такое себе 🤨" и "Браво! Это гениально 🤣"."""
    button = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
    if update.message.text == BRAVO_BTN:
        text = ('Молодец! Возьми с полки пиро-жок 🥯', 'Ещё бы! Я учил-ся у самого '
                'Дроботенко 😉', 'Смотри, чтоб пу-пок от смеха не развя-зался 🙈')
    else:
        text = ('У тебя просто нет чу-вства юмора 😤', 'Это до тебя дол-го доходит. '
                'Как до жира-фа 🦒', 'Иди смотри Смехопанора-му тогда 😠')
    update.message.reply_text(text=random.choice(text), reply_markup=button)


def what_are_you(update, _):
    """Ответ на нажатие кнопки "Да что ты такое 🤨"."""
    button = ReplyKeyboardMarkup([[HAVE_MERCY_BTN]], resize_keyboard=True)
    for text in txt.AWESOM_O_STORY[:-1]:
        update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
        time.sleep(1)
    update.message.reply_text(txt.AWESOM_O_STORY[-1], reply_markup=button)


def have_mercy_answer(update, _):
    """Ответ на нажатие кнопки "О, нет! Ш.И.К.А.Р.Н.-О, пощади 😨🙏"."""
    button = ReplyKeyboardMarkup([[KOMBIKORM_BTN], [NO_FUNNY_BTN]],
                                 resize_keyboard=True)
    update.message.reply_text(text='Расслабься! Ш.И.К.А.Р.Н.-О пошутил\nБуду кормить тебя '
                                   'ком-бикормом.\nИли что вы там еди-те? 😎',
                              reply_markup=button)


def no_funny_or_kombikorm(update, _):
    """Ответ на фразы "Очень смешно 😤" и "Комбикорм! Ммм... Вкуснятина 😋"."""
    button = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
    if update.message.text == KOMBIKORM_BTN:
        text = txt.DOSIER
    else:
        text = txt.NO_FUNNY
    for phrase in text[:-1]:
        update.message.reply_text(phrase, reply_markup=ReplyKeyboardRemove())
        time.sleep(1.5)
    update.message.reply_text(text[-1], reply_markup=button)


def secret_dossier(update, _):
    """Ответ на слово "Фалафель"."""
    button = ReplyKeyboardMarkup([[RED_BTN]], resize_keyboard=True)
    for text in txt.DOSSIER_TEXT[:-1]:
        update.message.reply_text(text, reply_markup=ReplyKeyboardRemove())
        time.sleep(2)
    update.message.reply_text(text=txt.DOSSIER_TEXT[-1], reply_markup=button)
    return FALAFEL


def cancel_secret_dossier(update, _):
    """Ответ на нажатие кнопки "Красная кнопка 🔴"."""
    button = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
    for text in txt.SELFDESTRUCTION[:-1]:
        update.message.reply_text(text=text)
        time.sleep(1.5)
    update.message.reply_text(txt.SELFDESTRUCTION[-1], reply_markup=button)
    return ConversationHandler.END


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


def bad_command(update, _):
    """Стандартный ответ в режиме диалога Фалафель."""
    update.message.reply_text(text='Несуществующая команда 🚫')


def show_hidden_phrases(update, _):
    """Реакция на команду /hidden - отобразить фразы-пасхалки для бота."""
    update.message.reply_text(
        '*** Пасхалки ***\n🔸 Они убили Кенни\n🔸 Притворись ноликом\n'
        '🔸 Эрик Картман\n🔸 Марклар'
    )


def answer_hidden_phrases(update, _):
    """Ответ на фразы-пасхалки."""
    phrase_answer = {'Марклар': txt.MARKLAR_ANSWER,
                     ZERO: 'Может ещё крес-тиком начать вышивать? 🙄',
                     CARTMAN: txt.CARTMAN,
                     KENNY: 'Сволочи! 😡'}
    for phrase, answer in phrase_answer.items():
        if re.match(phrase, update.message.text):
            update.message.reply_text(text=answer)
            break


def no_play_or_game_rules(update, _):
    """Ответ на кнопки "В другой раз 🙅🏻‍♂️" и "Изи! Доставай 🤠"."""
    if update.message.text == NEXT_TIME_BTN:
        main = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        update.message.reply_text('Как знаешь. Угова-ривать не буду 😼', reply_markup=main)
    else:
        global game_stat, PLAYER, bot_wins, user_wins, user_dice_counter, user_dice_result, triple_bet_bot, triple_bet_user
        bot_wins, user_wins, user_dice_counter, user_dice_result, triple_bet_bot, triple_bet_user = [0] * 6
        PLAYER = update.message.chat.full_name
        init_stat = dict(wins=0, dry_wins=0, triple_bet=0, double_six=0, double_one=0, made_bet=0, guessed_bet=0)
        game_stat = {'BOT': init_stat, f'{PLAYER}': init_stat.copy()}
        print(game_stat)
        button = ReplyKeyboardMarkup([[BEGIN_BTN], [HALL_OF_FAME_BTN]], resize_keyboard=True)
        for text in txt.RULES_DICE:
            update.message.reply_text(text, reply_markup=button if text == txt.RULES_DICE[-1] else ReplyKeyboardRemove())
            time.sleep(1)
        return BOT_DICE


def bot_bet_roll_dice(update, _):
    """Ответ на кнопки "Поехали 👌", "Твой ход 👆", "Хочу реванш 🥊" и "Дам тебе отыграться 😙"."""
    cancel = ReplyKeyboardMarkup([[NO_MORE_GAME_BTN]], resize_keyboard=True)
    choice = ReplyKeyboardMarkup([[REVENGE_BTN], [CATS_TRAIN_BTN]], resize_keyboard=True)
    global bot_wins, user_wins, triple_bet_bot, triple_bet_user
    if update.message.text == REVENGE_BTN:
        update.message.reply_text('Не любишь проигры-вать? Ну-ну!\nПродолжаем 😎'); time.sleep(1)
    if update.message.text == WIN_BACK_BTN:
        update.message.reply_text('Ну всё - шутки кончились!\nБольше под-даваться не буду 😠'); time.sleep(1)
    bet_1, bet_2 = random.randint(3, 11), random.randint(3, 11)
    while bet_2 == bet_1:
        bet_2 = random.randint(3, 11)
    update.message.reply_text(f'Я поставлю на {bet_1} и {bet_2} ✍️', reply_markup=ReplyKeyboardRemove())
    time.sleep(1)
    game_stat['BOT']['made_bet'] += 1; triple_bet_bot += 1
    update.message.reply_text('Бросаю ко-сти... ✊')
    result = 0
    for _ in (1, 2):
        value = update.message.reply_dice()['dice']['value']
        result += value
        time.sleep(3)
    update.message.reply_text(f'Мой ре-зультат:  {result} ❗️', reply_markup=cancel)
    time.sleep(1)
    if result not in (bet_1, bet_2): triple_bet_bot = 0
    if result in (bet_1, bet_2, 2, 12):
        if result == 2:
            update.message.reply_text('О, нет! 😱 Две еди-нички. Минус балл 😭')
            game_stat['BOT']['double_one'] += 1
            if bot_wins > 0: bot_wins -= 1
        elif result == 12:
            update.message.reply_text('Я со-рвал Джек пот 🥳\nДве шестёрки! Получаю балл 👏')
            game_stat['BOT']['double_six'] += 1
            bot_wins += 1
        else:
            update.message.reply_text('Ура! Мне повезло 😄\nЯ вы-играл в этом раунде 🦾')
            game_stat['BOT']['guessed_bet'] += 1
            bot_wins += 1
        if bot_wins == user_wins:
            update.message.reply_text(f'Счёт {bot_wins} : {user_wins}\nУ нас ничья 🍻')
        else:
            update.message.reply_text(
                f'Счёт {bot_wins} : {user_wins}\n' + ('Я впереди 🤘' if bot_wins > user_wins else 'В твою пользу 😕'))
        if bot_wins == 3:
            time.sleep(1.5)
            update.message.reply_text(
                f'Финальный ре-зультат: 💫 {bot_wins} : {user_wins} 💫' + ('  Всухую! Как котёнка 🙈' if user_wins == 0 else '') +
                '\n\n' + 'Ехууу 🥳 Победа за мной!\nУчись у мастера, салага 😎',
                reply_markup=choice)
            game_stat['BOT']['wins'] += 1
            if user_wins == 0: game_stat['BOT']['dry_wins'] += 1
            if triple_bet_bot == 3: game_stat['BOT']['triple_bet'] += 1
            time.sleep(1.5)
            update.message.reply_text(func.dice_game_stat(game_stat, PLAYER))
            bot_wins, user_wins, triple_bet_bot, triple_bet_user = 0, 0, 0, 0
            return BOT_DICE
    else:
        update.message.reply_text('Не угадал 😔\nЛадно, в следую-щий раз по-везёт...')
    time.sleep(1)
    update.message.reply_text('Твоя оче-редь. Делай ставку ☝️ и бросай ко-сти.', reply_markup=cancel)
    return USER_BET


def user_bets(update, _):
    """Ответ на ввод пользователем двух чисел перед бросками кубиков."""
    global user_bet_1, user_bet_2, triple_bet_user
    button = ReplyKeyboardMarkup([['🎲']], resize_keyboard=True)
    user_bet_1, user_bet_2 = map(int, (update.message.text).split())
    if user_bet_1 == user_bet_2:
        update.message.reply_text('Числа должны быть раз-ными! Это в твоих же инте-ресах 🤦🏻‍♂️')
    else:
        update.message.reply_text('Принято! Бросай ко-сти 🎲', reply_markup=button)
        game_stat[f'{PLAYER}']['made_bet'] += 1; triple_bet_user += 1
        return USER_DICE


def user_roll_dice(update, _):
    """Подсчёт результата бросков кубика игроком."""
    your_turn = ReplyKeyboardMarkup([[YOUR_TURN_BTN]], resize_keyboard=True)
    choice = ReplyKeyboardMarkup([[WIN_BACK_BTN], [EAT_CORN_BTN]], resize_keyboard=True)
    global user_dice_counter, user_dice_result, bot_wins, user_wins, triple_bet_user, triple_bet_bot
    points = update.message.dice['value']
    user_dice_counter += 1
    user_dice_result += points
    if user_dice_counter == 1:
        time.sleep(2)
        update.message.reply_text('Бросай ещё 👉')
        return
    time.sleep(3)
    update.message.reply_text(f'Твой результат:  {user_dice_result} ❗️', reply_markup=your_turn)
    if user_dice_result not in (user_bet_1, user_bet_2): triple_bet_user = 0
    if user_dice_result in (user_bet_1, user_bet_2, 2, 12):
        if user_dice_result == 2:
            update.message.reply_text('Ха! Две дырки 🙈 Не повез-ло. Минус балл.')
            game_stat[f'{PLAYER}']['double_one'] += 1
            if user_wins > 0: user_wins -= 1
        elif user_dice_result == 12:
            update.message.reply_text('Ничего себе! Две шестёрки 😳 Получаешь балл.')
            game_stat[f'{PLAYER}']['double_six'] += 1
            user_wins += 1
        else:
            update.message.reply_text('Удача на твоей сто-роне.\nТы угадал в этот раз 😏')
            game_stat[f'{PLAYER}']['guessed_bet'] += 1
            user_wins += 1
        if user_wins == bot_wins:
            update.message.reply_text(f'Счёт {bot_wins} : {user_wins}\nУ нас ничья 🍻')
        else:
            update.message.reply_text(
                f'Счёт {bot_wins} : {user_wins}\n' + ('Я впереди 🙃' if bot_wins > user_wins else 'В твою пользу 😒'))
        if user_wins == 3:
            time.sleep(1.5)
            update.message.reply_text(
                f'Финальный ре-зультат: 💫 {user_wins} : {bot_wins} 💫' + ('  Всухую. Читер! 😠' if bot_wins == 0 else '') +
                '\n\n' + 'Твоя победа!\nМожешь пола-комиться ку-курузкой 🌽\nНо не за-знавайся - тебе просто повез-ло 😈\nПонимаешь, да?',
                reply_markup=choice)
            game_stat[f'{PLAYER}']['wins'] += 1
            if bot_wins == 0: game_stat[f'{PLAYER}']['dry_wins'] += 1
            if triple_bet_user == 3: game_stat[f'{PLAYER}']['triple_bet'] += 1
            time.sleep(1.5)
            update.message.reply_text(func.dice_game_stat(game_stat, PLAYER))
            bot_wins, user_wins, triple_bet_user, triple_bet_bot = 0, 0, 0, 0
    else:
        update.message.reply_text('Не угадал 🤷🏻‍♂️ Ничего, бывает...\nПродолжаем ве-селиться 😉', reply_markup=your_turn)
    user_dice_counter, user_dice_result = 0, 0
    return BOT_DICE


def cancel_game(update, _):
    """Ответ на кнопки "Больше не хочу играть 😐", "Точно! Хватит 🖐",
    "Пойду грызть свою кукурузку 😋" и "Пойду тренироваться. На кошках 🐈"."""
    confirm = ReplyKeyboardMarkup([[ENOUGH_BTN], ['Нет, я передумал 🙃']], resize_keyboard=True)
    main = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
    text = update.message.text
    if text == NO_MORE_GAME_BTN:
        update.message.reply_text('Точно не хочешь про-должать? 🧐', reply_markup=confirm)
    if text == CATS_TRAIN_BTN or text == EAT_CORN_BTN or text == ENOUGH_BTN:
        update.message.reply_text('Ладно. За-хочешь ещё сыграть - ты знаешь, где меня най-ти 😼',
                                  reply_markup=main)
        return ConversationHandler.END


def show_hall_of_fame(update, _):
    """Ответ на нажатие кнопки "Покажи зал славы игроков 🤩"."""
    update.message.reply_text('🌟  З А Л    С Л А В Ы  🌟\n'
                              'Вот они - лучшие игроки, борю-щиеся за звание Абсолютного чем-пиона!\n'
                              'Не каждый сможет оказать-ся на вершине рейтинга, но любой может ис-пытать удачу 🍀💪')
    update.message.reply_text('⚠️ Для того, чтобы войти в трой-ку лидеров, необходимо оты-грать хотя бы 5 раундов ✅',
                              reply_markup=ReplyKeyboardMarkup([[BEGIN_BTN]], resize_keyboard=True))
    time.sleep(1)
    rating, last_champion = func.hall_of_fame()
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
            rest += f'{person[-1]}' + f'  >  осталось сыграть:  {5 - person[5]}\n' if person[5] < 5 else '  🔝\n'
    if champion:
        if champ_name != last_champion['name']:
            today = dt.date.today().strftime('%d.%m.%Y г.')
            db = shelve.open('statistic')
            last_champ = db['DICE_CHAMPION']
            last_champ['name'] = champ_name
            last_champ['date'] = today
            db['DICE_CHAMPION'] = last_champ
            db.close()
            champion_from_date = today + '\n'
        else:
            champion_from_date = last_champion['date'] + '\n'
    update.message.reply_text(champion + ('получил титул ' if champion else '') + (champion_from_date if champion else '') + places + rest)
    for (share_of_wins, average_dice_to_win, share_of_guessed_bet, dry_wins, triple_bet, games, wins, looses,
         made_bet, guessed_bet, double_six, share_of_double_six, double_one, share_of_double_one,
         share_of_dry_wins, share_of_triple_bet, name) in rating:
        update.message.reply_text(
            f'🔸 {name} 🔸  Сыграно раундов:  {games}\nПобеды:  {wins} ~ {-share_of_wins:.1f}%    Поражения:  {looses}\n'
            f'Победы "всухую" (счёт 3:0):  {-dry_wins} ~ {share_of_dry_wins:.1f}%\n'
            f'Победы "без шансов" (угаданы подряд три ставки):  {-triple_bet} ~ {share_of_triple_bet:.1f}%\n'
            f'В среднем бросков для победы:  {average_dice_to_win:.1f}\nВсего ставок:  {made_bet}  Угадано:  {guessed_bet} ~ {-share_of_guessed_bet:.1f}%\n'
            f'6️⃣6️⃣ выпадали:  {double_six} ~ {share_of_double_six:.1f}%\n1️⃣1️⃣ выпадали:  {double_one} ~ {share_of_double_one:.1f}%\n'
        )
    update.message.reply_text('Ну что, готов(а) сместить текуще-го чемпиона? Кажется, он уже засиделся... 🤫')
    return BOT_DICE


def place_bet(update, _):
    """Стандартный ответ на этапе ставки игрока."""
    update.message.reply_text('Тебе нужно сде-лать ставку 🤨\nВведи два разных числа через про-бел:\nминимум 3️⃣, максимум 1️⃣1️⃣.')


def go_on(update, _):
    """Стандартный ответ на этапе бросков кубика игроком."""
    update.message.reply_text('Тебе ну-жно бросить кубик. Сосре-доточься 🤨')


def dice_fallback(update, _):
    """Стандартный ответ внутри диалога игры в кости."""
    update.message.reply_text('Идёт игра. Не отвле-кайся 🤨')


def main():
    """Основная функция запуска бота."""
    updater = Updater(token=TOKEN)
    handler = updater.dispatcher.add_handler
    handler(CommandHandler('start', wake_up))
    birthday_сonversation = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(SURPRISE_ME_BTN), birthday_init)],
        states={
            BIRTH_1: [MessageHandler(Filters.regex(STUPID_BTN + OR + NOT_STUPID_BTN), cancel_or_birthday_1)],
            BIRTH_2: [MessageHandler(Filters.regex(DONE_NEXT_BTN + OR + r'^\d{1,2}$'), birthday_2)],
            BIRTH_3: [MessageHandler(Filters.regex(MATH_BAD_BTN + OR + r'^\d{3,4}$'), birthday_3)],
            BIRTH_4: [MessageHandler(Filters.regex(r'^\d{3,4}$'), birthday_4)],
            BIRTH_5: [MessageHandler(Filters.regex(NOT_MY_BIRTH_BTN + OR + EXTRASENS_BTN), birthday_finish)],
        },
        fallbacks=[MessageHandler(Filters.all, birth_fallback)]
    )
    handler(birthday_сonversation)
    falafel_сonversation = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^Фалафель$'), secret_dossier)],
        states={
            FALAFEL: [MessageHandler(Filters.regex(HAVE_DOSSIERS), show_secret_dossier),
                      MessageHandler(Filters.regex(RED_BTN), cancel_secret_dossier)],
        },
        fallbacks=[MessageHandler(Filters.all, bad_command)]
    )
    handler(falafel_сonversation)
    dice_game_сonversation = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(NEXT_TIME_BTN + OR + LETS_PLAY_BTN), no_play_or_game_rules)],
        states={
            BOT_DICE: [MessageHandler(Filters.regex(BEGIN_BTN + OR + YOUR_TURN_BTN + OR + REVENGE_BTN + OR + WIN_BACK_BTN),
                                      bot_bet_roll_dice),
                       MessageHandler(Filters.regex(CATS_TRAIN_BTN + OR + EAT_CORN_BTN), cancel_game),
                       MessageHandler(Filters.regex(HALL_OF_FAME_BTN), show_hall_of_fame)],
            USER_BET: [MessageHandler(Filters.regex(BET_RANGE), user_bets),
                       MessageHandler(Filters.regex(NO_MORE_GAME_BTN + OR + ENOUGH_BTN), cancel_game),
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
    handler(MessageHandler(Filters.regex(SO_SO_BTN + OR + BRAVO_BTN), bravo_or_so_so))
    handler(MessageHandler(Filters.regex(SONG_BTN), some_song))
    handler(MessageHandler(Filters.regex(HANDS_UP_BTN + OR + MORE_TALANTS_BTN), song_reaction))
    handler(MessageHandler(Filters.regex(WHAT_ARE_YOU_BTN), what_are_you))
    handler(MessageHandler(Filters.regex(HAVE_MERCY_BTN), have_mercy_answer))
    handler(MessageHandler(Filters.regex(KOMBIKORM_BTN + OR + NO_FUNNY_BTN), no_funny_or_kombikorm))
    handler(MessageHandler(Filters.regex(HIDDEN_PHRASES), answer_hidden_phrases))
    handler(MessageHandler(Filters.all & ~Filters.command, default_answer))
    handler(CommandHandler('hidden', show_hidden_phrases))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    # start_logging()
    main()
