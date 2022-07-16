"""Подключаемые функции для бота Ш.И.К.А.Р.Н.-О.."""
import datetime as dt
import logging
import shelve
from typing import Optional


def start_logging() -> None:
    """Логгирование работы бота."""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s, %(levelname)s, %(message)s, %(funcName)s, '
               '%(lineno)s',
        handlers=[
            logging.StreamHandler(),
            logging.handlers.RotatingFileHandler(
                'awesom_o.py.log',  # __file__ + '.log' -> текущее имя модуля
                maxBytes=2100000,
                backupCount=2,
                encoding='utf-8'
            )
        ]
    )


def inline_menu(buttons: list,
                columns: int,
                first_buttons: Optional[list] = None,
                last_buttons: Optional[list] = None) -> list[list]:
    """Функция для создание меню инлайн-кнопок."""
    menu = [buttons[i:i + columns] for i in range(0, len(buttons), columns)]
    if first_buttons:
        menu.insert(0, [first_buttons])
    if last_buttons:
        menu.append([last_buttons])
    return menu


def record_new_visitor(update) -> None:
    """Учёт пользователей, контактировавших с ботом."""
    user_id = update.message.chat.id
    db = shelve.open('statistic')
    visitors = db.setdefault('VISITORS', {})
    if user_id not in visitors:
        user = update.message.chat
        joined = dt.date.today().strftime('%d.%m.%Y')
        data = (
            f'ник: {user.username}, имя: {user.first_name}, дата: {joined}\n'
        )
        visitors[user_id] = data
        db['VISITORS'] = visitors
    db.close()


def visitors_list() -> str:
    """Создаёт перечень посетителей бота в виде строки."""
    db = shelve.open('statistic')
    visitors = db.get('VISITORS')
    if visitors is None:
        text = 'Посетителей не было 🙅🏻‍♂️'
    else:
        text = '✏️    Посетители:\n'
        for i, person in enumerate(visitors.values(), start=1):
            text += f'{i}. {person}\n'
    db.close()
    return text


def dice_game_stat(game_stat: dict, player: str) -> str:
    """Анализ статистики. Выводится в конце раунда и сохраненяется в БД."""
    bot_win = game_stat['BOT']['wins']
    bot_made_bet = game_stat['BOT']['made_bet']
    bot_guessed_bet = game_stat['BOT']['guessed_bet']
    bot_double_six = game_stat['BOT']['double_six']
    bot_double_one = game_stat['BOT']['double_one']
    player_win = game_stat[player]['wins']
    player_made_bet = game_stat[player]['made_bet']
    player_guessed_bet = game_stat[player]['guessed_bet']
    player_double_six = game_stat[player]['double_six']
    player_double_one = game_stat[player]['double_one']
    total_games = bot_win + player_win
    db = shelve.open('statistic')
    for player in game_stat:
        game_stat[player]['games'] = total_games
    statistic = db.setdefault('DICE', {})
    for player, new_data in game_stat.items():
        if player not in statistic:
            statistic[player] = new_data
            continue
        for key, value in new_data.items():
            statistic[player][key] += value
    db['DICE'] = statistic
    db.close()
    return (
        f'Ш.И.К.А.Р.Н.-О  🆚  {player}\n 👊 cыграно раундов:  {total_games}\n\n'
        '✅ Ш.И.К.А.Р.Н.-О\n'
        f'победы:  {bot_win}\nпроигрыши:  {player_win}\nсделал ставок:  '
        f'{bot_made_bet}\nугадал:  {bot_guessed_bet}\n6️⃣6️⃣ выпадали:  '
        f'{bot_double_six}\n1️⃣1️⃣ выпадали:  {bot_double_one}\n\n'
        f'✅ {player}\n'
        f'победы:  {player_win}\nпроигрыши:  {bot_win}\nсделано ставок:  '
        f'{player_made_bet}\nугадано:  {player_guessed_bet}\n6️⃣6️⃣ выпадали:'
        f'  {player_double_six}\n1️⃣1️⃣ выпадали:  {player_double_one}'
    )


def hall_of_fame() -> tuple[Optional[list], Optional[dict]]:
    """Сортировка игроков в зависимости от статистических показателей."""
    db = shelve.open('statistic')
    if not db.get('DICE'):
        return None, None
    rating = []
    for player, data in db['DICE'].items():
        name = 'Ш.И.К.А.Р.Н.-О 🤖' if player == 'BOT' else player
        games = data['games']
        wins = data['wins']
        share_of_wins = wins / games * 100
        looses = games - wins
        dry_wins = data['dry_wins']
        triple_bet = data['triple_bet']
        made_bet = data['made_bet']
        guessed_bet = data['guessed_bet']
        share_of_guessed_bet = guessed_bet / made_bet * 100
        double_six = data['double_six']
        share_of_double_six = double_six / made_bet * 100
        double_one = data['double_one']
        share_of_double_one = double_one / made_bet * 100
        if wins == 0:
            share_of_dry_wins = 0
            share_of_triple_bet = 0
            average_dice_to_win = 0
        else:
            share_of_dry_wins = dry_wins / wins * 100
            share_of_triple_bet = triple_bet / wins * 100
            average_dice_to_win = made_bet / wins
        add = (
            -share_of_wins, average_dice_to_win, -share_of_guessed_bet,
            -dry_wins, -triple_bet, games, wins, looses, made_bet,
            guessed_bet, double_six, share_of_double_six, double_one,
            share_of_double_one, share_of_dry_wins, share_of_triple_bet, name
        )
        rating.append(add)
    last_champion = db.setdefault('DICE_CHAMPION', {})
    db.close()
    rating.sort()
    return rating, last_champion
