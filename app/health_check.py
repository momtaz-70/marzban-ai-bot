#!/usr/bin/env python3
"""
Health check script for Docker container
"""

import sys
import asyncio
import aiohttp
import os

async def check_health():
    """Check if the bot services are healthy"""
    try:
        # Check webhook server
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:8080/health', timeout=5) as response:
                if response.status != 200:
                    print("❌ Webhook server health check failed")
                    return False
        
        print("✅ All services healthy")
        return True
        
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(check_health())
    sys.exit(0 if result else 1)