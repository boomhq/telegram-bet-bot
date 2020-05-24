@bot.message_handler(commands=["whobets", "whobet"])
def who_bet(message):
    if message.chat.type != "private":
        bot.send_message(
            message.chat.id, _("This command can not be used on group chats.")
        )
        return
    chat_id = message.chat.id
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
    userStep[message.from_user.id] = 100


@bot.message_handler(func=lambda message: get_user_step(message.from_user.id) == 100)
def confirm_match_choose(message):
    if message.text == _("Cancel"):
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, _("Action cancelled."), reply_markup=markup)
        userStep[message.from_user.id] = None
        return

    chat_id = message.chat.id
    markup = types.ReplyKeyboardRemove()

    bot.send_message(chat_id, _("Voici les paris enregistre pour ce match"), reply_markup=markup)

    mid = message.text.split(" ")
    queryMatch = get_matches()
    match = queryMatch.filter(Match.id == int(mid[0])).one()

    queryBets = get_bets()
    bets = queryBets.filter(Bet.match == int(mid[0])).options(joinedload('player')).all()
    text = ""
    for bet in bets:
        text += "Pseudo : * "+bet.player.telegram+" * Choix : *" + bet.bet + " *\n"

    markup = types.ReplyKeyboardRemove()
    bot.send_message(chat_id, text, reply_markup=markup, parse_mode="markdown")
    userStep[message.from_user.id] = None
