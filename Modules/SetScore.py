@bot.message_handler(commands=["setscore"])
def set_winner(message):
    chat_id = message.chat.id
    if message.from_user.id not in administrators:
        bot.send_message(message.chat.id, _("You can not use this command."))
        return
    if chat_id != message.from_user.id:
        bot.send_message(
            message.chat.id, _("This command can not be used on group chats.")
        )
        return
    query = get_matches()
    matches = query.filter(Match.score1 == None).filter(Match.score1 == None).all()
    if not matches:
        bot.send_message(message.chat.id, _("No matches available."))
        return
    markup = types.ReplyKeyboardMarkup(row_width=len(matches))
    for m in matches:
        markup.add(str(m.id) + " - " + m.title + " - " + m.team1 + " - " + m.team2)
    markup.add(_("Cancel"))
    bot.send_message(chat_id, _("Choose a match:"), reply_markup=markup)
    userStep[message.from_user.id] = 31


@bot.message_handler(func=lambda message: get_user_step(message.from_user.id) == 31)
def confirm_match_choose(message):
    if message.text == _("Cancel"):
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, _("Action cancelled."), reply_markup=markup)
        userStep[message.from_user.id] = None
        return
    chat_id = message.chat.id
    markup = types.ReplyKeyboardRemove()
    bot.send_message(chat_id, _("Match selected correctly."), reply_markup=markup)
    mid = message.text.split(" ")
    query = get_matches()
    match = query.filter(Match.id == int(mid[0])).one()
    to_winner[message.from_user.id] = {
        "id": match.id,
        "team1": match.team1,
        "team2": match.team2,
    }
    markup = types.ForceReply(selective=False)
    bot.send_message(chat_id, match.team1 + " " + _("Score:"), reply_markup=markup)
    userStep[message.from_user.id] = 32


@bot.message_handler(func=lambda message: get_user_step(message.from_user.id) == 32)
def second_score(message):
    chat_id = message.chat.id
    markup = types.ForceReply(selective=False)
    if message.text == _("Cancel"):
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, _("Action cancelled."), reply_markup=markup)
        userStep[message.from_user.id] = None
        return

    if not message.text.isdigit():
        set_winner(message)
        return

    to_winner[message.from_user.id]["score1"] = message.text
    team2 = to_winner[message.from_user.id]["team2"]
    bot.send_message(chat_id, team2 + " " + _("Score:"), reply_markup=markup)
    userStep[message.from_user.id] = 33


@bot.message_handler(func=lambda message: get_user_step(message.from_user.id) == 33)
def set_bet_db(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardRemove()
    if message.text == _("Cancel"):
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, _("Action cancelled."), reply_markup=markup)
        userStep[message.from_user.id] = None
        return

    if not message.text.isdigit():
        set_winner(message)
        return

    bot.send_message(chat_id, _("Winner correctly selected."), reply_markup=markup)
    query = get_matches()
    match = query.filter(Match.id == to_winner[message.from_user.id]["id"]).first()
    match.score1 = to_winner[message.from_user.id]["score1"]
    match.score2 = message.text

    update()
    query = get_bets()
    bets = query.filter(Bet.match == to_winner[message.from_user.id]["id"]).all()
    for b in bets:
        query = get_ranking()
        ranking = query.filter(Ranking.player_id == b.player_id).first()
        if not ranking:
            ranking = Ranking(player_id=b.player_id)
            add(ranking)
        ranking.total += 1
        winner = (
            "team1"
            if int(message.text) < int(to_winner[message.from_user.id]["score1"])
            else "team2"
        )
        if to_winner[message.from_user.id][winner] == b.bet:
            ranking.wins += 1
        update()
    userStep[message.from_user.id] = None