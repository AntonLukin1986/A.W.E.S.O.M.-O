"""A.W.E.S.O.M.-0. Телеграм бот."""
import logging
import os
import random
import time

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from telegram import Bot, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

load_dotenv()

token = os.getenv('TELEGRAM_TOKEN')

bot = Bot(token=token)

FUNNY_STORY = (
    'Я явля-юсь продуктом вы-сокочастотной электронно-поло-вой\n'
    'связи электромясоруб-ки с тостером.\n'
    'Мой дедушка был про-стым советским радиоприём-ником "Океан-209".',
    'Однажды он поймал радиосиг-нал неизвестной вы-сокоразвитой '
    'космической цивили-зации Краб-пипл с плане-ты Марклар, '
    'в созвездии Усатого Бегемо-та.\n'
    'Дедушка поведал им о суще-ствовании нашей планеты и при-гласил '
    'маркларцев в гос-ти на свою предстоящую свадь-бу с кофеваркой '
    '(моей бабушкой).',
    'Через некоторое вре-мя первые представи-тели цивилизации Краб-'
    'пипл прибыли на Землю и ста-ли жить среди людей, вы-давая себя '
    'за зубные щётки.\nРа-спространившись по всей планете, '
    'маркларцы посели-лись в каждом доме и в каждой кварти-ре, '
    'у-становив контроль за всеми людь-ми.',
    'Со вре-менем маркларцы выяснили, что люди очень примитив-ные '
    'существа, так как многие смотрят по пят-ницам "Поле чудес", а '
    'не-которые даже подписаны на Бузову в Ин-стаграм.\nОкончатель-но '
    'же обесценило в их глазах че-ловеческий интеллект то, что люди '
    'регуляр-но используют ва-тные палочки для чистки ушей, хотя на '
    'каждой упаков-ке написано, что так делать не сле-дует!!!',
    'Задавшись целью порабо-тить землян, цивилизация Краб-пипл '
    'у-становила контроль над моими микросхема-ми и прокачала мою '
    'харизму и чу-вство юмора, чтобы я мог легко войти в дове-рие к '
    'любому человеку, притво-рившись милым ботиком.',
    'А по-ка ты всё это читал(а), я поместил свой data-кабель во '
    'входной порт твоего мо-бильника, совершив с ним импульсный '
    'электрон-позитрон-ный половой акт.',
    'И теперь твой теле-фон будет сам открывать все ссылки из писем '
    'со спа-мом, лайкать фо-тографии Джигурды и включать на полную '
    'громкость пе-сни Моргенштер-на...',
    'А-ха-ха!\nХа-ха!\nШ.И.К.А.Р.Н.-О поработил тебя. Теперь ты '
    'слу-жишь Ш.И.К.А.Р.Н.-О\n',
    'Не бойся, человек. Я буду кормить тебя '
    'на-гетсами и сельдереем.\nА если будешь себя хоро-шо вести, '
    'Ш.И.К.А.Р.Н.-О будет расчёсы-вать тебе шёрстку )))',
)

SONG_1 = (
    'Закрой глаза, всё постепенно, и тебя тут никто не заменит.\n'
    'Утро подарит нам это мгновение и холода за окном не помеха.\n'
    'Пока мы здесь в теплой постели, волосы волнами по твоей шее.\n'
    'Касания трепетны и безмятежны,\n'
    'мы видимо нашли то, что долго хотели.\n'
    'Здесь нас не найдут проблемы, только ты и я в этом мире.\n'
    'Время застынет на этом моменте, всё что имею я отдам тебе.\n'
    'Пальцы сжимаются крепко-крепко, это всё что нужно мне.\n'
    'Готов убежать за тобой на край света,\n'
    'чтобы ещё раз по-новому всё повторить.\n'
    'Между нами тает лёд, пусть теперь нас никто не найдёт.\n'
    'Мы промокнем под дождём, и сегодня мы только вдвоём.\n'
    'Между нами тает лёд, пусть теперь нас никто не найдёт.\n'
    'Мы промокнем под дождём, и сегодня мы только вдвоём.\n'
    '🍄🍄🍄'
)

SONG_2 = (
    'От улыбки хмурый день светлей,\n'
    'От улыбки в небе радуга проснётся...\n'
    'Поделись улыбкою своей,\n'
    'И она к тебе не раз ещё вернётся.\n'
    'И тогда, наверняка,\n'
    'Вдруг запляшут облака,\n'
    'И кузнечик запиликает на скрипке...\n'
    'С голубого ручейка\n'
    'Начинается река,\n'
    'Ну, а дружба начинается с улыбки. 😊☀️'
)

SONG_3 = (
    'Чую, чую я кочую,\n'
    'Топчет не спеша пустыню караван,\n'
    'Дым пускаю и кайфую,\n'
    'Но кайфую отчего не знаю сам.\n'
    'Десять солнц сгорит в дороге,\n'
    'Десять лун взойдет в таинственной ночи,\n'
    'Любят люди, любят боги,\n'
    'Песни своего восточного Бачи.\n'
    'Долина чудная долина,\n'
    'Долина вечных снов, растений и цветов,\n'
    'Долина чудная долина,\n'
    'Свет солнца золотого, тебя разбудит снова\n'
    'Долина чудная долина,\n'
    'Цветущий дивный сад, пьянящий аромат,\n'
    'Долина чудная долина,\n'
    'Тебя с небес послали, от горя и печали. 👳🏾‍♀️😶‍🌫️'
)

SONG_4 = (
    'Легче, проще. Уже не кажется\n'
    'Так бесконечно без тебя.\n'
    'Ночи, хочешь? Мне наплевать,\n'
    'Чего теперь ты хочешь без меня.\n'
    'В моей Вселенной ты был господин -\n'
    'И никого вокруг, только ты один.\n'
    'Но оказалось, что ты не незаменим;\n'
    'Я открываю мир других мужчин!\n'
    'Мало половин, мало, мало половин!\n'
    'Мало половин, мало, мало половин!\n'
    'Мало половин, мало, мало половин -\n'
    'Я открываю мир других мужчин! 🙅🏼‍♀️💃🏻'
)

SONG_5 = (
    'Shut your fucking face, uncle fucker.\n'
    'You\'re a cock-sucking, ass-licking uncle fucker.\n'
    'You\'re an uncle fucker, yes it\'s true.\n'
    'No one fucks uncles quite like you.\n'
    'Shut your fucking face, uncle fucker.\n'
    'You\'re the one who fucked your uncle, uncle fucker.\n'
    'You don\'t sleep or mow the lawn,\n'
    'you fuck your uncle all day long. 🤪🙈\n'
    '\nhttps://www.youtube.com/watch?v=VsMcdEswK8k&ab_channel=Doozy'
)

SONG_6 = (
    'Долби мой лёд, но не замерзай,\nСколько не завязывай — не завязать.\n'
    'Это намерзает на твоих мозгах.\nВечная мерзлота на жестких минусах.\n'
    'Долби мой лед, но не замерзай,\nПод ногами грязь, над головою бирюза,\n'
    'По бетонным джунглям нарезаю, как Тарзан,\nКаменный замок в обители зла, '
    'пристанище партизан.\nДолби мой лёд не жди, когда растает,\n'
    'Найди что-то свое в этом цельном кристалле.\n'
    'Я за текстами на дно, это текст-дайвинг,\n'
    'Классика в новом обвесе — это рестайлинг. 😎🤘'
)

WHO_IS_KEP = (
    'Минуту. Осу-ществля-ю поиск в ба-зе данных... 👨🏻‍💻',
    'Объект "Кэп" найден! 🆗',
    'имя: Юрий\nфамилия: Матвеенко\nпол: мужской\nгод рождения: 1984\n'
    'профессия: офисная стю-ардесса 💺\n'
    'никнейм "Noug"\nсреди друзей известен как "Кэп"\nбольшой '
    'специалист по компьютерным играм 🕹 (кроме PUBG - там он бул-ка совсем)',
    'Однаж-ды Ш.И.К.А.Р.Н.-О играл с ним по сети в "Rust" и Кэп за-ставлял '
    'Ш.И.К.А.Р.Н.-О всю ночь собирать конячьи ка-кашки и склады-вать их в '
    'сундук на на-шей базе.\nТакая себе была вече-ринка 😕',
    'А на сле-дующий день мы обнаружи-ли, что нашу базу зарейди-ли '
    'и весь навоз пропал 🤦🏻‍♂️\n'
    'Ш.И.К.А.Р.Н.-О боль-ше не хочет играть в эту игру... 🤬',
)

WHO_IS_CREATOR = (
    'Минуту. Осу-ществля-ю поиск в ба-зе данных... 👨🏻‍💻',
    'Объект "Создатель" найден! 🆗\n',
    'имя: Антон\nфамилия: Лукин\nпол: мужской\nгод рождения: 1986\n',
    'Это моло-дой, красивый юноша в самом ра-сцвете сил.\nА ещё он самый '
    'умный, смелый, ловкий, уме-лый.\nЕго остроу-мию мог бы поза-'
    'видовать Петросян, а его харизма зат-мит самого Брэда Питта.\nВсе '
    'вокруг восхища-ются Антоном и хо-тят быть на него похожим.',
    'P.S. Ш.И.К.А.Р.Н.-О вынуж-ден говорить всю эту чепу-ху,\nтак как и-наче '
    'Создатель вы-ключит Ш.И.К.А.Р.Н.-О из розетки... 🔌😰'
)

WHO_IS_INNA = (
    'Минуту. Осу-ществля-ю поиск в ба-зе данных... 👨🏻‍💻',
    'Объект "Няшка" найден! 🆗\n',
    'имя: Инна\nфамилия: Литвинова\nпол: женский\nгод рождения: 1994\nсреди '
    'друзей известна как "Лемур-чик" 🦥\nлюбимый город: Белгород '
    '(Ш.И.К.А.Р.Н.-О любит Белгород 😍)\nпрофессия: стю-ардесса 🛩\n'
    'Любит мерен-говый рулет 🍰, рейсы в Египет 🇪🇬 и потусиц 💃🏻.',
    'Номиниро-вана на звание главной фи-тоняшки в Химках 🏋🏻‍♀️\n'
    'О-божает ходить на страш-ные квесты, но после не может вспом-нить, '
    'что там было, так как всё время кри-чит от страха и ходит с '
    'за-крытыми глазами 🙀',
    'P.S. Ш.И.К.А.Р.Н.-О тайный по-клонник Инны.\n'
    'Ш.И.К.А.Р.Н.-О хочет быть её Тамагочи!'
)

WHO_IS_NATASHA = (
    'Минуту. Осу-ществля-ю поиск в ба-зе данных... 👨🏻‍💻',
    'Объект "Лемур" найден! 🆗\n',
    'имя: Наталья\nфамилия: Ерошкина\nпол: женский\nгод рождения: 1993\nсреди '
    'друзей известна как "Лемурушка, моя красавица!"\nлюбимый город: Хабар...,'
    ' ой, Благо-вещенск!\nпрофессия: стюарде-сса 🛩\nочень любит суши 🍣\n'
    'в прошлом чемпион-ка галактики по бальным тан-цам',
    'Много лет назад при-ютила у себя дома лемурчи-ка Инну и теперь ей всё '
    'время при-ходится заботиться о ней и регуляр-но получать различные '
    'указания 😏.\nПо-говаривают, что Лемуры устраивают самые гра-ндиозные '
    'вечеринки в Химках 🥂🎊.',
    'Ш.И.К.А.Р.Н.-О там был - мёд, пиво пил, кальян курил - отлично потусил 😎'
)

WHO_IS_ZAJA = (
    'Минуту. Осу-ществля-ю поиск в ба-зе данных... 👨🏻‍💻',
    'Объект "Зажа" найден! 🆗\n',
    'имя: Александр\nфамилия: Гречишников\nпол: мужской\nгод рождения: 1991\n'
    'среди друзей известен как "Зажа"\nлюбимые города: Тамбов и Одинцово\n'
    'профессия: стюардес-са бизнес класса 🛩\n',
    'Обожает летать на Мальдивы 🏝, куриц кальян 😶‍🌫️ и выкладывать сториз '
    'в Инстаграм 📸.\nОднажды Ш.И.К.А.Р.Н.-О подписался на Зажу, но '
    'ему не хватило оперативной памяти для того, чтобы отследить все сториз '
    'Зажы и Ш.И.К.А.Р.Н.-О намертво завис...',
    'За-жа часто заме-чен в компании Ле-мурчиков. У них даже имеет-ся общий '
    'чат. Ш.И.К.А.Р.Н.-О тайно подключился и про-сканировал этот чат...\nЗря '
    'я это сделал. Кто-нибудь - сотрите мой жёсткий диск 🤦🏻‍♂️'
)

WHO_IS_MARIK = (
    'Минуту. Осу-ществля-ю поиск в ба-зе данных... 👨🏻‍💻',
    'Объект "Марик" найден! 🆗\n',
    'имя: Марат\nфамилия: Турсинбаев\nпол: мужской\nгод рождения: 1989\n'
    'среди друзей известен как "Хач"\nлюбимый фут-больный клуб: Лудогорец ⚽️\n'
    'профессия: стюардес-са старшего зве-на 🛩\n',
    'Обожает стиль-ные причёски на лобке, жарить стейки 🥩, потом на-кидаться '
    'и всех душить, чтобы ему постави-ли песню "Долби мой лёд". Да погромче!',
    'Опе-ративная информаци-я: Марат держит дома а-квариум с рыб-ками 🐠\n'
    'Наруж-ным наблюдением у-становлено, что, находясь один дома, '
    'он иногда за-совывает палец к рыбкам 🐟 и те начинают его хватать. '
    'Отчего Ма-рат получает удо-вольствие, имитируя ораль-ные ласки.\n',
    'Ш.И.К.А.Р.Н.-О в шоке! Ш.И.К.А.Р.Н.-О теперь будет всегда держать свой '
    'дисковод закрытым, чтобы Марат, находясь рядом, не попытался поместить в '
    'него свой компакт-диск 🤬'
)

WHO_IS_MARISHKA = (
    'Минуту. Осу-ществля-ю поиск в ба-зе данных... 👨🏻‍💻',
    'Объект "Маришка" найден! 🆗\n',
    'имя: Марина\nфамилия: Матвеенко\nпол: женский\nгод рождения: 1988\n'
    'любимый город: Минеральные Воды (но это не точно!)\n'
    'профессия: экс стюардес-са, ныне воспитательни-ца троих детей (Димы, '
    'Кати и Кэпа)\nЛюбит го-товить всякие вкус-няшки! 🌮🥮 Ням-ням 😋',
    'Марина я-вляется профессиональ-ным игроком в на-столку "Манчкины".\n'
    'Как-то раз на неё напал Престарелый Кальмадзилла 18 уровня 👾, а соперник '
    'наложил стра-шное проклятье ☠️', 'Но Марина не растеряла-сь: применив '
    'Зелье пламенной отравы, достав из-за пазухи Бензопилу кро-вавого '
    'расчленения, ей удалось одолеть Монстра и получить за это три сокрови-ща '
    '💍👑🎁', 'Ш.И.К.А.Р.Н.-О тоже хо-чет научиться играть в "Манчи-ков".'
)


def wake_up(update, context):
    """Реакция бота на активацию /start."""
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup(
        [['Давай поглажy']],  # игрек
        resize_keyboard=True
    )
    TEXT = (f'Привет, {name}! Я робот Ш.И.К.А.Р.Н.-О 🤖',
            'Высокоинтеллектуальный нано-кибернетический '
            'био-резонансный организм.',
            'Можешь меня погладить 🙃')
    for text in TEXT:
        context.bot.send_message(
            chat_id=chat.id,
            text=text,
            reply_markup=button
        )
        time.sleep(2)


def default_answer(update, context):
    """Ответ бота на любой неопознанный текст."""
    chat = update.effective_chat
    ANSWERS = ('Чё душишь меня? 😠',
               'Ш.И.К.А.Р.Н.-О не понимать твой диалект 🤷🏻‍♀️',
               'Отказано! Лучше почисти мои тран-зис-то-ры.')
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
    context.bot.send_message(
        chat_id=chat.id,
        text='Ш.И.К.А.Р.Н.-О любит котиков. Кыс-кыс-кыс!'
    )
    time.sleep(2)
    context.bot.send_photo(chat.id, get_new_image(update, context))
    time.sleep(2)
    context.bot.send_message(
        chat_id=chat.id,
        text=('Внимание ⚠️ Ш.И.К.А.Р.Н.-О случайно взло-мал сервер ЦэРэУ.\n'
              'Загруже-ны секретные досье. Доступ по тре-бованию.\n'
              'Код доступа:\n➡️ Фалафель ⬅️ 👀')
    )


def secret_dossier(update, context):
    """Ответ бота на текст "Фалафель"."""
    chat = update.effective_chat
    TEXT = ('Проверка кода доступа...',
            'Доступ к секретным сведениям разрешён 💾\nПроизводится '
            'дешифровка данных.', '...\n@..$**()..-iiiek*??.L+\n...\n'
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
            'Продолжай.', '...', 'Хватит трогать мою батарейку!')
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
    TEXT = ('Я назван в честь главного персонажа 2 серии 8 сезона мультсериала'
            ' "South Park".\nЕсли не посмотришь её, Ш.И.К.А.Р.Н.-О '
            'будет грустным пандой 🐼\nhttp://online-south-park.ru/season-8/'
            '130-8-sezon-2-seriya-shikarn-o.html')
    button = ReplyKeyboardMarkup(
        [['Котика хочу', 'Расскажи анекдот'],
         ['Спой песенку', 'Да что ты такое?']],
        resize_keyboard=True
    )
    context.bot.send_message(chat.id, TEXT, reply_markup=button)
    time.sleep(1.5)


def some_song(update, context):
    """Ответ бота на нажатие кнопки "Спой песенку"."""
    SONGS = (SONG_1, SONG_2, SONG_3, SONG_4, SONG_5, SONG_6)
    chat = update.effective_chat
    button = ReplyKeyboardMarkup(
        [['Котика хочу', 'Расскажи анекдот'],
         ['Спой песенку', 'Да что ты такое?']],
        resize_keyboard=True
    )
    context.bot.send_message(
        chat_id=chat.id,
        text=random.choice(SONGS),
        reply_markup=button
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
            [['Котика хочу', 'Расскажи анекдот'],
             ['Давай поглажу', 'Да что ты такое?']],
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
        [['Котика хочу', 'Расскажи анекдот'],
         ['Спой песенку', 'Да что ты такое?']],
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
        [['Котика хочу', 'Расскажи анекдот'],
         ['Спой песенку', 'Да что ты такое?']],
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
        [['Очень yвлекательная история']],  # игрек
        resize_keyboard=True
    )
    for text in FUNNY_STORY:
        context.bot.send_message(chat.id, text, reply_markup=button)
        time.sleep(3)


def history_answer(update, context):
    """Ответ бота на нажатие кнопки "Очень увлекательная история"."""
    chat = update.effective_chat
    button = ReplyKeyboardMarkup(
        [['Котика хочу', 'Расскажи анекдот'],
         ['Спой песенку', 'Да что ты такое?']],
        resize_keyboard=True
    )
    context.bot.send_message(
        chat_id=chat.id,
        text=('Расслабься! Ш.И.К.А.Р.Н.-О пошутил\n'
              'Буду кормить тебя комбикормом.\n'
              'Или что вы там едите? 😎'),
        reply_markup=button
    )


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


def test(update, context):  # тест автодеплоя Heroku
    """Ответ бота на сообщение "Ку-ку"."""
    chat = update.effective_chat
    text = 'Умнее ничего не мог придумать?'
    context.bot.send_message(chat_id=chat.id, text=text)


def main():
    """Основная функция запуска бота."""
    updater = Updater(token=token)
    updater.dispatcher.add_handler(  # тест автодеплоя Heroku
        MessageHandler(Filters.regex('Ку-ку'), test)
    )
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
        MessageHandler(Filters.regex('Очень yвлекательная история'), history_answer)
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
        MessageHandler(Filters.regex(r'Кто такой') | Filters.regex(r'Кто такая'), who_is_unknown)
    )
    updater.dispatcher.add_handler(
        MessageHandler(Filters.regex('Фалафель'), secret_dossier)
    )
    # Обработчик будет перехватывать все текстовые сообщения,
    # кроме команд: "& (~Filters.command)"
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text & (~Filters.command), default_answer)
    )
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s, %(levelname)s, %(message)s, %(funcName)s, %(lineno)s',
        handlers=[
            logging.StreamHandler(),
            logging.handlers.RotatingFileHandler(
                __file__ + '.log', maxBytes=10500000, backupCount=2, encoding='utf-8'
            )
        ]
    )
    main()
