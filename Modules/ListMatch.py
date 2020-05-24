@bot.message_handler(commands=["matchs"])
def list_bets(message):
    query = get_matches()
    matches = query.filter(Match.score1 == None).all()
    text = (
            "*************************"
            + " \n"
            + _("Faites /bet pour vous positionnez sur un match")
            + " \n"
            + _("Faites /whobets pour voir les positions des autres personnes")
            + " \n"
            + "*************************"
            + " \n"
    )
    query = get_bets()
    for m in matches:
        bets = query.filter(Bet.match == m.id).all()
        date = m.start_date.strftime("%d-%m-%Y")
        hour = m.start_date.strftime("%H:%M")
        bets1 = 0
        bets2 = 0
        for b in bets:
            if b.bet == m.team1:
                bets1 += 1
            elif b.bet == m.team2:
                bets2 += 1
        odd1 = 0
        odd2 = 0
        if bets1 or bets2:
            odd1 = bets1 * 100 / (bets1 + bets2)
            odd2 = bets2 * 100 / (bets1 + bets2)
        text += (
                " *"
                + "========================="
                + "\n"
                + m.title
                + "* "
                + "\n"
                + _('Fin de la prise des paris')
                + date
                + " "
                + _('at')
                + hour
                + " "
                + "\n"
                + " *"
                + m.team1
                + "* "
                + str(odd1)
                + "%"
                + " "
                + emoji(":vs:")
                + " "
                + str(odd2)
                + "% *"
                + m.team2
                + "\n"
                + "========================="
                + "*\n"
        )
    if not matches:
        bot.send_message(message.chat.id, _("No matches available."))
    else:
        bot.send_message(message.chat.id, text, parse_mode="markdown")
