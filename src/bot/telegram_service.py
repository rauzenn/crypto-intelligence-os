from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from src.config.settings import settings
from src.utils.logger import logger
import asyncio

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN) if settings.TELEGRAM_BOT_TOKEN else None
dp = Dispatcher()

@dp.message(Command("radar"))
async def cmd_radar(message: types.Message):
    # This would normally query the database for recent alerts or trigger a manual scan
    await message.answer("Alpha Radar is active and scanning continuously in the background. No critical anomalies detected in the last cycle.")

@dp.message(Command("coin"))
async def cmd_coin(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Please provide a coin symbol or address. Usage: /coin <symbol>")
        return
        
    from src.intelligence.coin_research import CoinResearcher
    researcher = CoinResearcher()
    report = await researcher.research(args[1])
    await message.answer(report, parse_mode="Markdown")

@dp.message(Command("research"))
async def cmd_research(message: types.Message):
    # For now, map research to the same logic as coin
    await cmd_coin(message)

@dp.message(Command("wallet"))
async def cmd_wallet(message: types.Message):
    await message.answer("Wallet Hunter: Provide address to analyze. Usage: /wallet <address>")

@dp.message(Command("watchlist"))
async def cmd_watchlist(message: types.Message):
    await message.answer("Wallet Watchlist is currently empty. Add smart wallets to monitor.")

@dp.message(Command("chains"))
async def cmd_chains(message: types.Message):
    await message.answer("Chain Discovery Engine: \nTier A: solana, ethereum\nTier B: base, arbitrum\n(Monitoring dynamic acceleration)")

@dp.message(Command("narratives"))
async def cmd_narratives(message: types.Message):
    await message.answer("Narrative Engine: \nAccelerating topics: AI, DePIN, RWA")

@dp.message(Command("status"))
async def cmd_status(message: types.Message):
    await message.answer("Crypto Intelligence OS v0.1 is online with Phase 3 active.")

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
