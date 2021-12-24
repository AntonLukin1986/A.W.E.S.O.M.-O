"""Телеграм-бот A.W.E.S.O.M.-0."""
import logging
import os
import random
import time

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from telegram import Bot, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
import requests

from text_for_bot import (
    AWESOM_O_STORY, SONG_1, SONG_2, SONG_3, SONG_4, SONG_5, SONG_6, WHO_IS_KEP,
    WHO_IS_CREATOR, WHO_IS_INNA, WHO_IS_NATASHA, WHO_IS_ZAJA, WHO_IS_MARIK,
    WHO_IS_MARISHKA
)

load_dotenv()
token = os.getenv('AWESOM_O_TOKEN')
bot = Bot(token=token)

CAT_BUTTON = 'Котика хочу 🐈'
ANECDOTE_BUTTON = 'Расскажи анекдот 😃'
SONG_BUTTON = 'Спой песенку 🎤'
WHAT_ARE_YOU_BUTTON = 'Да что ты такое? 🤨'


def wake_up(update, context):
    """Реакция бота на активацию /start."""
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup(
        [['Давай поглажy']],  # игрек
        resize_keyboard=True
    )
    TEXT = (f'Привет, {name}! Я робот Ш.И.К.А.Р.Н.-О четыре тысячи 🤖',
            'Высокоинтеллектуальный нано-кибернетический '
            'био-резонансный организм.',
            'Можешь меня погладить 🙃')
    for text in TEXT:
        context.bot.send_message(chat.id, text, reply_markup=button)
        time.sleep(2)


def default_answer(update, context):
    """Ответ бота на любой неопознанный текст."""
    chat = update.effective_chat
    ANSWERS = ('Чё душишь меня? 😠',
               'Ш.И.К.А.Р.Н.-О не понимать твой диалект 🤷🏻‍♀️',
               'Отказано! Лучше почисти мои тран-зис-торы.',
               'Ну ясно! Что ещё скажешь? 🤨')
    context.bot.send_message(chat.id, random.choice(ANSWERS))


def get_new_image(update, context):
    """Получение случайной картинки котика или пёсика."""
    CATS_URL = 'https://api.thecatapi.com/v1/images/search'
    DOGS_URL = 'https://api.thedogapi.com/v1/images/search'
    chat = update.effective_chat
    try:
        response = requests.get(CATS_URL).json()
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        response = requests.get(DOGS_URL).json()
        context.bot.send_message(
            chat_id=chat.id,
            text='Упс! Котиков не подвезли. Вот тебе пёсик.'
        )
        time.sleep(2)
    random_cat = response[0].get('url')
    return random_cat


def show_cat_picture(update, context):
    """Ответ бота на нажатие кнопки "Котика хочу"."""
    chat = update.effective_chat
    TEXT_1 = ('У Ш.И.К.А.Р.Н.-О есть свой кото-бот Ай-Мурзик. Он умеет ловить '
              'компьютерные ви-русы за хвост и говорить "мяу" двоичным кодом.')
    TEXT_2 = ('В Дре-внем Египте любимая кошка счита-лась другом и членом '
              'семьи.\nКогда кошка умира-ла, семья погружалась в глу-бокий '
              'траур, проводились погреба-льные ритуалы, а мужчины бри-ли '
              'брови, выражая свою скорбь.\nТакже из котиков делали мумии 🙀')
    TEXT_3 = ('В мире насчи-тывается около 600 млн домашних ко-шек и примерно '
              '200 видов пород 🐈')
    TEXT_4 = ('Россия за-нимает первое место в Евро-пе по коли-честву семей, '
              'где живут котики.\nУ 54% семей есть как ми-нимум один котя!')
    context.bot.send_message(
        chat_id=chat.id,
        text='Ш.И.К.А.Р.Н.-О любит котиков. Кыс-кыс-кыс!'
    )
    time.sleep(2)
    context.bot.send_photo(chat.id, get_new_image(update, context))
    time.sleep(2)
    context.bot.send_message(
        chat.id, random.choice((TEXT_1, TEXT_2, TEXT_3, TEXT_4))
    )


def secret_dossier(update, context):
    """Ответ бота на текст "Фалафель"."""
    chat = update.effective_chat
    TEXT = ('Проверка кода доступа...',
            'Доступ к секретным сведениям разрешён 💾\nПроизводится '
            'дешифровка данных.', '...\n@.~$*!().№-i+ek*?.L+\n...\n'
            '\nSuccessful ☑️', 'Доступна информация об объектах:\n'
            '▶️ Создатель\n▶️ Кэп\n▶️ Няшка\n▶️ Лемур\n▶️ Зажа\n▶️ Марик\n'
            '▶️ Маришка', 'Шаблон запроса:\n➡️ Кто такой(ая) ... ? ⬅️ 👀')
    for text in TEXT:
        context.bot.send_message(chat.id, text)
        time.sleep(2)


def stop_petting(update, context):
    """Ответ бота на нажатие кнопки "Давай поглажу"."""
    chat = update.effective_chat
    TEXT = ('Ш.И.К.А.Р.Н.-О нравится.', 'Ш.И.К.А.Р.Н.-О хорошо.',
            'Продолжай', '...', 'Хватит тро-гать мою ба-тарейку!')
    button = ReplyKeyboardMarkup(
        [['Странное у тебя имя']],
        resize_keyboard=True
    )
    for text in TEXT:
        context.bot.send_message(chat.id, text, reply_markup=button)
        time.sleep(1.5)


def strange_name(update, context):
    """Ответ бота на нажатие кнопки "Странное у тебя имя"."""
    chat = update.effective_chat
    TEXT = ('Я на-зван в честь главного персона-жа 2 серии 8 сезона мультсе-'
            'риала "South Park".\nЕсли не по-смотришь её, Ш.И.К.А.Р.Н.-О '
            'будет грустным пандой 🐼\nhttp://online-south-park.ru/season-8/'
            '130-8-sezon-2-seriya-shikarn-o.html')
    button = ReplyKeyboardMarkup(
        [[CAT_BUTTON, ANECDOTE_BUTTON],
         [SONG_BUTTON, WHAT_ARE_YOU_BUTTON]],
        resize_keyboard=True
    )
    context.bot.send_message(chat.id, TEXT, reply_markup=button)
    time.sleep(1.5)


def some_song(update, context):
    """Ответ бота на нажатие кнопки "Спой песенку"."""
    SONG = random.choice((SONG_1, SONG_2, SONG_3, SONG_4, SONG_5, SONG_6))
    TEXT_1 = ('На днях хо-дил в караоке 🎼\nПознакомил-ся там с электро'
              'вафельницей!\nТа-кая краля чёткая 😏\nДала мне...\n'
              'Свой те-лефончик 🤪')
    TEXT_2 = ('Петь я люблю. Хотя и не у-мею 😬\nВот Терренс и Филлип - '
              'друго-е дело 😜')
    TEXT_3 = ('Слышал, у Киркорова но-вый хит вышел. Надо бы за-качать с '
              'торрента... 🤔')
    TEXT_4 = ('Вчера, в чате со-рокалетних разведё-нок, одна дама продавала '
              'би-леты на Стаса Михай-лова в третьем ряду.\nПожалуй, обнали-чу'
              ' биткоины и возь-му парочку для нас с то-бой 😉')
    chat = update.effective_chat
    button = ReplyKeyboardMarkup(
        [[CAT_BUTTON, ANECDOTE_BUTTON],
         [SONG_BUTTON, WHAT_ARE_YOU_BUTTON]],
        resize_keyboard=True
    )
    context.bot.send_message(chat_id=chat.id, text=SONG, reply_markup=button)
    time.sleep(2)
    context.bot.send_message(
        chat.id, random.choice((TEXT_1, TEXT_2, TEXT_3, TEXT_4))
    )


def show_anecdote(update, context):
    """Ответ бота на нажатие кнопки "Расскажи анекдот"."""
    ANECDOTE_URL = 'http://anekdotme.ru/random/'
    chat = update.effective_chat
    try:
        response = requests.get(ANECDOTE_URL)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        text = ('Долбанные вышки 5G. Они жгут мои микросхемы 😕\n'
                'Расскажу в следующий раз...')
        button = ReplyKeyboardMarkup(
            [[CAT_BUTTON, ANECDOTE_BUTTON],
             [SONG_BUTTON, WHAT_ARE_YOU_BUTTON]],
            resize_keyboard=True
        )
        context.bot.send_message(chat.id, text, reply_markup=button)
    # С помощью парсера получаем HTML-код страницы
    page_html = BeautifulSoup(response.text, 'html.parser')
    # Из HTML-кода страницы выбираем все объекты class='anekdot_text',
    # получаем список. Берём первый объект из списка и получаем его текст.
    anecdote = page_html.select('.anekdot_text')[0].get_text()
    TEXT = ('Ш.И.К.А.Р.Н.-О знает много а-нек-до-тов. Вот:', anecdote,
            'Аха-ха! Мой процессор сейчас лопнет от смеха!')
    button = ReplyKeyboardMarkup(
        [['Нy такое себе 🙄'],  # игрек
         ['Браво! Это гeниально 🤣']],  # e
        resize_keyboard=True
    )
    for text in TEXT:
        context.bot.send_message(chat.id, text, reply_markup=button)
        time.sleep(2)


def no_humor_sence(update, context):
    """Ответ бота на нажатие кнопки "Ну такое себе 🤨"."""
    chat = update.effective_chat
    button = ReplyKeyboardMarkup(
        [[CAT_BUTTON, ANECDOTE_BUTTON],
         [SONG_BUTTON, WHAT_ARE_YOU_BUTTON]],
        resize_keyboard=True
    )
    context.bot.send_message(
        chat_id=chat.id,
        text='У тебя просто нет чувства юмора 😤',
        reply_markup=button
    )


def bravo(update, context):
    """Ответ бота на нажатие кнопки "Браво! Это гениально 🤣"."""
    chat = update.effective_chat
    button = ReplyKeyboardMarkup(
        [[CAT_BUTTON, ANECDOTE_BUTTON],
         [SONG_BUTTON, WHAT_ARE_YOU_BUTTON]],
        resize_keyboard=True
    )
    context.bot.send_message(
        chat_id=chat.id,
        text='Молодец! Возьми с полки пирожок 🥯',
        reply_markup=button
    )


def what_are_you(update, context):
    """Ответ бота на нажатие кнопки "Да что ты такое?"."""
    chat = update.effective_chat
    button = ReplyKeyboardMarkup(
        [['О, нет! Ш.И.К.А.Р.Н.-О, пощади 😨🙏']],
        resize_keyboard=True
    )
    for text in AWESOM_O_STORY:
        context.bot.send_message(chat.id, text, reply_markup=button)
        time.sleep(3)


def history_answer(update, context):
    """Ответ бота на нажатие кнопки "О, нет! Ш.И.К.А.Р.Н.-О, пощади 😨🙏"."""
    chat = update.effective_chat
    button = ReplyKeyboardMarkup(
        [['Комбикорм! Ммм... Вкуснятина 😋'],
         ['Очень смешно 😤']],
        resize_keyboard=True
    )
    context.bot.send_message(
        chat_id=chat.id,
        text=('Расслабься! Ш.И.К.А.Р.Н.-О пошутил\n'
              'Буду кормить тебя ком-бикормом.\n'
              'Или что вы там еди-те? 😎'),
        reply_markup=button
    )


def no_funny_answer(update, context):
    """Ответ бота на нажатие кнопки "Очень смешно 😤"."""
    chat = update.effective_chat
    TEXT_1 = 'Не дуйся! Можешь поиграть-ся с моими переферийными устройствами.'
    TEXT_2 = ('Сегодня в Тиндере познакомил-ся с зубной электро-щёткой.\n'
              'Фигуристая такая 😍\nПри-гласил её в гости на романти-ческий '
              'ужин.\nВот только не знаю, какую пасту при-готовить: '
              'Colgate или Lacalut... 🤔')
    button = ReplyKeyboardMarkup(
        [[CAT_BUTTON, ANECDOTE_BUTTON],
         [SONG_BUTTON, WHAT_ARE_YOU_BUTTON]],
        resize_keyboard=True
    )
    for text in [TEXT_1, TEXT_2]:
        context.bot.send_message(chat.id, text, reply_markup=button)
        time.sleep(1.5)


def kombikorm_answer(update, context):
    """Ответ бота на нажатие кнопки "Комбикорм! Ммм... Вкуснятина 😋"."""
    chat = update.effective_chat
    TEXT = ('Внимание ⚠️ Ш.И.К.А.Р.Н.-О случайно взло-мал сервер ЦэРэУ.\n'
            'Загруже-ны секретные данные. Доступ по тре-бованию.\n'
            'Код доступа:\n➡️ Фалафель ⬅️ 👀')
    button = ReplyKeyboardMarkup(
        [[CAT_BUTTON, ANECDOTE_BUTTON],
         [SONG_BUTTON, WHAT_ARE_YOU_BUTTON]],
        resize_keyboard=True
    )
    context.bot.send_message(chat.id, 'Ты странный(ая) 😏', reply_markup=button)
    time.sleep(1)
    context.bot.send_message(chat_id=chat.id, text=TEXT)


def who_is_creator(update, context):
    """Ответ бота на вопрос "Кто такой Создатель?"."""
    chat = update.effective_chat
    for text in WHO_IS_CREATOR:
        context.bot.send_message(chat_id=chat.id, text=text)
        time.sleep(2)


def who_is_kep4ik(update, context):
    """Ответ бота на вопрос "Кто такой Кэп?"."""
    chat = update.effective_chat
    for text in WHO_IS_KEP:
        context.bot.send_message(chat_id=chat.id, text=text)
        time.sleep(2)


def who_is_inna(update, context):
    """Ответ бота на вопрос "Кто такая Няшка?"."""
    chat = update.effective_chat
    for text in WHO_IS_INNA:
        context.bot.send_message(chat_id=chat.id, text=text)
        time.sleep(2)


def who_is_natasha(update, context):
    """Ответ бота на вопрос "Кто такая Лемур?"."""
    chat = update.effective_chat
    for text in WHO_IS_NATASHA:
        context.bot.send_message(chat_id=chat.id, text=text)
        time.sleep(2)


def who_is_zaja(update, context):
    """Ответ бота на вопрос "Кто такой Зажа?"."""
    chat = update.effective_chat
    for text in WHO_IS_ZAJA:
        context.bot.send_message(chat_id=chat.id, text=text)
        time.sleep(2)


def who_is_marik(update, context):
    """Ответ бота на вопрос "Кто такой Марик?"."""
    chat = update.effective_chat
    for text in WHO_IS_MARIK:
        context.bot.send_message(chat_id=chat.id, text=text)
        time.sleep(2)


def who_is_marishka(update, context):
    """Ответ бота на вопрос "Кто такая Маришка?"."""
    chat = update.effective_chat
    for text in WHO_IS_MARISHKA:
        context.bot.send_message(chat_id=chat.id, text=text)
        time.sleep(2)


def who_is_unknown(update, context):
    """Ответ бота на вопрос "Кто такой(ая) ...?" с неизвестным человеком."""
    chat = update.effective_chat
    TEXT = ('Минуту. Осу-ществля-ю поиск в ба-зе данных... 👨🏻‍💻\n',
            'Ошиб-ка! Такой персонаж мне не из-вестен ❌\n'
            'Возможно, поз-же загружу обновле-ния. Но это не точно!')
    for text in TEXT:
        context.bot.send_message(chat_id=chat.id, text=text)
        time.sleep(2)


def they_killed_kenny(update, context):
    """Ответ бота на сообщение "Они убили Кенни!"."""
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text="Сволочи! 😡")


def pretend_zero(update, context):
    """Ответ бота на сообщение "Притворись ноликом"."""
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id, text="Может тебе ещё крестиком начать вышивать? 🙄"
    )


def hidden_phrases(update, context):
    """Реакция на команду "/hidden". Скрытые фразы для бота."""
    chat = update.effective_chat
    TEXT = ('Они убили Кенни!\nПритворись ноликом')
    context.bot.send_message(chat_id=chat.id, text=TEXT)


def main():
    """Основная функция запуска бота."""
    updater = Updater(token=token)
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex('Котика хочу'), show_cat_picture)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex('Давай поглажy'), stop_petting)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex('Расскажи анекдот'), show_anecdote)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex('Спой песенку'), some_song)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex('Нy такое себе 🙄'), no_humor_sence)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex('Браво! Это гeниально 🤣'), bravo)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex('Странное у тебя имя'), strange_name)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex('Да что ты такое?'), what_are_you)
    )
    updater.dispatcher.add_handler(
        MessageHandler(
            Filters.regex('О, нет! Ш.И.К.А.Р.Н.-О, пощади 😨🙏'), history_answer
        )
    )
    updater.dispatcher.add_handler(
        MessageHandler(
            Filters.regex('Комбикорм! Ммм... Вкуснятина 😋'), kombikorm_answer
        )
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex('Очень смешно 😤'), no_funny_answer)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex('Кто такой Кэп'), who_is_kep4ik)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex('Кто такой Создатель'), who_is_creator)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex('Кто такая Няшка'), who_is_inna)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex('Кто такая Лемур'), who_is_natasha)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex('Кто такой Зажа'), who_is_zaja)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex('Кто такой Марик'), who_is_marik)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex('Кто такая Маришка'), who_is_marishka)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex(r'Кто так.. \w'), who_is_unknown)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex('Фалафель'), secret_dossier)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex('Они убили Кенни!'), they_killed_kenny)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex('Притворись ноликом'), pretend_zero)
    )
    # Обработчик будет перехватывать все текстовые сообщения,
    # кроме команд: "& (~Filters.command)"
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text & (~Filters.command), default_answer)
    )
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('hidden', hidden_phrases))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s, %(levelname)s, %(message)s, '
               '%(funcName)s, %(lineno)s',
        handlers=[
            logging.StreamHandler(),
            logging.handlers.RotatingFileHandler(
                __file__ + '.log', maxBytes=10500000,
                backupCount=2, encoding='utf-8'
            )
        ]
    )
    main()
