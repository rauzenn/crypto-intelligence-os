from fastapi import FastAPI
from src.config.settings import settings
from src.utils.logger import logger
from src.db.schema import init_db

app = FastAPI(title="Crypto Intelligence OS", version="0.1.0")

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Crypto Intelligence OS API...")
    try:
        await init_db()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENV,
        "version": "0.1.0"
    }

@app.get("/status")
async def status_check():
    return {
        "system": "Crypto Intelligence OS",
        "status": "operational",
        "modules": {
            "api": "ok",
            "db": "checking",
            "redis": "checking"
        }
    }
