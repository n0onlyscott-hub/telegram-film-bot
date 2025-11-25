import telebot
from telebot import types
import time
import os
from flask import Flask
import threading

# Flask app для порта
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Bot is running!"

TOKEN = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(TOKEN)

CHANNEL = "@bot_shook"  # ⚠️ ЗАМЕНИ НА СВОЙ КАНАЛ!

FILMS = """🎬 ВАШ СПИСОК ФИЛЬМОВ:

1. "Начало" - 8.7/10 ⭐
2. "Матрица" - 8.7/10 ⭐  
3. "Интерстеллар" - 8.6/10 ⭐
4. "Побег из Шоушенка" - 9.1/10 ⭐
5. "Криминальное чтиво" - 8.9/10 ⭐"""

def check_sub(user_id):
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    if check_sub(message.from_user.id):
        send_films(message.chat.id)
    else:
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("📺 ПОДПИСАТЬСЯ", url=f"https://t.me/{CHANNEL[1:]}")
        btn2 = types.InlineKeyboardButton("✅ Я ПОДПИСАЛСЯ", callback_data="check")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, "Подпишись для доступа к фильмам!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check")
def check(call):
    if check_sub(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ Доступ открыт!")
        send_films(call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, "❌ Сначала подпишись!")

def send_films(chat_id):
    bot.send_message(chat_id, FILMS)

def run_bot():
    print("🚀 Telegram бот запущен!")
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"Ошибка бота: {e}")
            time.sleep(10)

def run_web():
    port = int(os.environ.get('PORT', 10000))
    print(f"🌐 Web сервер запущен на порту {port}")
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Запускаем web сервер
    run_web()
