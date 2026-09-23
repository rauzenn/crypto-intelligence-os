from src.config.settings import sources_config
from src.utils.logger import logger
from src.sources.adapters.coingecko import CoinGeckoAdapter
from src.sources.adapters.defillama import DefiLlamaAdapter
from src.sources.adapters.dexscreener import DexScreenerAdapter
from src.sources.adapters.helius import HeliusAdapter
from src.sources.adapters.alchemy import AlchemyAdapter
from src.sources.adapters.news import NewsAdapter
from src.sources.adapters.telegram_ingest import TelegramIngestAdapter

class SourceRegistry:
    def __init__(self):
        self.adapters = {}
        self._initialize_adapters()
        
    def _initialize_adapters(self):
        # Market
        if sources_config.get("market", {}).get("coingecko", {}).get("enabled"):
            self.adapters["coingecko"] = CoinGeckoAdapter()
            logger.info("CoinGecko adapter initialized.")
            
        # DeFi
        if sources_config.get("defi", {}).get("defillama", {}).get("enabled"):
            self.adapters["defillama"] = DefiLlamaAdapter()
            logger.info("DeFiLlama adapter initialized.")
            
        # DEX
        if sources_config.get("dex", {}).get("dexscreener", {}).get("enabled"):
            self.adapters["dexscreener"] = DexScreenerAdapter()
            logger.info("DexScreener adapter initialized.")
            
        # Solana
        if sources_config.get("solana", {}).get("helius", {}).get("enabled"):
            self.adapters["helius"] = HeliusAdapter()
            logger.info("Helius adapter initialized.")
            
        # EVM
        if sources_config.get("evm", {}).get("alchemy", {}).get("enabled"):
            self.adapters["alchemy"] = AlchemyAdapter()
            logger.info("Alchemy adapter initialized.")
            
        # News
        if sources_config.get("news", {}).get("generic_web_research", {}).get("enabled"):
            self.adapters["news"] = NewsAdapter()
            logger.info("News adapter initialized.")
            
        # Social
        if sources_config.get("social", {}).get("telegram", {}).get("enabled"):
            self.adapters["telegram_ingest"] = TelegramIngestAdapter()
            logger.info("Telegram ingest adapter initialized.")
        
    def get_adapter(self, name: str):
        return self.adapters.get(name)
        
    def get_all_active(self):
        return list(self.adapters.values())
        
    async def close_all(self):
        for adapter in self.adapters.values():
            await adapter.close()

registry = SourceRegistry()
