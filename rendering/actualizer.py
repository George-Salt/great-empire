import inquirer
import pyrebase
import telebot


BOT = telebot.TeleBot("6571625894:AAHS7lVGmpYMrhUpmDw6WkRO_yYNw9hcIFE")


def get_firebase_database():
    firebase_config = {
        "apiKey": "AIzaSyAH9gQ6Ycyc_N01IOL5Eub7qGNYuywdOU0",
        "authDomain": "our-atm.firebaseapp.com",
        "databaseURL": "https://our-atm-default-rtdb.firebaseio.com",
        "projectId": "our-atm",
        "storageBucket": "our-atm.appspot.com",
        "messagingSenderId": "821684806115",
        "appId": "1:821684806115:web:b25e5216fda188ea8f00d6",
        "measurementId": "G-5E4396GEEK"
    }
    firebase = pyrebase.initialize_app(firebase_config)

    database = firebase.database()
    return database


def get_user_variables(message: telebot.types.Message):
    user_id = str(message.from_user.id)
    user_name = message.from_user.first_name
    user_params = database.child("users").child(user_id).get()
    return user_id, user_name, user_params


def get_user_in_dict(user_params):
    user = {}
    for param in user_params.each():
        user[param.key()] = param.val()
    return user


def get_other_users_column(user_id):
    users_objects = database.child("users").get()
    users = []
    for user in users_objects:
        name = user.val()["name"]
        id = user.key()
        if id != user_id:
            users.append(f"👤 {id} ({name})")
    users_column = "\n".join(users)

    if users_column:
        return users_column
    else:
        return "⚠ Пользователей пока нет!"


def save_user(user_id, user):
    database.child("users").child(user_id).set(user)


@BOT.message_handler(commands=["admin"])
def admin(message: telebot.types.Message):
    BOT.send_message(message.chat.id, f"👋 Добро пожаловать в консоль Администратора!")
    BOT.send_message(message.chat.id, f"Выберите команду.\n\n/admin_add - добавить средства на счет пользователя\n/admin_deprive - изъять средства со счета пользователя")


@BOT.message_handler(commands=["start"])
def start(message: telebot.types.Message):
    user_id, user_name, user_params = get_user_variables(message)

    if not user_params.val():
        user = {
            "name": user_name,
            "money": 200
        }
        database.child("users").child(user_id).set(user)

        BOT.send_message(message.chat.id, f"👋 Добро пожаловать в игру, {user_name}!\n\n💳 Мы дарим вам 200 монет для успешного старта!")
    else:
        user = get_user_in_dict(user_params)
        user_money = user["money"]

        BOT.send_message(message.chat.id, f"👋 Добро пожаловать, {user_name}!\n\n💳 Ваш баланс: {user_money} монет.")
    show_commands(message)


def show_commands(message: telebot.types.Message):
    BOT.send_message(message.chat.id, f"Выберите команду.\n\n/transfer - перевести средства\n/profile - посмотреть профиль")


@BOT.message_handler(commands=["transfer"])
def transfer(message: telebot.types.Message):
    user_id, user_name, user_params = get_user_variables(message)
    user = get_user_in_dict(user_params)
    user_money = user["money"]

    users_column = get_other_users_column(user_id)

    message = BOT.send_message(message.chat.id, f"💳 Ваш баланс: {user_money} монет.\n\nКому желаете перевести деньги, {user_name}?\n\nСписок пользователей:\n{users_column}\n\n🆔 Введите ID получателя.")
    BOT.register_next_step_handler(message, get_recipient)


def get_recipient(message: telebot.types.Message):
    user_id, user_name, user_params = get_user_variables(message)
    user = get_user_in_dict(user_params)
    user_money = user["money"]

    recipient_id = message.text
    recipient_params = database.child("users").child(recipient_id).get()

    recipient = {}
    for param in recipient_params.each():
        recipient[param.key()] = param.val()

    message = BOT.send_message(message.chat.id, f"💳 Ваш баланс: {user_money} монет.\n\nКакую сумму вы желаете перевести пользователю, {user_name}?\n\n🔢 Введите число.")
    BOT.register_next_step_handler(message, transfer_money, recipient_id, recipient)


def transfer_money(message: telebot.types.Message, recipient_id, recipient):
    try:
        money_to_transfer = int(message.text)
        if money_to_transfer > 0:
            user_id, user_name, user_params = get_user_variables(message)
            user = get_user_in_dict(user_params)
            user_money = user["money"]

            recipient_name = recipient["name"]
            
            if user_money >= money_to_transfer:
                user_money -= money_to_transfer
                user["money"] = user_money
                save_user(user_id, user)

                recipient["money"] += money_to_transfer
                save_user(recipient_id, recipient)

                BOT.send_message(message.chat.id, f"✔ Выполнен перевод {money_to_transfer} монет пользователю {recipient_id} ({recipient_name}).\n\n💳 Ваш баланс: {user_money} монет.")
                if recipient_name != "BANK":
                    BOT.send_message(recipient_id, f"Поступил перевод {money_to_transfer} монет от пользователя {user_id} ({user_name}).")

            show_commands(message)
        else:
            BOT.send_message(message.chat.id, f"⚠ Неверная сумма! Повторите попытку!")
            transfer(message)
    except:
        BOT.send_message(message.chat.id, f"⚠ Произошла ошибка! Повторите попытку!")
        transfer(message)


@BOT.message_handler(commands=["profile"])
def profile(message: telebot.types.Message):
    user_id, user_name, user_params = get_user_variables(message)
    user = get_user_in_dict(user_params)
    user_money = user["money"]

    BOT.send_message(message.chat.id, f"📰 Информация о пользователе.\n\n👤 Имя: {user_name}\n🆔 ID: {user_id}\n💳 Баланс: {user_money} монет.")


if __name__ == "__main__":
    database = get_firebase_database()
    while True:
        try:
            BOT.polling(non_stop=True)
        except:
            continue
