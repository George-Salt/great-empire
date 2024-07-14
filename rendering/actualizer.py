import telebot


MEMBERS = ["george20097", ""]

BOT = telebot.TeleBot("6502376077:AAH3drxuzjip8LNFojiPwJOdjtv5sMszmrk", parse_mode="Markdown")


@BOT.message_handler(commands=["start"])
def start(message: telebot.types.Message):
    auth_player(message)


def auth_player(message):
    bot_message = BOT.send_message(message.chat.id, "Кто ты такой? Напиши сюда свой ник в War Thunder без собачки и названия полка.")

    BOT.register_next_step_handler(bot_message, open_website)


def open_website(message):
    nick = message.text

    if nick in MEMBERS:
        bot_message = BOT.send_message(message.chat.id, f"Окей, ты - @{nick}. Теперь зайди на [страницу информации](https://warthunder.com/ru/community/userinfo/?nick={nick}). Как будешь готов, отправь любое сообщение.")
        BOT.register_next_step_handler(bot_message, get_level, nick)
    else:
        bot_message = BOT.send_message(message.chat.id, f"⚠ БАМ! {nick} не состоит в полку =I22I=. Если хочешь вступить в полк, напиши /join.")



def get_level(message, nick):
    nick = message.text

    bot_message = BOT.send_message(message.chat.id, f"Окей, ты - {nick}. Теперь зайди на [страницу информации](https://warthunder.com/ru/community/userinfo/?nick={nick}). Как будешь готов, отправь любое сообщение.")

    BOT.register_next_step_handler(bot_message, get_level, nick)


if __name__ == "__main__":
    BOT.infinity_polling()
