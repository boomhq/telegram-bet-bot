import unicodedata

import datetime
from Settings.settings import *
from telebot import types
from Models.betMODEL import (
    Match,
    Bet,
    User,
    get_matches,
    get_bets,
    get_users,
    add,
    update,
)
# Getter for translation
_ = gettext
userStep = {}
to_bet = {}

@bot.message_handler(commands=["addmatch"])
def add_match(message):
    if message.from_user.id not in administrators:
        bot.send_message(message.chat.id, _("You can not use this command."))
        return
    if message.chat.id != message.from_user.id:
        bot.send_message(
            message.chat.id, _("This command can not be used on group chats.")
        )
        return
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, _("Title bet"), reply_markup=markup)
    to_add[message.from_user.id] = {}
    userStep[message.from_user.id] = 20


@bot.message_handler(func=lambda message: get_user_step(message.from_user.id) == 20)
def msg_add_match_team1(message):
    to_add[message.from_user.id]["Title"] = message.text
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, _("Team A name:"), reply_markup=markup)
    userStep[message.from_user.id] = 21


@bot.message_handler(func=lambda message: get_user_step(message.from_user.id) == 21)
def msg_add_match_team1(message):
    markup = types.ForceReply(selective=False)
    to_add[message.from_user.id]["Team1"] = message.text
    bot.send_message(message.chat.id, _("Team B name:"), reply_markup=markup)
    userStep[message.from_user.id] = 22


@bot.message_handler(func=lambda message: get_user_step(message.from_user.id) == 22)
def msg_add_match_team2(message):
    to_add[message.from_user.id]["Team2"] = message.text
    markup = types.ForceReply(selective=False)
    bot.send_message(message.chat.id, _("Match date:"), reply_markup=markup)
    userStep[message.from_user.id] = 23


@bot.message_handler(func=lambda message: get_user_step(message.from_user.id) == 23)
def msg_add_match_date(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardRemove()
    bot.send_message(chat_id, _("Date set correctly."), reply_markup=markup)
    markup = types.ForceReply(selective=False)
    to_add[message.from_user.id]["date"] = message.text
    bot.send_message(message.chat.id, _("Match hour:"), reply_markup=markup)
    userStep[message.from_user.id] = 24


@bot.message_handler(func=lambda message: get_user_step(message.from_user.id) == 24)
def msg_add_match_hour(message):
    to_add[message.from_user.id]["hour"] = message.text
    add_match_db(message)


def add_match_db(message):
    userStep[message.from_user.id] = None
    teams = to_add[message.from_user.id]
    date = teams["date"] + " " + teams["hour"]
    try:
        date_time = datetime.datetime.strptime(date, "%d-%m-%Y %H:%M")
    except ValueError:
        bot.send_message(
            message.chat.id, _("The format of the date/hour is " + "incorrect.")
        )
        return

    new_match = Match(
        title=teams["Title"],
        team1=teams["Team1"],
        team2=teams["Team2"],
        start_date=date_time,
    )
    try:
        add(new_match)
    except Exception:
        bot.send_message(message.chat.id, _("An error ocurred adding the" + "match."))
        return
    bot.send_message(message.chat.id, _("Added correctly."))
    # Notify
    query = get_users()
    notify = query.filter(User.notify == 1).all()
    for u in notify:
        try:
            bot.send_message(
                u.player_id,
                _("New match added %(3)s - %(1)s %(vs)s %(2)s")
                % {
                    "1": teams["Team1"],
                    "vs": emoji(":vs:"),
                    "2": teams["Team2"],
                    "3": teams["title"],
                },
            )
        except Exception:
            # Set notify to 0 if error (because user stopped bot /stop)
            user = query.filter(User.player_id == message.from_user.id).first()
            user.notify = 0
            update()