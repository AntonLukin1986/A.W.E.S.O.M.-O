import shelve


def dice_game_stat(game_stat, PLAYER):
    """Анализ статистики для вывода в конце раунда. И сохранение в БД."""
    bot_win = game_stat['BOT']['wins']
    bot_made_bet = game_stat['BOT']['made_bet']
    bot_guessed_bet = game_stat['BOT']['guessed_bet']
    bot_double_six = game_stat['BOT']['double_six']
    bot_double_one = game_stat['BOT']['double_one']
    player_win = game_stat[f'{PLAYER}']['wins']
    player_made_bet = game_stat[f'{PLAYER}']['made_bet']
    player_guessed_bet = game_stat[f'{PLAYER}']['guessed_bet']
    player_double_six = game_stat[f'{PLAYER}']['double_six']
    player_double_one = game_stat[f'{PLAYER}']['double_one']
    total_games = bot_win + player_win
    db = shelve.open('statistic')
    for player in game_stat:
        game_stat[player]['games'] = total_games
    statistic = db['DICE']
    for player, new_data in game_stat.items():
        if player not in statistic:
            statistic[player] = new_data
            continue
        for key, value in new_data.items():
            statistic[player][key] += value
    db['DICE'] = statistic
    db.close()
    return (f'Ш.И.К.А.Р.Н.-О  🆚  {PLAYER}\n 👊 cыграно раундов:  {total_games}\n\n'
            '✅ Ш.И.К.А.Р.Н.-О\n'
            f'победы:  {bot_win}\nпроигрыши:  {player_win}\nсделал ставок:  {bot_made_bet}\nугадал:  {bot_guessed_bet}\n'
            f'6️⃣6️⃣ выпадали:  {bot_double_six}\n1️⃣1️⃣ выпадали:  {bot_double_one}\n\n'
            f'✅ {PLAYER}\n'
            f'победы:  {player_win}\nпроигрыши:  {bot_win}\nсделано ставок:  {player_made_bet}\nугадано:  {player_guessed_bet}\n'
            f'6️⃣6️⃣ выпадали:  {player_double_six}\n1️⃣1️⃣ выпадали:  {player_double_one}')


def hall_of_fame():
    """Сортировка игроков в зависимости от статистических показателей."""
    db = shelve.open('statistic')
    rating = []
    for player, data in db['DICE'].items():
        name = 'Ш.И.К.А.Р.Н.-О 🤖' if player == 'BOT' else player
        games = data['games']
        wins = data['wins']
        share_of_wins = wins / games * 100
        looses = games - wins
        dry_wins = data['dry_wins']
        share_of_dry_wins = dry_wins / wins * 100
        triple_bet = data['triple_bet']
        share_of_triple_bet = triple_bet / wins * 100
        made_bet = data['made_bet']
        guessed_bet = data['guessed_bet']
        share_of_guessed_bet = guessed_bet / made_bet * 100
        average_dice_to_win = made_bet / wins
        double_six = data['double_six']
        share_of_double_six = double_six / made_bet * 100
        double_one = data['double_one']
        share_of_double_one = double_one / made_bet * 100
        add = (-share_of_wins, average_dice_to_win, -share_of_guessed_bet, -dry_wins, -triple_bet, games, wins,
               looses, made_bet, guessed_bet, double_six, share_of_double_six, double_one, share_of_double_one,
               share_of_dry_wins, share_of_triple_bet, name)
        rating.append(add)
    last_champion = db['DICE_CHAMPION']
    db.close()
    rating.sort()
    return rating, last_champion
