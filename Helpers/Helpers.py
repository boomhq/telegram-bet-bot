def get_user(message):
    player_id = message.from_user.id
    query = get_users()
    user = query.filter(User.player_id == player_id).first()
    if user and user.telegram != message.from_user.first_name:
        user.telegram = unicodedata.normalize(
            "NFC", message.from_user.first_name
        ).encode("ascii", "ignore")
        update()
    if not user:
        user = User(player_id=message.from_user.id, telegram=message.from_user.username)
        add(user)

def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]

def emoji(code):
    return emojize(code, use_aliases=True)