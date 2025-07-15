import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from marzban_api import MarzbanAPI
from gemini_handler import GeminiHandler

logger = logging.getLogger(__name__)

class MarzbanAIBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.allowed_users = self._parse_allowed_users()
        
        # Initialize services
        self.marzban = MarzbanAPI()
        self.gemini = GeminiHandler()
        
        # Initialize Telegram bot
        self.app = Application.builder().token(self.token).build()
        self._setup_handlers()
        
        logger.info("✅ Bot initialized successfully")
    
    def _parse_allowed_users(self):
        """Parse allowed users from environment variable"""
        users_str = os.getenv('ALLOWED_USERS', '')
        if not users_str:
            return []
        return [int(user_id.strip()) for user_id in users_str.split(',') if user_id.strip()]
    
    def _setup_handlers(self):
        """Setup bot command and message handlers"""
        # Commands
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("status", self.status_command))
        
        # Messages
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Error handler
        self.app.add_error_handler(self.error_handler)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_id = update.effective_user.id
        
        welcome_message = """
🤖 **سلام! به بات پشتیبانی VPN خوش آمدید**

من می‌تونم کمکتون کنم با:
• درخواست اکانت جدید
• بررسی وضعیت اکانت
• تمدید اشتراک
• دریافت فایل کانفیگ
• راهنمایی نصب و استفاده

فقط کافیه سوالتون رو بپرسید! 😊

**مثال‌ها:**
- "اکانت جدید می‌خوام"
- "وضعیت اکانت user123 چطوره؟"
- "چطور تو گوشیم نصب کنم؟"
        """
        
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
        logger.info(f"👋 User {user_id} started the bot")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🆘 **راهنمای استفاده**

**دستورات موجود:**
• `/start` - شروع کار با بات
• `/help` - نمایش این راهنما
• `/status` - وضعیت سیستم

**خدمات:**
🔹 **درخواست اکانت:** "اکانت جدید می‌خوام"
🔹 **بررسی وضعیت:** "وضعیت اکانت [نام کاربری]"
🔹 **تمدید اشتراک:** "تمدید اکانت [نام کاربری]"
🔹 **دریافت کانفیگ:** "فایل کانفیگ [نام کاربری]"
🔹 **راهنمایی نصب:** "چطور نصب کنم؟"

فقط کافیه سوالتون رو به زبان ساده بپرسید! 🤖
        """
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        try:
            # Check Marzban connection
            marzban_status = await self.marzban.check_connection()
            
            # Check Gemini AI
            gemini_status = self.gemini.check_status()
            
            status_text = f"""
📊 **وضعیت سیستم**

🔗 **اتصال مرزبان:** {'✅ متصل' if marzban_status else '❌ قطع'}
🧠 **هوش مصنوعی:** {'✅ فعال' if gemini_status else '❌ غیرفعال'}
🤖 **بات:** ✅ فعال

آخرین بروزرسانی: {self._get_current_time()}
            """
            
            await update.message.reply_text(status_text, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error in status command: {e}")
            await update.message.reply_text("❌ خطا در دریافت وضعیت سیستم")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle user messages with AI processing"""
        user_id = update.effective_user.id
        message_text = update.message.text
        
        # Check if user is allowed (if restriction is enabled)
        if self.allowed_users and user_id not in self.allowed_users:
            await update.message.reply_text("❌ شما مجاز به استفاده از این بات نیستید.")
            return
        
        try:
            logger.info(f"📨 Message from {user_id}: {message_text}")
            
            # Send typing indicator
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
            
            # Process with Gemini AI
            ai_response = await self.gemini.process_message(message_text)
            
            # Execute action if needed
            if ai_response.get('action') != 'NONE':
                result = await self._execute_action(ai_response, user_id)
                if result:
                    ai_response['response'] += f"\n\n{result}"
            
            # Send response
            await update.message.reply_text(
                ai_response['response'], 
                parse_mode='Markdown'
            )
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await update.message.reply_text(
                "❌ متأسفانه خطایی رخ داد. لطفاً دوباره تلاش کنید یا با پشتیبانی تماس بگیرید."
            )
    
    async def _execute_action(self, ai_response, user_id):
        """Execute the action determined by AI"""
        action = ai_response.get('action')
        parameters = ai_response.get('parameters', {})
        
        try:
            if action == 'REQUEST_ACCOUNT':
                return await self._handle_account_request(parameters, user_id)
            
            elif action == 'CHECK_ACCOUNT':
                username = parameters.get('username')
                if username:
                    return await self._handle_account_check(username)
                else:
                    return "❓ لطفاً نام کاربری را مشخص کنید"
            
            elif action == 'GET_CONFIG':
                username = parameters.get('username')
                if username:
                    return await self._handle_get_config(username)
                else:
                    return "❓ لطفاً نام کاربری را مشخص کنید"
            
            elif action == 'RENEW_ACCOUNT':
                username = parameters.get('username')
                if username:
                    return await self._handle_renew_account(username)
                else:
                    return "❓ لطفاً نام کاربری را مشخص کنید"
            
        except Exception as e:
            logger.error(f"Error executing action {action}: {e}")
            return "❌ خطا در انجام عملیات. لطفاً با پشتیبانی تماس بگیرید."
        
        return None
    
    async def _handle_account_request(self, parameters, user_id):
        """Handle new account request"""
        # This would typically involve creating a support ticket
        # or forwarding to admin for manual processing
        return """
📝 **درخواست اکانت جدید ثبت شد**

درخواست شما برای ایجاد اکانت جدید ثبت شد.
پشتیبانی ما در اسرع وقت با شما تماس خواهد گرفت.

🕐 زمان پاسخ: معمولاً کمتر از 2 ساعت
📞 پشتیبانی: @support_username
        """
    
    async def _handle_account_check(self, username):
        """Handle account status check"""
        user_info = await self.marzban.get_user(username)
        if user_info:
            return self._format_user_info(user_info)
        else:
            return f"❌ کاربر '{username}' یافت نشد"
    
    async def _handle_get_config(self, username):
        """Handle config file request"""
        config_info = await self.marzban.get_user_subscription(username)
        if config_info:
            return f"""
📱 **فایل کانفیگ آماده است**

🔗 **لینک اشتراک:** 
`{config_info['subscription_url']}`

📋 **راهنمای نصب:**
1. لینک بالا را کپی کنید
2. در اپلیکیشن VPN خود وارد کنید
3. روی "اتصال" کلیک کنید

💡 **اپلیکیشن‌های پیشنهادی:**
• اندروید: V2rayNG
• iOS: FairVPN
• ویندوز: V2rayN
            """
        else:
            return f"❌ اطلاعات کانفیگ برای '{username}' یافت نشد"
    
    async def _handle_renew_account(self, username):
        """Handle account renewal request"""
        # This would typically involve payment processing
        return f"""
💳 **درخواست تمدید اکانت '{username}'**

برای تمدید اکانت خود، لطفاً:
1. مبلغ مورد نظر را واریز کنید
2. فیش واریزی را ارسال کنید
3. منتظر تأیید پشتیبانی باشید

💰 **تعرفه‌ها:**
• یک ماهه: 50,000 تومان
• سه ماهه: 140,000 تومان
• شش ماهه: 270,000 تومان

📞 **پشتیبانی:** @support_username
        """
    
    def _format_user_info(self, user_info):
        """Format user information for display"""
        status_emoji = {
            'active': '✅',
            'disabled': '❌',
            'limited': '⚠️',
            'expired': '⏰'
        }.get(user_info.get('status', 'unknown'), '❓')
        
        # Convert bytes to GB
        used_gb = user_info.get('used_traffic', 0) / (1024**3)
        limit_gb = user_info.get('data_limit', 0) / (1024**3) if user_info.get('data_limit') else 'نامحدود'
        
        return f"""
👤 **اطلاعات اکانت**

🏷️ **نام کاربری:** {user_info.get('username')}
{status_emoji} **وضعیت:** {user_info.get('status')}
📊 **مصرف:** {used_gb:.2f} GB از {limit_gb} GB
📅 **تاریخ ایجاد:** {user_info.get('created_at', 'نامشخص')}
⏰ **انقضا:** {user_info.get('expire', 'نامحدود')}

🔗 **لینک اشتراک:** 
`{user_info.get('subscription_url', 'موجود نیست')}`
        """
    
    def _get_current_time(self):
        """Get current time in Persian format"""
        from datetime import datetime
        return datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Update {update} caused error {context.error}")
    
    async def start(self):
        """Start the bot"""
        logger.info("🚀 Starting Telegram bot...")
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()
        
        # Keep running
        await self.app.updater.idle()
    
    async def stop(self):
        """Stop the bot"""
        logger.info("🛑 Stopping Telegram bot...")
        await self.app.stop()