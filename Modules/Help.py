@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    cid = message.chat.id
    query = get_users()
    user = query.filter(User.player_id == message.from_user.id).first()
    help_text = _("Talk me in private to get the command list.")
    if user:
        cid = message.from_user.id
        help_text = _("The following commands are available:") + "\n"
        for key in commands:
            help_text += "/" + key + ": "
            help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)
