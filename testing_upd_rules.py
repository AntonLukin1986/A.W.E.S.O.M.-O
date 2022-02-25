import os
import random
import time

from dotenv import load_dotenv
from telegram import Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, Filters, MessageHandler, Updater

load_dotenv()
token = os.getenv('AWESOM_O_TOKEN')
bot = Bot(token=token)


CATS_TRAIN = 'Пойду тренироваться. На кошках 🐈'
EAT_CORN = 'Пойду грызть свою кукурузку 😋'
ENOUGH = 'Точно! Хватит 🖐'
GO = 'Поехали 👌'
NO_MORE_GAME = 'Больше не хочу играть 😐'
REVENGE = 'Хочу реванш 🥊'
WIN_BACK = 'Дам тебе отыграться 😙'
YOUR_TURN = 'Твой ход 👆'

BET_RANGE = r'^([3-9]|[1][0-1]) ([3-9]|[1][0-1])$'
BOT_DICE, USER_BET, USER_DICE = 1, 2, 3
BOT_WINS = 0
USER_DICE_COUNTER = 0
USER_DICE_RESULT = 0
USER_WINS = 0


def games_stat():
    """Анализ статистики из GAME_STAT для вывода в конце раунда."""
    bot_win = GAME_STAT['BOT']['wins']
    bot_made_bet = GAME_STAT['BOT']['made_bet']
    bot_guessed_bet = GAME_STAT['BOT']['guessed_bet']
    bot_double_six = GAME_STAT['BOT']['double_six']
    bot_double_one = GAME_STAT['BOT']['double_one']
    player_win = GAME_STAT[f'{PLAYER}']['wins']
    player_made_bet = GAME_STAT[f'{PLAYER}']['made_bet']
    player_guessed_bet = GAME_STAT[f'{PLAYER}']['guessed_bet']
    player_double_six = GAME_STAT[f'{PLAYER}']['double_six']
    player_double_one = GAME_STAT[f'{PLAYER}']['double_one']
    total_games = bot_win + player_win
    return (
        f'Ш.И.К.А.Р.Н.-О  🆚  {PLAYER}\n ℹ️ cыграно раундов:  {total_games}\n\n'
        f'✅ Ш.И.К.А.Р.Н.-О \n'
        f'победы:  {bot_win}' + f'  =>  {bot_win / total_games * 100:.1f}%' if bot_win else '' + f'\nпроигрыши:  {player_win}\n'
        f'ставок:  {bot_made_bet}  успешных:  {bot_guessed_bet}' + f'  =>  {bot_guessed_bet / bot_made_bet * 100:.1f}%' if bot_guessed_bet else '' + '\n'
        f'В среднем бросков для победы  {bot_made_bet / bot_win:.1f}\n' if bot_win else ''
        f'6️⃣6️⃣ выпадали:  {bot_double_six}' + f'  =>  {bot_double_six / bot_made_bet * 100:.1f}%' if bot_double_six else '' + '\n'
        f'1️⃣1️⃣ выпадали:  {bot_double_one}' + f'  =>  {bot_double_one / bot_made_bet * 100:.1f}%' if bot_double_one else '' + '\n\n'
        f'✅ {PLAYER}\n'
        f'победы:  {player_win}' + f'  =>  {player_win / total_games * 100:.1f}%' if player_win else '' + f'\nпроигрыши:  {bot_win}\n'
        f'ставок:  {player_made_bet}  успешных:  {player_guessed_bet}' + f'  =>  {player_guessed_bet / player_made_bet * 100:.1f}%' if player_guessed_bet else '' + '\n'
        f'В среднем бросков для победы  ' + f'{player_made_bet / player_win:.1f}' if player_win else '--' + '\n'
        f'6️⃣6️⃣ выпадали:  {player_double_six}' + f'  =>  {player_double_six / player_made_bet * 100:.1f}%' if bot_double_six else '' + '\n'
        f'1️⃣1️⃣ выпадали:  {player_double_one}' + f'  =>  {player_double_one / player_made_bet * 100:.1f}%' if bot_double_one else ''
    )


def game_rules(update, _):
    """Ответ на кнопку "Старт"."""
    global GAME_STAT, PLAYER
    GAME_STAT = {'BOT': dict(wins=0, double_six=0, double_one=0, made_bet=0, guessed_bet=0)}
    PLAYER = update.message.chat.full_name
    GAME_STAT[f'{PLAYER}'] = dict(wins=0, double_six=0, double_one=0, made_bet=0, guessed_bet=0)
    button = ReplyKeyboardMarkup([[GO]], resize_keyboard=True)
    RULES_DICE = (
        'Рассказываю пра-вила игры 🤓\nИгроки по очереди бро-сают две игральные кости 🎲\nПеред бросками необходи-мо предсказать свой '
        'ре-зультат, назвав два числа.\nЕсли сум-ма выпавших очков 👓 со-впадёт с одним из этих чисел - игрок зара-батывает один балл.\n',
        'Если на ку-биках выпадут 1️⃣1️⃣ - с игрока снимает-ся один балл (если он есть). Пе-чалька 😩\nЗато, если выпадут 6️⃣6️⃣ - '
        'игрок автомати-чески зарабатывает один балл! Джек пот 🥳\nСоответственно, числа 2 и 12 загадывать не нужно ⚠️ '
        'Диапозон возможных ставок: от 3 до 11 ‼️\nПобежда-ет тот, кто первым наберёт 3️⃣ балла 🏆💐🎊',
        'Победи-телю торжественно вручат кочан ку-курузы 🌽 и похлопают по плечу 👏\nПроигравшего ждёт неодобри-тельное освистывание и '
        '20 часов исправи-тельных работ 🧤🪚⚒\nНо это не точно 🤔', 'Я похо-жу первым и покажу, как это ра-ботает ☝️'
    )
    for text in RULES_DICE:
        update.message.reply_text(text, reply_markup=button if text == RULES_DICE[-1] else None)
    return BOT_DICE


def bot_bet_roll_dice(update, _):
    """Ответ на кнопки "Поехали 👌", "Твой ход 👆", "Хочу реванш 🥊" и "Дам тебе отыграться 😙"."""
    cancel = ReplyKeyboardMarkup([[NO_MORE_GAME]], resize_keyboard=True)
    choise = ReplyKeyboardMarkup([[REVENGE], [CATS_TRAIN]], resize_keyboard=True)
    global BOT_WINS, USER_WINS
    bet_1, bet_2 = random.randint(3, 11), random.randint(3, 11)
    while bet_2 == bet_1:
        bet_2 = random.randint(3, 11)
    update.message.reply_text(f'Я поставлю на {bet_1} и {bet_2} ✍️', reply_markup=ReplyKeyboardRemove())
    GAME_STAT['BOT']['made_bet'] += 1
    update.message.reply_text('Бросаю ко-сти... ✊')
    result = 0
    for _ in (1, 2):
        value = update.message.reply_dice()['dice']['value']
        result += value
    update.message.reply_text(f'Мой ре-зультат:  {result} ❗️', reply_markup=cancel)
    if result in (bet_1, bet_2, 2, 12):
        if result == 2:
            update.message.reply_text('О, нет! 😱 Две еди-нички. Минус балл 😭')
            GAME_STAT['BOT']['double_one'] += 1
            if BOT_WINS > 0: BOT_WINS -= 1
        elif result == 12:
            update.message.reply_text('Я со-рвал Джек пот 🥳 Две шестёрки! Получаю балл 👏')
            GAME_STAT['BOT']['double_six'] += 1
            BOT_WINS += 1
        else:
            update.message.reply_text('Ура! Удача на моей сто-роне 😄\nЯ вы-играл в этом раунде 🦾')
            GAME_STAT['BOT']['guessed_bet'] += 1
            BOT_WINS += 1
        if BOT_WINS == USER_WINS:
            update.message.reply_text(f'Счёт {BOT_WINS} : {USER_WINS}\У нас ничья 🍻')
        else:
            update.message.reply_text(f'Счёт {BOT_WINS} : {USER_WINS}\n' + ('Я впереди 🤘' if BOT_WINS > USER_WINS else 'В твою пользу 😕'))
        if BOT_WINS == 3:
            update.message.reply_text(
                f'Финальный ре-зультат: 💫 {BOT_WINS} : {USER_WINS} 💫' + '  Всухую 🙈' if abs(BOT_WINS - USER_WINS) == 3 else '' + '\n\n'
                'Ехууу 🥳 Победа за мной!\nУчись у мастера, салага 😎',
                reply_markup=choise
            )
            GAME_STAT['BOT']['wins'] += 1
            update.message.reply_text(games_stat())
            BOT_WINS = 0
            USER_WINS = 0
            return BOT_DICE
    else:
        update.message.reply_text('Не угадал 😔\nЛадно, в следую-щий раз повезёт...')
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
    your_turn = ReplyKeyboardMarkup([[YOUR_TURN]], resize_keyboard=True)
    choice = ReplyKeyboardMarkup([[WIN_BACK], [EAT_CORN]], resize_keyboard=True)
    global BOT_WINS, USER_DICE_COUNTER, USER_DICE_RESULT, USER_WINS
    points = update.message.dice['value']
    USER_DICE_COUNTER += 1
    USER_DICE_RESULT += points
    if USER_DICE_COUNTER != 2:
        update.message.reply_text('Бросай ещё 👉')
        return None
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
            update.message.reply_text('Удача на твоей сто-роне.\nТы победил в этот раз 😠')
            GAME_STAT[f'{PLAYER}']['guessed_bet'] += 1
            USER_WINS += 1
        if USER_WINS == BOT_WINS:
            update.message.reply_text(f'Счёт {BOT_WINS} : {USER_WINS}\nУ нас ничья 🍻')
        else:
            update.message.reply_text(f'Счёт {BOT_WINS} : {USER_WINS}\n' + ('Я впереди 🙃' if BOT_WINS > USER_WINS else 'В твою пользу 😒'))
        if USER_WINS == 3:
            update.message.reply_text(
                f'Финальный ре-зультат: 💫 {USER_WINS} : {BOT_WINS} 💫\n\nПо-здравляю, твоя победа! Можешь пола-комиться ку-курузкой 🌽😏\n'
                'Но сильно не за-знавайся - тебе просто повез-ло 😈 Понимаешь, да?',
                reply_markup=choice
            )
            GAME_STAT[f'{PLAYER}']['wins'] += 1
            update.message.reply_text(games_stat())
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
    confirm = ReplyKeyboardMarkup([[ENOUGH], ['Нет, я передумал 🙃']], resize_keyboard=True)
    if update.message.text == NO_MORE_GAME:
        update.message.reply_text('Точно не хочешь про-должать?\nВесь прогресс сбросит-ся 🧐', reply_markup=confirm)
    if update.message.text == CATS_TRAIN or update.message.text == EAT_CORN or update.message.text == ENOUGH:
        update.message.reply_text('Ладно. За-хочешь ещё сыграть - ты знаешь, где меня най-ти 😼',
                                  reply_markup=ReplyKeyboardRemove())  # здесь нужна кнопка главного меню
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
    update.message.reply_text('Тебе ну-жно два раза бросить кубик. Сосре-доточься 🤨')


def dice_fallback(update, _):
    """Стандартный ответ внутри диалога игры в кости."""
    update.message.reply_text('У нас игра. Не отвле-кайся 🤨')


def default_answer(update, _):
    update.message.reply_text('Фраза ВНЕ диалога!!!')


def main():
    updater = Updater(token=token)
    handler = updater.dispatcher.add_handler

    play_game = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('Старт'), game_rules)],
        states={
            BOT_DICE: [MessageHandler(Filters.regex(GO + '|' + YOUR_TURN + '|' + REVENGE + '|' + WIN_BACK), bot_bet_roll_dice),
                       MessageHandler(Filters.regex(CATS_TRAIN + '|' + EAT_CORN), cancel_game)],
            USER_BET: [MessageHandler(Filters.regex(BET_RANGE), user_bets),
                       MessageHandler(Filters.regex(NO_MORE_GAME + '|' + ENOUGH), cancel_game),
                       MessageHandler(Filters.all, place_bet)],
            USER_DICE: [MessageHandler(Filters.dice, user_roll_dice),
                        MessageHandler(Filters.all, go_on)],
        },
        fallbacks=[MessageHandler(Filters.all, dice_fallback)]
    )
    handler(play_game)

    handler(MessageHandler(Filters.text & ~Filters.command, default_answer))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
