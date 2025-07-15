import os
import hmac
import hashlib
import json
import logging
import asyncio
from aiohttp import web, ClientSession
from typing import Dict, Any

logger = logging.getLogger(__name__)

class WebhookServer:
    def __init__(self, bot_handler):
        self.bot = bot_handler
        self.secret = os.getenv('WEBHOOK_SECRET', 'default-secret')
        self.port = int(os.getenv('WEBHOOK_PORT', '8080'))
        self.app = web.Application()
        self._setup_routes()
        
        logger.info(f"🔗 Webhook server initialized on port {self.port}")
    
    def _setup_routes(self):
        """Setup webhook routes"""
        self.app.router.add_post('/webhook/marzban', self.handle_marzban_webhook)
        self.app.router.add_get('/health', self.health_check)
    
    def _verify_signature(self, data: bytes, signature: str) -> bool:
        """Verify webhook signature"""
        try:
            expected_signature = hmac.new(
                self.secret.encode(), 
                data, 
                hashlib.sha256
            ).hexdigest()
            return hmac.compare_digest(expected_signature, signature)
        except Exception as e:
            logger.error(f"❌ Signature verification error: {e}")
            return False
    
    async def handle_marzban_webhook(self, request):
        """Handle webhooks from Marzban panel"""
        try:
            # Get signature from headers
            signature = request.headers.get('x-webhook-secret', '')
            
            # Read request body
            body = await request.read()
            
            # Verify signature
            if not self._verify_signature(body, signature):
                logger.warning("⚠️ Invalid webhook signature")
                return web.Response(status=403, text="Invalid signature")
            
            # Parse JSON payload
            try:
                payload = json.loads(body.decode('utf-8'))
            except json.JSONDecodeError:
                logger.error("❌ Invalid JSON in webhook payload")
                return web.Response(status=400, text="Invalid JSON")
            
            # Process the webhook event
            await self._process_webhook_event(payload)
            
            return web.Response(status=200, text="OK")
            
        except Exception as e:
            logger.error(f"❌ Webhook handling error: {e}")
            return web.Response(status=500, text="Internal server error")
    
    async def _process_webhook_event(self, payload: Dict[str, Any]):
        """Process webhook event from Marzban"""
        try:
            action = payload.get('action')
            username = payload.get('username')
            
            logger.info(f"📨 Webhook event: {action} for user: {username}")
            
            # Handle different event types
            if action == 'user_created':
                await self._handle_user_created(payload)
            
            elif action == 'user_updated':
                await self._handle_user_updated(payload)
            
            elif action == 'user_deleted':
                await self._handle_user_deleted(payload)
            
            elif action == 'user_limited':
                await self._handle_user_limited(payload)
            
            elif action == 'user_expired':
                await self._handle_user_expired(payload)
            
            else:
                logger.info(f"ℹ️ Unhandled webhook action: {action}")
                
        except Exception as e:
            logger.error(f"❌ Error processing webhook event: {e}")
    
    async def _handle_user_created(self, payload: Dict[str, Any]):
        """Handle user creation event"""
        username = payload.get('username')
        logger.info(f"✅ User created: {username}")
        
        # Here you could notify admins or send welcome messages
        # For now, just log the event
    
    async def _handle_user_updated(self, payload: Dict[str, Any]):
        """Handle user update event"""
        username = payload.get('username')
        logger.info(f"🔄 User updated: {username}")
    
    async def _handle_user_deleted(self, payload: Dict[str, Any]):
        """Handle user deletion event"""
        username = payload.get('username')
        logger.info(f"🗑️ User deleted: {username}")
    
    async def _handle_user_limited(self, payload: Dict[str, Any]):
        """Handle user traffic limit reached"""
        username = payload.get('username')
        logger.info(f"⚠️ User traffic limited: {username}")
        
        # Here you could send notification to user about traffic limit
        # This would require storing user telegram IDs
    
    async def _handle_user_expired(self, payload: Dict[str, Any]):
        """Handle user expiration event"""
        username = payload.get('username')
        logger.info(f"⏰ User expired: {username}")
        
        # Here you could send expiration notification to user
    
    async def health_check(self, request):
        """Health check endpoint"""
        return web.Response(
            status=200, 
            text=json.dumps({
                "status": "healthy",
                "service": "marzban-ai-bot-webhook"
            }),
            content_type='application/json'
        )
    
    async def start(self):
        """Start the webhook server"""
        try:
            logger.info(f"🚀 Starting webhook server on port {self.port}")
            
            runner = web.AppRunner(self.app)
            await runner.setup()
            
            site = web.TCPSite(runner, '0.0.0.0', self.port)
            await site.start()
            
            logger.info(f"✅ Webhook server started successfully")
            
            # Keep the server running
            while True:
                await asyncio.sleep(3600)  # Sleep for 1 hour
                
        except Exception as e:
            logger.error(f"❌ Failed to start webhook server: {e}")
            raise