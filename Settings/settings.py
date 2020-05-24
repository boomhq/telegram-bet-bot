# Settings.py
import json
import os
from dotenv import load_dotenv

# Load .ENV
load_dotenv()
# Load Translation
lang = "en"
path = os.path.dirname(os.path.abspath(__file__))
enabled_modules = [
    "AddMatch",
    "Bet",
    "DeleteMatch",
    "Help",
    "ListMatch",
    "SetScore",
    "Top",
    "Users",
]

with open(path + "/../Translations/lang.json", encoding="utf8") as json_data:
    texts = json.load(json_data)


def change_lang(lan="fr"):
    global lang
    if texts.get(lan):
        lang = lan
    else:
        print("Language not translated yet.")
    return lang


def gettext(string):
    if texts.get(lang) and texts[lang].get(string):
        return texts[lang][string]
    return string
