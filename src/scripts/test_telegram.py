import asyncio
from src.interface.telegram_service import send_alert
from src.utils.logger import logger

async def test():
    logger.info("Sending test alert...")
    await send_alert("🟢 *JARVIS System Update*\n\nYour Chat ID has been successfully registered. The automated push notification system (P3) is now ONLINE and ready to deliver Alpha Signals.")
    logger.info("Done.")

if __name__ == "__main__":
    asyncio.run(test())
