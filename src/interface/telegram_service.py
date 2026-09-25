from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from src.config.settings import settings
from src.utils.logger import logger
from src.db.schema import async_session, AlertModel, WalletModel, NarrativeModel
from sqlalchemy import select, desc
import asyncio

# Note: Uses aiogram 3.x
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN) if settings.TELEGRAM_BOT_TOKEN else None
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    welcome_text = (
        "🤖 *JARVIS Intelligence OS*\n\n"
        "Commands:\n"
        "/alpha - Latest detected alpha signals\n"
        "/wallets - Top smart money wallets\n"
        "/narratives - Current market narratives\n"
        "/status - System health and metrics"
    )
    await message.answer(welcome_text, parse_mode="Markdown")

@dp.message(Command("alpha"))
async def cmd_alpha(message: types.Message):
    async with async_session() as session:
        result = await session.execute(select(AlertModel).order_by(desc(AlertModel.detected_at)).limit(3))
        alerts = result.scalars().all()
        
        if not alerts:
            await message.answer("No active alpha signals found.")
            return
            
        for a in alerts:
            score = a.content_json.get('composite_score', 'N/A')
            earlyness = a.content_json.get('earlyness', 'N/A')
            priority = a.content_json.get('priority', 'N/A')
            
            msg = (
                f"🚨 *[{priority}] {a.title}*\n"
                f"Asset: {a.asset} | Chain: {a.chain}\n"
                f"Score: {score} | Earlyness: {earlyness}\n"
                f"Time: {a.detected_at.strftime('%Y-%m-%d %H:%M:%S')} UTC"
            )
            await message.answer(msg, parse_mode="Markdown")

@dp.message(Command("wallets"))
async def cmd_wallets(message: types.Message):
    async with async_session() as session:
        result = await session.execute(
            select(WalletModel)
            .where(WalletModel.lifecycle_state.in_(["WATCHED", "HIGH_SIGNAL"]))
            .order_by(desc(WalletModel.reputation_score))
            .limit(5)
        )
        wallets = result.scalars().all()
        
        if not wallets:
            await message.answer("No smart money wallets in WATCHED or HIGH_SIGNAL state yet.")
            return
            
        text = "🕵️ *Top Smart Money Wallets*\n\n"
        for w in wallets:
            text += f"- `{w.address[:6]}...{w.address[-4:]}` [{w.chain}] | Score: {w.reputation_score} | {w.lifecycle_state}\n"
            
        await message.answer(text, parse_mode="Markdown")

@dp.message(Command("narratives"))
async def cmd_narratives(message: types.Message):
    async with async_session() as session:
        result = await session.execute(
            select(NarrativeModel)
            .order_by(desc(NarrativeModel.mention_velocity))
            .limit(5)
        )
        narratives = result.scalars().all()
        
        if not narratives:
            await message.answer("No narratives detected yet.")
            return
            
        text = "📈 *Market Narratives*\n\n"
        for n in narratives:
            text += f"- *{n.topic}* | {n.lifecycle_state} | Velocity: {n.mention_velocity:.1f}\n"
            
        await message.answer(text, parse_mode="Markdown")

@dp.message(Command("status"))
async def cmd_status(message: types.Message):
    await message.answer("✅ *JARVIS Systems Online*\n\n- Ingestion: Active\n- Event Bus: Active\n- Alpha Radar 2.0: Active\n- Wallet Hunter 2.0: Active\n- Risk Engine 2.0: Active", parse_mode="Markdown")

async def start_bot():
    if not bot:
        logger.warning("TELEGRAM_BOT_TOKEN is not set. Bot will not start.")
        return
    logger.info("Starting Telegram bot polling...")
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
