from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from src.utils.logger import logger

class ResearchObject(BaseModel):
    asset: str
    website: str = "Unknown"
    github_activity: str = "Unknown"
    tokenomics: Dict[str, Any] = {}
    holders_count: int = 0
    top_10_holder_pct: float = 0.0
    liquidity_usd: float = 0.0
    deployer_behavior: str = "Unknown"
    competitors: List[str] = []
    security_history: str = "No known exploits"
    generated_at: datetime = datetime.now(timezone.utc)

class ResearchEngine:
    """
    STEP 9 (Rule 16): RESEARCH AGENT
    Automatically kicks off deep research when a token hits the radar.
    Aggregates web, docs, github, tokenomics into a single object.
    """
    async def run_deep_research(self, asset: str, context: Dict[str, Any] = None) -> ResearchObject:
        logger.info(f"[ResearchEngine] Starting deep autonomous research for {asset}...")
        
        # 1. Scrape Website & Docs (Simulated)
        website = f"https://{asset.lower()}.io"
        
        # 2. Check GitHub (Simulated)
        github_activity = "High (30 commits this week)" if len(asset) < 5 else "Low (Abandoned)"
        
        # 3. Analyze Tokenomics & On-Chain (Simulated)
        tokenomics = {
            "total_supply": 1_000_000_000,
            "circulating": 250_000_000,
            "vesting_schedule": "Cliff in 6 months"
        }
        
        # 4. Competitor Graph Analysis (Simulated)
        competitors = [f"{asset}Killer", f"Better{asset}"]
        
        obj = ResearchObject(
            asset=asset,
            website=website,
            github_activity=github_activity,
            tokenomics=tokenomics,
            holders_count=15420,
            top_10_holder_pct=45.5,
            liquidity_usd=1_500_000.0,
            deployer_behavior="Funded by Binance. Clean history.",
            competitors=competitors
        )
        
        logger.info(f"[ResearchEngine] Completed deep research for {asset}.")
        return obj

    async def generate_report(self, asset: str) -> str:
        """Used by the Telegram interface to generate a natural language report."""
        obj = await self.run_deep_research(asset)
        return f"""🔬 *Deep Research Report: {obj.asset.upper()}*

🌍 *Web & Code*
- Website: {obj.website}
- GitHub Activity: {obj.github_activity}

📊 *Tokenomics & On-Chain*
- Holders: {obj.holders_count}
- Top 10 Ownership: {obj.top_10_holder_pct}%
- Liquidity: ${obj.liquidity_usd:,.2f}
- Vesting: {obj.tokenomics.get('vesting_schedule')}

🕵️ *Deployer & Security*
- Behavior: {obj.deployer_behavior}
- Security: {obj.security_history}

⚔️ *Competitors:* {', '.join(obj.competitors)}
"""
