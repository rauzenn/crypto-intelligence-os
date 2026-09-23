from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from src.config.settings import settings
from src.utils.logger import logger
import asyncio

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN) if settings.TELEGRAM_BOT_TOKEN else None
dp = Dispatcher()

@dp.message(Command("radar"))
async def cmd_radar(message: types.Message):
    await message.answer("Alpha Radar is scanning... No new anomalies detected currently.")

@dp.message(Command("status"))
async def cmd_status(message: types.Message):
    await message.answer("Crypto Intelligence OS v0.1 is online.")

async def start_bot():
    if not bot:
        logger.warning("TELEGRAM_BOT_TOKEN is not set. Bot will not start.")
        return
    logger.info("Starting Telegram bot...")
    await dp.start_polling(bot)

async def send_alert(text: str):
    if not bot or not settings.TELEGRAM_CHAT_ID:
        logger.warning("Bot token or Chat ID not configured. Cannot send alert.")
        return
    try:
        await bot.send_message(chat_id=settings.TELEGRAM_CHAT_ID, text=text, parse_mode="Markdown")
        logger.info("Alert sent to Telegram successfully.")
    except Exception as e:
        logger.error(f"Failed to send Telegram alert: {e}")
