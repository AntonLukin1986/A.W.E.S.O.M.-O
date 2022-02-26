def dice_game_stat(GAME_STAT, PLAYER):
    """Анализ статистики для вывода в конце раунда."""
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
        f'Ш.И.К.А.Р.Н.-О  🆚  {PLAYER}\n 👊 cыграно раундов:  {total_games}\n\n'
        '✅ Ш.И.К.А.Р.Н.-О\n'
        f'победы:  {bot_win}' + (f'  =>  {bot_win / total_games * 100:.1f}%' if bot_win else '') + f'\nпроигрыши:  {player_win}\n'
        f'ставок:  {bot_made_bet}  успешных:  {bot_guessed_bet}' + (f'  =>  {bot_guessed_bet / bot_made_bet * 100:.1f}%' if bot_guessed_bet else '') + '\n' +
        (f'В среднем бросков для победы  {bot_made_bet / bot_win:.1f}\n' if bot_win else '') +
        f'6️⃣6️⃣ выпадали:  {bot_double_six}' + (f'  =>  {bot_double_six / bot_made_bet * 100:.1f}%' if bot_double_six else '') + '\n'
        f'1️⃣1️⃣ выпадали:  {bot_double_one}' + (f'  =>  {bot_double_one / bot_made_bet * 100:.1f}%' if bot_double_one else '') + '\n\n'
        f'✅ {PLAYER}\n'
        f'победы:  {player_win}' + (f'  =>  {player_win / total_games * 100:.1f}%' if player_win else '') + f'\nпроигрыши:  {bot_win}\n'
        f'ставок:  {player_made_bet}  успешных:  {player_guessed_bet}' + (f'  =>  {player_guessed_bet / player_made_bet * 100:.1f}%' if player_guessed_bet else '') + '\n'
        'В среднем бросков для победы  ' + (f'{player_made_bet / player_win:.1f}' if player_win else '--') + '\n'
        f'6️⃣6️⃣ выпадали:  {player_double_six}' + (f'  =>  {player_double_six / player_made_bet * 100:.1f}%' if bot_double_six else '') + '\n'
        f'1️⃣1️⃣ выпадали:  {player_double_one}' + (f'  =>  {player_double_one / player_made_bet * 100:.1f}%' if bot_double_one else ''))
