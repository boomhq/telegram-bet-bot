#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unicodedata

import sys
import ast
import datetime
from Settings.settings import *
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, relationship, lazyload, subqueryload, lazyload_all, subqueryload_all, joinedload

from telebot import TeleBot, types
from emoji import emojize
from Models.betMODEL import (
    Match,
    Ranking,
    Bet,
    User,
    get_matches,
    get_bets,
    get_users,
    get_ranking,
    add,
    update,
    delete,
    get_session,
)

token = os.environ.get("BET_BOT_API_KEY")

# Getter for translation
_ = gettext

if not token:
    sys.exit(_("Add an enviroment variable $betBOT with your token."))

lang = os.environ.get("BET_BOT_LANG")
change_lang(lang)

administrators = ast.literal_eval(os.environ.get("BET_BOT_ADMINS"))

bot = TeleBot(token)
userStep = {}
knownUsers = []
to_add = {}
to_winner = {}
to_bet = {}
commands = {
    "help": _("Gives you information about the available commands"),
    "bet": _("Add a bet in a match"),
    "whobets": _("Show who have bet why"),
    "matches": _("Show active matches"),
    "mybets": _("Show your bet stats"),
    "history": _("Show match result history"),
    "top10": _("Shows the top 10 players with wins and totale"),
    "top10rate": _("Shows the top10 players ordered by win percentage"),
    "notify": _("Notify when a match is added."),
    "addmatch": _("Add a Match to bet on"),
    "deletematch": _("Remove a previously added match"),
    "setscore": _("Sets the score of an ended match."),
}

for module in enabled_modules:
    try:
        exec(open("./Modules/" + module + ".py").read())
        print("Enabled plugin " + module)
    except:
        print("Error enabling " + module)

bot.polling()
