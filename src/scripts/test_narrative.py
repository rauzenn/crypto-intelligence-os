from src.narrative.engine import NarrativeEngine2
from src.utils.logger import logger

def run_test():
    engine = NarrativeEngine2()
    
    logger.info("Testing Narrative Engine 2.0...")
    
    # 1. Process social mention
    logger.info("Simulating social mentions...")
    engine.process_social_event("I think autonomous agents will rule the world via AI.", "telegram_group_a", "user_1")
    engine.process_social_event("AI agents are launching their own tokens now.", "twitter", "user_2")
    
    # 2. Integrate Market Data
    logger.info("Integrating market data...")
    engine.integrate_market_data("AI", 1_500_000, 10.0)
    
    profile = engine.narratives["AI"]
    
    logger.info(f"Topic: {profile.topic}")
    logger.info(f"Lifecycle: {profile.lifecycle_state}")
    logger.info(f"Graph Nodes: {[n.name for n in profile.graph_nodes]}")
    logger.info(f"Confidence: {profile.confidence_score}")

if __name__ == "__main__":
    run_test()
