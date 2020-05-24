@bot.message_handler(commands=["mestats"])
def mestats(message):
    chat_id = message.chat.id
    query = get_ranking()
    ra = query.filter(Ranking.player_id == message.from_user.id).first()
    query = get_users()
    username = query.filter(User.player_id == message.from_user.id).first()
    text = _("You do not have any resolved bet yet.")
    if username and username.telegram and ra:
        text = username.telegram.encode("UTF-8")
        text += emoji(":trophy:") + " " + str(ra.wins) + " \n"
        text += emoji(":1234:") + " " + str(ra.total) + " \n"
        text += (
                emoji(":chart_with_upwards_trend:")
                + " "
                + str(ra.wins * 100 / ra.total)
                + "%"
        )
    bot.send_message(chat_id, text)


@bot.message_handler(commands=["mybets"])
def mybets(message):
    query = get_bets()
    bets = query.filter(Bet.player_id == message.from_user.id).all()
    text = ""
    query = get_matches()
    for b in bets:
        m = query.filter(Match.id == b.match).first()
        if m and (m.start_date > datetime.datetime.now() or m.score1 == None):
            text += (
                    m.title
                    + " "
                    + m.team1
                    + " "
                    + emoji(":vs:")
                    + " "
                    + m.team2
                    + " - "
                    + emoji(":video_game:")
                    + " <b>"
                    + b.bet
                    + "</b>\n"
            )
    if not bets or not text:
        bot.send_message(message.chat.id, _("No bets available."))
    else:
        bot.send_message(message.chat.id, text, parse_mode="html")


@bot.message_handler(commands=["history"])
def history(message):
    query = get_matches()
    matches = (
        query.filter(
            Match.start_date > datetime.datetime.now() - datetime.timedelta(days=5)
        )
            .filter(Match.score1 != None)
            .all()
    )
    text = ""
    count = 0
    for m in matches:
        if count == 10:
            return
        count += 1
        winner = "TBD"
        score1 = str(m.score1) + " " if m.score1 or m.score1 == 0 else ""
        score2 = str(m.score2) + " " if m.score2 or m.score1 == 0 else ""
        if m.score2 or m.score2 == 0 and m.score1 or m.score1 == 0:
            winner = m.team1 if m.score2 < m.score1 else m.team2
        text += (
                m.title + " "
                          "<b> "
                + score1
                + "</b> "
                + m.team1
                + " "
                + emoji(":vs:")
                + " <b>"
                + score2
                + "</b> "
                + " "
                + m.team2
                + " - "
                + emoji(":trophy:")
                + " <b>"
                + winner
                + "</b>\n"
        )
    if not matches:
        bot.send_message(message.chat.id, _("No bets available."))
    else:
        bot.send_message(message.chat.id, text, parse_mode="html")


@bot.message_handler(commands=["notify"])
def notify(message):
    chat_id = message.chat.id
    if chat_id != message.from_user.id:
        bot.send_message(
            message.chat.id, _("This command can not be used on group chats.")
        )
        return
    chat_id = message.chat.id
    query = get_users()
    user = query.filter(User.player_id == message.from_user.id).first()
    if user.notify:
        user.notify = 0
        bot.send_message(chat_id, _("You will no longer be notified."))
    else:
        user.notify = 1
        bot.send_message(chat_id, _("You will be notified when a match is added."))
    update()