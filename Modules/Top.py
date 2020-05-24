@bot.message_handler(commands=["top10"])
def top_10(message):
    chat_id = message.chat.id
    query = get_ranking()
    rankings = query.order_by(Ranking.wins.desc()).order_by(Ranking.total.desc()).all()
    text = _("No user with any resolved bet.")
    if rankings:
        text = (
                emoji(":trophy:") + " " + _("TOP 10 WINS") + " " + emoji(":trophy:") + "\n"
        )
        text += "-----------------\n"

    query = get_users()
    count = 0
    for ra in rankings:
        if count == 10:
            break
        count += 1
        username = query.filter(User.player_id == ra.player_id).first()
        textu = "<pre>"
        textu += username.telegram
        textu += " " * (20 - len(textu)) + " "
        textu += "</pre>"
        # text += '{0: <15}'.format(username.telegram)
        textu += emoji(":trophy:") + " " + str(ra.wins)
        textu += emoji(":video_game:") + " " + str(ra.total) + "\n"
        text += textu
    bot.send_message(chat_id, text, parse_mode="html")


@bot.message_handler(commands=["top10rate"])
def top_10_rate(message):
    chat_id = message.chat.id
    query = get_ranking()
    session = get_session()
    rankings = session.execute(
        "select id, player_id, (wins * 100 / total) as percentage, total"
        " from ranking group by player_id, percentage, total, id "
        "having total > (select max(total) from ranking) / 2 "
        "order by percentage desc limit 10"
    ).fetchall()
    text = _("No user with any resolved bet.")

    if rankings:
        text = "🏆 TOP 10 WIN RATE 🏆 \n" if rankings else ""
        text += "═══════════════════\n"

    query = get_users()
    for ra in rankings:
        username = query.filter(User.player_id == ra[1]).first()
        # textu = '{0: <15}'.format(username.telegram)
        textu = "<pre>"
        textu += username.telegram
        textu += " " * (20 - len(textu)) + " "
        textu += "</pre>"
        textu += emoji(":game_die:")
        textu += " " + str(ra[2]) + "% \n"
        text += textu
    bot.send_message(chat_id, text, parse_mode="html")
