import telebot
from telebot import types
import os
import time

# Токен бота (добавим в настройках позже)
TOKEN = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(TOKEN)

# 📢 ЗАМЕНИТЕ НА ВАШ КАНАЛ!
CHANNEL = "@kinoshook"  # 

# 🎬 Список фильмов (можно менять)
FILMS = """🎬 ЭКСКЛЮЗИВНЫЙ СПИСОК ФИЛЬМОВ:

🔥 ТОП-10 ШЕДЕВРОВ КИНО:

1. "Начало" (Inception) - 8.7/10 ⭐
2. "Матрица" - 8.7/10 ⭐  
3. "Интерстеллар" - 8.6/10 ⭐
4. "Побег из Шоушенка" - 9.1/10 ⭐
5. "Криминальное чтиво" - 8.9/10 ⭐
6. "Король Лев" - 8.8/10 ⭐
7. "Форрест Гамп" - 8.8/10 ⭐
8. "Список Шиндлера" - 9.0/10 ⭐
9. "Зеленая миля" - 9.1/10 ⭐
10. "Леон" - 8.5/10 ⭐

💎 Подписка открывает доступ к постоянным обновлениям!"""

# 🔍 Проверка подписки
def check_sub(user_id):
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# 🚀 Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.first_name
    if check_sub(message.from_user.id):
        send_films(message.chat.id)
    else:
        show_subscription_request(message, name)

# 📺 Запрос подписки
def show_subscription_request(message, name):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("📺 ПОДПИСАТЬСЯ НА КАНАЛ", url=f"https://t.me/{CHANNEL[1:]}")
    btn2 = types.InlineKeyboardButton("✅ Я ПОДПИСАЛСЯ", callback_data="check")
    markup.add(btn1)
    markup.add(btn2)
    
    bot.send_message(
        message.chat.id,
        f"👋 Привет, {name}!\n\n"
        "🎥 Чтобы получить эксклюзивный список лучших фильмов, и узнать название фильмов/сериалов, "
        "подпишись на наш киноканал!\n\n"
        "👇 Нажми кнопку ниже:",
        reply_markup=markup
    )

# 🔘 Проверка подписки
@bot.callback_query_handler(func=lambda call: call.data == "check")
def check(call):
    if check_sub(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ Отлично! Вот твой список фильмов! Приятного просмотра!")
        send_films(call.message.chat.id)
    else:
        bot.answer_callback_query(call.id, "❌ Ты еще не подписался на канал!")

# 📨 Отправка фильмов
def send_films(chat_id):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("📺 ПЕРЕЙТИ В КАНАЛ", url=f"https://t.me/{CHANNEL[1:]}")
    markup.add(btn)
    
    bot.send_message(chat_id, FILMS, reply_markup=markup)
    print(f"✅ Выдали фильмы пользователю {chat_id}")

# 🏃 Запуск бота
print("🚀 Кино-бот запущен!")
while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(f"🔧 Перезапуск: {e}")
        time.sleep(10)
