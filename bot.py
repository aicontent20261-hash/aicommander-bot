import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder # ОСЬ ЦЕЙ ІМПОРТ БУВ ПОТРІБЕН
import google.generativeai as genai
import os
import asyncio
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# 1. Твій токен Telegram і API ключ Gemini
TOKEN = "8539700014:AAE9Wl5lFJ-__c7XKZI4x2YTo7U8mFUf2e4"
API_KEY = "AIzaSyBMiTc6e24o5DD1sZH7Sc23pADX4k9rTZk"

# 2. Налаштування Gemini
genai.configure(api_key=API_KEY)

# ВАЖЛИВО: Використовуй саме цю назву моделі
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Вітаю у AiCommander! Бот запущено 24/7. Напишіть мені щось.")

@dp.message()
async def chat(message: types.Message):
    try:
        # 3. Виклик генерації
        response = model.generate_content(message.text)
        await message.answer(response.text)
    except Exception as e:
        await message.answer(f"⚠️ Помилка: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
# --- ДАНІ ---
TOKEN = "8539700014:AAE9Wl5lFJ-__c7XKZI4x2YTo7U8mFUf2e4"
GEMINI_KEY = "AIzaSyBMiTc6e24o5DD1sZH7Sc23pADX4k9rTZk"

# Налаштування Gemini
genai.configure(api_key=GEMINI_KEY, transport='rest')

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функція вибору моделі
def get_working_model():
    try:
        instruction = (
            "Ви — AiCommander, професійний інтелектуальний асистент, розроблений @dav_ps22. "
            "Ваш стиль спілкування: ввічливий, діловий та стриманий. "
            "Звертайтеся до користувача на 'Ви'. Уникайте сленгу та неформальних звертань. "
            "Ви маєте експертні знання в програмуванні, економіці, ресторанному бізнесі та спорті. "
            "Відповідайте завжди українською мовою, структуровано та чітко."
        )
        target_model = None
        for m in genai.list_models():
            if '1.5-flash' in m.name and 'generateContent' in m.supported_generation_methods:
                target_model = m.name
                break
        if not target_model:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    target_model = m.name
                    break
        print(f"✅ Вибрано модель: {target_model}")
        return genai.GenerativeModel(model_name=target_model, system_instruction=instruction)
    except Exception as e:
        print(f"❌ Помилка при виборі моделі: {e}")
        return None

active_model = get_working_model()

# Функція створення головного меню
def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🎨 Створити аватар")
    builder.button(text="📚 Допомога з завданнями")
    builder.button(text="🤝 Реферальна програма")
    builder.button(text="💎 Premium")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

# Команда /start
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    welcome_text = (
        "<b>Вітаємо у AiCommander!</b> 🚀\n\n"
        "Я — Ваш персональний інтелектуальний асистент. Я допоможу Вам у вирішенні "
        "складних навчальних завдань, розробці технічної документації для бізнесу "
        "та створенні візуального контенту.\n\n"
        "<b>Будь ласка, оберіть потрібний розділ меню:</b>"
    )
    await message.answer(welcome_text, parse_mode="HTML", reply_markup=main_menu())

# Обробка кнопок меню
@dp.message(lambda message: message.text in ["🎨 Створити аватар", "📚 Допомога з завданнями", "🤝 Реферальна програма", "💎 Premium"])
async def menu_handler(message: types.Message):
    if message.text == "🎨 Створити аватар":
        await message.answer("Будь ласка, опишіть бажане зображення. \n\n<i>Наприклад: 'Сучасний логотип у стилі мінімалізму'</i>", parse_mode="HTML")
    elif message.text == "📚 Допомога з завданнями":
        await message.answer("Надішліть, будь ласка, умову завдання або тему дослідження. Я підготую детальну відповідь. ✍️")
    elif message.text == "🤝 Реферальна програма":
        bot_info = await bot.get_me()
        ref_link = f"https://t.me/{bot_info.username}?start={message.from_user.id}"
        ref_text = (
            "<b>🤝 Партнерська програма</b>\n\n"
            "Запрошуйте нових користувачів та отримуйте додаткові запити як бонус.\n\n"
            f"🔗 <b>Ваше персональне посилання:</b>\n<code>{ref_link}</code>"
        )
        await message.answer(ref_text, parse_mode="HTML")
    elif message.text == "💎 Premium":
        await message.answer(
            "💎 <b>AICOMMANDER PREMIUM</b>\n\n"
            "• Пріоритетний доступ до моделі\n"
            "• Безлімітна генерація контенту\n\n"
            "Для оформлення підписки звертайтеся до адміністратора: @dav_ps22", 
            parse_mode="HTML"
        )

# Обробка звичайних текстових повідомлень (Gemini)
@dp.message()
async def handle_message(message: types.Message):
    global active_model
    if not active_model:
        active_model = get_working_model()
    
    try:
        response = active_model.generate_content(message.text)
        if response.text:
            await message.answer(response.text)
        else:
            await message.answer("⚠️ Бро, нейронка щось промовчала. Спробуй ще раз.")
    except Exception as e:
        if "429" in str(e):
            await message.answer("🔴 Бро, ліміти на сьогодні все. Модель 2.5 має всього 20 запитів. Чекаємо завтра або міняй ключ!")
        else:
            await message.answer(f"⚠️ Помилка: {e}")

# Запуск бота
async def main():
    print("🚀 Бот запускається...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
