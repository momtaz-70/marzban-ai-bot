import os
import aiohttp
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class MarzbanAPI:
    def __init__(self):
        self.base_url = os.getenv('MARZBAN_URL').rstrip('/')
        self.username = os.getenv('MARZBAN_USERNAME')
        self.password = os.getenv('MARZBAN_PASSWORD')
        self.token = None
        self.session = None
        
        logger.info(f"🔗 Marzban API initialized for {self.base_url}")
    
    async def _get_session(self):
        """Get or create aiohttp session"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def _authenticate(self):
        """Authenticate with Marzban API and get token"""
        try:
            session = await self._get_session()
            
            auth_data = {
                'username': self.username,
                'password': self.password
            }
            
            async with session.post(
                f"{self.base_url}/api/admin/token",
                data=auth_data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    self.token = data.get('access_token')
                    logger.info("✅ Successfully authenticated with Marzban")
                    return True
                else:
                    logger.error(f"❌ Authentication failed: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Authentication error: {e}")
            return False
    
    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None):
        """Make authenticated request to Marzban API"""
        if not self.token:
            if not await self._authenticate():
                return None
        
        try:
            session = await self._get_session()
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            }
            
            url = f"{self.base_url}{endpoint}"
            
            async with session.request(method, url, json=data, headers=headers) as response:
                if response.status == 401:  # Token expired
                    logger.info("🔄 Token expired, re-authenticating...")
                    if await self._authenticate():
                        headers['Authorization'] = f'Bearer {self.token}'
                        async with session.request(method, url, json=data, headers=headers) as retry_response:
                            if retry_response.status == 200:
                                return await retry_response.json()
                    return None
                
                elif response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"❌ API request failed: {response.status} - {await response.text()}")
                    return None
                    
        except Exception as e:
            logger.error(f"❌ Request error: {e}")
            return None
    
    async def check_connection(self) -> bool:
        """Check if connection to Marzban is working"""
        try:
            result = await self._make_request('GET', '/api/system')
            return result is not None
        except:
            return False
    
    async def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user information"""
        try:
            result = await self._make_request('GET', f'/api/user/{username}')
            if result:
                logger.info(f"📊 Retrieved user info for: {username}")
            return result
        except Exception as e:
            logger.error(f"❌ Error getting user {username}: {e}")
            return None
    
    async def create_user(self, username: str, data_limit: int = 10737418240, expire_days: int = 30) -> Optional[Dict[str, Any]]:
        """Create a new user"""
        try:
            import time
            expire_timestamp = int(time.time()) + (expire_days * 24 * 60 * 60)
            
            user_data = {
                "username": username,
                "data_limit": data_limit,  # 10GB default
                "expire": expire_timestamp,
                "status": "active",
                "proxies": {
                    "vless": {},
                    "vmess": {}
                },
                "inbounds": {
                    "vless": [],
                    "vmess": []
                }
            }
            
            result = await self._make_request('POST', '/api/user', user_data)
            if result:
                logger.info(f"✅ Created user: {username}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error creating user {username}: {e}")
            return None
    
    async def modify_user(self, username: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Modify user settings"""
        try:
            result = await self._make_request('PUT', f'/api/user/{username}', kwargs)
            if result:
                logger.info(f"✅ Modified user: {username}")
            return result
        except Exception as e:
            logger.error(f"❌ Error modifying user {username}: {e}")
            return None
    
    async def reset_user_traffic(self, username: str) -> Optional[Dict[str, Any]]:
        """Reset user traffic usage"""
        try:
            result = await self._make_request('POST', f'/api/user/{username}/reset')
            if result:
                logger.info(f"🔄 Reset traffic for user: {username}")
            return result
        except Exception as e:
            logger.error(f"❌ Error resetting traffic for {username}: {e}")
            return None
    
    async def get_user_subscription(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user subscription information"""
        try:
            user_info = await self.get_user(username)
            if user_info and 'subscription_url' in user_info:
                return {
                    'subscription_url': user_info['subscription_url'],
                    'links': user_info.get('links', [])
                }
            return None
        except Exception as e:
            logger.error(f"❌ Error getting subscription for {username}: {e}")
            return None
    
    async def get_system_stats(self) -> Optional[Dict[str, Any]]:
        """Get system statistics"""
        try:
            result = await self._make_request('GET', '/api/system')
            return result
        except Exception as e:
            logger.error(f"❌ Error getting system stats: {e}")
            return None
    
    async def close(self):
        """Close the session"""
        if self.session:
            await self.session.close()
            logger.info("🔒 Marzban API session closed")