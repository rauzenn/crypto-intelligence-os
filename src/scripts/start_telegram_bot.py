import asyncio
from src.interface.telegram_service import start_bot
from src.utils.logger import logger
import sys

if __name__ == "__main__":
    logger.info("Initializing Telegram Bot Subsystem...")
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
    except Exception as e:
        logger.error(f"Bot execution failed: {e}")
        sys.exit(1)
