import os
import telebot
from telebot import types

TOKEN = os.getenv("TOKEN")
ADMIN_CHAT_ID = -5187651629
SITE_URL = "https://emperiorsworld-32c5a.web.app"

bot = telebot.TeleBot(TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton("🌐 Открыть сайт", url=SITE_URL))
    markup.add(types.InlineKeyboardButton("📝 Подать заявку", callback_data="apply"))
    markup.add(types.InlineKeyboardButton("👑 О клане", callback_data="about"))

    bot.send_message(
        message.chat.id,
        "👑 Добро пожаловать в Emperiors World!\n\nВыбери действие:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "apply":
        user_data[call.message.chat.id] = {}
        bot.send_message(call.message.chat.id, "📝 Напиши свой ник в Roblox:")
        bot.register_next_step_handler(call.message, get_nick)

    elif call.data == "about":
        bot.send_message(
            call.message.chat.id,
            "👑 Emperiors World — клан Blox Fruits.\n\n"
            "Здесь ты можешь подать заявку и открыть сайт клана."
        )

def get_nick(message):
    user_data[message.chat.id]["nick"] = message.text
    bot.send_message(message.chat.id, "🎂 Сколько тебе лет?")
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    user_data[message.chat.id]["age"] = message.text

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("1 Division", "2 Division", "3 Division")

    bot.send_message(message.chat.id, "⚔️ В какой дивизион хочешь?", reply_markup=markup)
    bot.register_next_step_handler(message, get_division)

def get_division(message):
    user_data[message.chat.id]["division"] = message.text
    bot.send_message(message.chat.id, "🏆 Сколько у тебя баунти?", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_bounty)

def get_bounty(message):
    user_data[message.chat.id]["bounty"] = message.text
    bot.send_message(message.chat.id, "❓ Почему хочешь вступить в Emperiors World?")
    bot.register_next_step_handler(message, get_reason)

def get_reason(message):
    data = user_data[message.chat.id]
    data["reason"] = message.text

    username = message.from_user.username
    user_link = f"@{username}" if username else "Без username"

    application = f"""
📝 НОВАЯ ЗАЯВКА В КЛАН

👤 Telegram: {user_link}
🎮 Ник Roblox: {data['nick']}
🎂 Возраст: {data['age']}
⚔️ Дивизион: {data['division']}
🏆 Баунти: {data['bounty']}

❓ Причина:
{data['reason']}
"""

    bot.send_message(ADMIN_CHAT_ID, application)
    bot.send_message(message.chat.id, "✅ Заявка отправлена! Ожидай ответа от глав клана.")

    user_data.pop(message.chat.id, None)

bot.infinity_polling()