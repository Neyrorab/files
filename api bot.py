import requests
import asyncio
import nest_asyncio  # Нужно установить
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# === Настройки ===
TELEGRAM_BOT_TOKEN = '6903853942:AAFCLWr5LdKaqqcYosCG00pn3JmlBzgzl7w'  # Заменить на токен вашего бота
DEEPSEEK_API_KEY = 'sk-aaa1984ad9514b5cab4755fa9c940932'  # Заменить на ваш API ключ

API_URL = "https://api.deepseek.com/v1/chat/completions" 

HEADERS = {
    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Применяем патч для поддержки вложенных циклов событий
nest_asyncio.apply()

# === Функция для отправки запроса к DeepSeek API ===
def get_deepseek_response(question: str) -> str:
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": question}
        ],
        "temperature": 0.7,
        "max_tokens": 1024
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Ошибка API: {response.status_code}, {response.text}"
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"

# === Обработчик входящих сообщений ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text("Подождите, я думаю...")

    bot_response = get_deepseek_response(user_message)
    await update.message.reply_text(bot_response)

# === Основная функция запуска бота ===
async def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    app.add_handler(handler)
    await app.run_polling()

# Запуск
if __name__ == '__main__':
    asyncio.run(main())