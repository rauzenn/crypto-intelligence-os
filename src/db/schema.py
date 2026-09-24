from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, JSON, Text
from datetime import datetime, timezone
import os
from src.config.settings import settings

def get_utc_now():
    return datetime.now(timezone.utc)

Base = declarative_base()

class EventModel(Base):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(String, index=True, nullable=False)
    chain = Column(String, index=True, nullable=False)
    wallet = Column(String, index=True, nullable=True)
    asset = Column(String, index=True, nullable=True)
    timestamp = Column(DateTime, default=get_utc_now, index=True)
    source = Column(String, nullable=False)
    raw_reference = Column(String, nullable=False, unique=True)
    metadata_json = Column(JSON, default=dict)

class AlertModel(Base):
    __tablename__ = 'alerts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    asset = Column(String, nullable=True)
    chain = Column(String, nullable=True)
    detected_at = Column(DateTime, default=get_utc_now, index=True)
    content_json = Column(JSON, nullable=False) # Stores the rest of the alert data
    
class AlertOutcomeModel(Base):
    """
    P2 Learning Loop: Tracks the outcome of an alert at various time snapshots.
    """
    __tablename__ = 'alert_outcomes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    alert_id = Column(Integer, index=True, nullable=False)
    snapshot_time = Column(String, index=True, nullable=False) # e.g. "1h", "6h", "24h"
    price_at_alert = Column(String, nullable=True)
    price_at_snapshot = Column(String, nullable=True)
    pnl_pct = Column(String, nullable=True)
    is_false_positive = Column(String, nullable=True) # "true", "false", or "pending"
    recorded_at = Column(DateTime, default=get_utc_now)

engine = create_async_engine(settings.DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
