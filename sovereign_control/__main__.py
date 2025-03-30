import asyncio
import logging
from pathlib import Path
import json

from .core import SovereignControlProtocol
from .security import SecurityProtocol
from .quantum import QuantumStateManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/sovereign.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def main():
    """Main entry point for the Sovereign Control Protocol."""
    try:
        # Load configuration
        config_path = Path("config/default_config.json")
        with open(config_path) as f:
            config = json.load(f)
        
        # Initialize components
        security = SecurityProtocol()
        quantum = QuantumStateManager()
        protocol = SovereignControlProtocol(security, quantum)
        
        # Start the interface
        logger.info("Starting Sovereign Control Protocol...")
        await protocol.start()
        
    except Exception as e:
        logger.error(f"Error starting protocol: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 