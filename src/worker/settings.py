from arq.connections import RedisSettings
from arq.cron import cron
from src.config.settings import settings
from src.worker.tasks import run_ingestion_cycle, run_wallet_hunter_cycle, run_outcome_evaluations, startup, shutdown
import urllib.parse

parsed_url = urllib.parse.urlparse(settings.REDIS_URL)

redis_settings = RedisSettings(
    host=parsed_url.hostname or 'localhost',
    port=parsed_url.port or 6379,
    password=parsed_url.password,
    database=int(parsed_url.path.strip('/')) if parsed_url.path.strip('/') else 0
)

class WorkerSettings:
    """
    ARQ Worker configuration
    """
    redis_settings = redis_settings
    
    # Run these on worker start/stop
    on_startup = startup
    on_shutdown = shutdown
    
    # Tasks that can be queued dynamically
    functions = [run_ingestion_cycle, run_wallet_hunter_cycle, run_outcome_evaluations]
    
    # Cron jobs that run automatically
    cron_jobs = [
        # Run ingestion every minute for testing (In production: every 5-10 minutes depending on rate limits)
        cron(run_ingestion_cycle, minute=set(range(0, 60, 5))),
        
        # Run Wallet Hunter once an hour
        cron(run_wallet_hunter_cycle, minute=0),
        
        # P2: Check alert outcomes every 15 minutes
        cron(run_outcome_evaluations, minute=set(range(0, 60, 15)))
    ]
