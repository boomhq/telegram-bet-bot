@bot.message_handler(commands=["deletematch"])
def del_match(message):
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
    matches = query.filter(Match.score1 == None).all()
    markup = types.ReplyKeyboardMarkup(row_width=len(matches))
    for m in matches:
        markup.add(str(m.id) + " " + m.title + " " + m.team1 + " " + m.team2)
    if not matches:
        bot.send_message(message.chat.id, _("No matches available."))
        return
    markup.add(_("Cancel"))
    bot.send_message(chat_id, _("Choose a match:"), reply_markup=markup)
    userStep[message.from_user.id] = 41


@bot.message_handler(func=lambda message: get_user_step(message.from_user.id) == 41)
def del_match_db(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardRemove()
    match = message.text.split(" ")
    try:
        response = _("Match correctly deleted.")
        query = get_matches()
        query.filter(Match.id == int(match[0])).delete()
        delete(Match, Match.id == int(match[0]))
    except ValueError:
        response = _("Action canceled")
    bot.send_message(chat_id, response, reply_markup=markup)
    userStep[message.from_user.id] = None
