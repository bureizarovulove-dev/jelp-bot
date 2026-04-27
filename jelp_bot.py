"""
Telegram бот JELP - генератор помощи
Используйте: @jelp в любом чате для выбора уровня помощи (как @pic @gif)
"""

import logging
import random
import uuid
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, CommandHandler, InlineQueryHandler, ContextTypes
from config import TOKEN, BOT_USERNAME
from responses import get_response

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик inline query для @jelp"""
    percentage = random.randint(0, 100)
    message = get_response(percentage)

    results = [
        InlineQueryResultArticle(
            id=str(uuid.uuid4()),
            title="jelp",
            description="Посмотрите сколько вам нужно jelp 👀",
            input_message_content=InputTextMessageContent(message)
        )
    ]

    await update.inline_query.answer(results, cache_time=0, is_personal=True)
    logger.info(f"inline_query: {message}")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    welcome_message = f"""
👋 Привет! Я бот JELP!

Я помогаю определить, насколько вам нужна помощь! 

📝 Как пользоваться:
Напишите @{BOT_USERNAME} в любом чате - появится список вариантов!

Выберите уровень помощи:
• 0% - Вы полностью здоровы 🟢
• 10% - Всё хорошо 🟢
• 20% - Небольшие проблемы 🟡
• 30-50% - Нужна помощь 🟠
• 60-70% - Срочно нужна помощь 🔴
• 80-90% - Очень срочно!!! 🔴
• 100% - ПОЛНАЯ КАТАСТРОФА!!! 🔴

Или выберите случайный вариант 🎲

Попробуйте прямо сейчас: напишите @{BOT_USERNAME} в любом чате!
    """
    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    help_message = f"""
📖 Справка по боту JELP:

Использование:
Напишите @{BOT_USERNAME} в любом чате, и вы увидите список вариантов помощи.
Выберите нужный процент, и бот отправит результат в чат!

Примеры:
• @jelp 0% - Вы полностью здоровы! Все хорошо! 🟢
• @jelp 50% - Вам нужна помощь. Обратитесь к специалисту. 🟠
• @jelp 87% - Вам срочно нужна помощь! Это серьёзно! 🔴
• @jelp 100% - ПОЛНАЯ КАТАСТРОФА!!! ПОМОГИТЕ МНЕ!!! 🔴

Команды:
/start - Приветствие
/help - Эта справка

Уровни помощи:
🟢 0-10% - Полностью здоровы
🟡 11-30% - Небольшие проблемы
🟠 31-50% - Нужна помощь
🔴 51-70% - Срочно нужна помощь
🔴 71-90% - ОЧЕНЬ СРОЧНО!
🔴 91-100% - ПОЛНАЯ КАТАСТРОФА!
    """
    await update.message.reply_text(help_message)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка ошибок"""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)


def main() -> None:
    """Запуск бота"""
    # Проверяем, что токен установлен
    if TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("❌ ОШИБКА: Установите токен бота в файле config.py!")
        print("\n⚠️  ВАЖНО: Перейдите в файл config.py и замените YOUR_BOT_TOKEN_HERE на ваш реальный токен!")
        print("Получить токен можно у BotFather в Telegram (@BotFather)\n")
        return
    
    # Создаём приложение
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # Обработчик для inline query (@jelp в чате)
    application.add_handler(InlineQueryHandler(inline_query))

    # Обработчик ошибок
    application.add_error_handler(error_handler)

    # Запускаем бота
    logger.info("✅ Бот запущен! Нажмите Ctrl+C для остановки.")
    print("\n" + "="*60)
    print("🤖 JELP БОТ ЗАПУЩЕН!")
    print("="*60)
    print(f"✅ Бот работает в режиме INLINE QUERY")
    print(f"📝 Напишите @{BOT_USERNAME} в любом чате Telegram")
    print(f"📋 Выберите нужный вариант из предложенных")
    print("🔧 Нажмите Ctrl+C для остановки")
    print("="*60 + "\n")
    
    application.run_polling()


if __name__ == '__main__':
    main()
