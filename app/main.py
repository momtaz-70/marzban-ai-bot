#!/usr/bin/env python3
"""
Marzban AI Customer Support Bot
A Telegram bot with Gemini AI integration for Marzban panel customer support
"""

import asyncio
import logging
import os
from dotenv import load_dotenv

from bot_handler import MarzbanAIBot
from webhook_server import WebhookServer

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def main():
    """Main function to start the bot and webhook server"""
    try:
        logger.info("🚀 Starting Marzban AI Bot...")
        
        # Initialize bot
        bot = MarzbanAIBot()
        
        # Initialize webhook server for Marzban events
        webhook_server = WebhookServer(bot)
        
        # Start both services
        await asyncio.gather(
            bot.start(),
            webhook_server.start()
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to start bot: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user")
    except Exception as e:
        logger.error(f"💥 Bot crashed: {e}")
        exit(1)