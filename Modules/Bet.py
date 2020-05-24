@bot.message_handler(commands=["bet"])
def do_bet(message):
    if message.chat.id != message.from_user.id:
        bot.send_message(
            message.chat.id, _("This command can not be used on group chats.")
        )
        return
    get_user(message)
    chat_id = message.chat.id
    query = get_matches()
    matches = (
        query.filter(Match.score1 == None)
        .filter(Match.start_date > datetime.datetime.now())
        .all()
    )
    query = get_bets()
    user_bets = query.filter(Bet.player_id == message.from_user.id).all()
    markup = types.ReplyKeyboardMarkup(row_width=len(matches))
    to_bet = 0
    for m in matches:
        to_bet += 1
        markup.add(str(m.id) + " - " + m.title + " - " + m.team1 + " - " + m.team2)
    if not matches or not to_bet:
        bot.send_message(
            message.chat.id, _("No matches available (Or you already bet on all).")
        )
        return
    markup.add(_("Cancel"))
    bot.send_message(chat_id, _("Choose a match:"), reply_markup=markup)
    userStep[message.from_user.id] = 51


@bot.message_handler(func=lambda message: get_user_step(message.from_user.id) == 51)
def do_bet_winner(message):
    chat_id = message.chat.id
    if message.text == _("Cancel"):
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, _("Action cancelled."), reply_markup=markup)
        userStep[message.from_user.id] = None
        return
    mid = message.text.split(" ")
    query = get_matches()
    try:
        match = query.filter(Match.id == int(mid[0])).one()
        to_bet[message.from_user.id] = mid
        markup = types.ReplyKeyboardMarkup(row_width=2)
        markup.add(match.team1)
        markup.add(match.team2)
        markup.add(_("Cancel"))
        bot.send_message(chat_id, _("Choose a winner:"), reply_markup=markup)
        userStep[message.from_user.id] = 52
    except ValueError:
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, _("Action cancelled."), reply_markup=markup)


@bot.message_handler(func=lambda message: get_user_step(message.from_user.id) == 52)
def set_match_winner_db(message):
    userStep[message.from_user.id] = None
    chat_id = message.chat.id
    markup = types.ReplyKeyboardRemove()
    if message.text == _("Cancel"):
        bot.send_message(message.chat.id, _("Action cancelled."), reply_markup=markup)
        userStep[message.from_user.id] = None
        return
    mid = to_bet[message.from_user.id]
    query = get_bets()
    # TODO Add unique constraint on sql match and return error if already bet
    already_bet = (
        query.filter(Bet.player_id == message.from_user.id)
        .filter(Bet.match == mid[0])
        .first()
    )
    if already_bet:
        already_bet.bet = message.text
        already_bet.match = mid[0]
        update()
        bot.send_message(chat_id, _("New bet correctly update"), reply_markup=markup)
        userStep[message.from_user.id] = None
        return
    new_bet = Bet(player_id=message.from_user.id, match=mid[0], bet=message.text)
    add(new_bet)
    bot.send_message(chat_id, _("Bet correctly done."), reply_markup=markup)
    userStep[message.from_user.id] = None

