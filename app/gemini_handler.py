import os
import json
import logging
import google.generativeai as genai
from typing import Dict, Any

logger = logging.getLogger(__name__)

class GeminiHandler:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # System prompt for customer support
        self.system_prompt = """
شما یک دستیار پشتیبانی هوشمند برای سرویس VPN هستید. وظیفه شما کمک به کاربران در موارد زیر است:

**عملیات ممکن:**
- REQUEST_ACCOUNT: درخواست اکانت جدید
- CHECK_ACCOUNT: بررسی وضعیت اکانت (نیاز به username)
- RENEW_ACCOUNT: تمدید اشتراک (نیاز به username)
- GET_CONFIG: دریافت فایل کانفیگ (نیاز به username)
- HELP_SETUP: راهنمایی نصب و استفاده
- HELP_TROUBLESHOOT: عیب‌یابی مشکلات
- CONTACT_SUPPORT: ارتباط با پشتیبانی انسانی
- NONE: فقط پاسخ دادن بدون عملیات خاص

**قوانین مهم:**
1. همیشه به فارسی پاسخ دهید
2. دوستانه و مؤدب باشید
3. اگر username لازم است ولی داده نشده، آن را درخواست کنید
4. برای مسائل پیچیده، کاربر را به پشتیبانی انسانی هدایت کنید
5. اطلاعات امنیتی مثل رمز عبور را هرگز درخواست نکنید

**فرمت پاسخ:**
پاسخ را در قالب JSON ارائه دهید:
{
  "response": "پاسخ دوستانه به کاربر",
  "action": "نوع عملیات",
  "parameters": {
    "username": "نام کاربری اگر مشخص شده",
    "request_type": "نوع درخواست"
  },
  "confidence": 0.95
}
        """
        
        logger.info("🧠 Gemini AI handler initialized")
    
    def check_status(self) -> bool:
        """Check if Gemini AI is working"""
        try:
            # Simple test generation
            response = self.model.generate_content("سلام")
            return bool(response.text)
        except Exception as e:
            logger.error(f"❌ Gemini status check failed: {e}")
            return False
    
    async def process_message(self, message: str) -> Dict[str, Any]:
        """Process user message with Gemini AI"""
        try:
            # Create full prompt
            full_prompt = f"""
{self.system_prompt}

**پیام کاربر:** "{message}"

لطفاً پاسخ مناسب را در قالب JSON ارائه دهید.
            """
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            
            if not response.text:
                return self._fallback_response("متأسفانه نتوانستم پیام شما را پردازش کنم.")
            
            # Try to parse JSON response
            try:
                result = json.loads(response.text.strip())
                
                # Validate response structure
                if not isinstance(result, dict) or 'response' not in result:
                    raise ValueError("Invalid response structure")
                
                # Set defaults
                result.setdefault('action', 'NONE')
                result.setdefault('parameters', {})
                result.setdefault('confidence', 0.8)
                
                logger.info(f"🧠 AI processed message with action: {result.get('action')}")
                return result
                
            except (json.JSONDecodeError, ValueError) as e:
                logger.warning(f"⚠️ Failed to parse AI response as JSON: {e}")
                # Extract text response if JSON parsing fails
                return self._fallback_response(response.text)
                
        except Exception as e:
            logger.error(f"❌ Error processing message with Gemini: {e}")
            return self._fallback_response(
                "متأسفانه در حال حاضر مشکلی در سیستم هوش مصنوعی وجود دارد. "
                "لطفاً دوباره تلاش کنید یا با پشتیبانی تماس بگیرید."
            )
    
    def _fallback_response(self, text: str) -> Dict[str, Any]:
        """Create fallback response when AI processing fails"""
        return {
            "response": text,
            "action": "NONE",
            "parameters": {},
            "confidence": 0.5
        }
    
    def _detect_intent(self, message: str) -> str:
        """Simple intent detection as fallback"""
        message_lower = message.lower()
        
        # Account requests
        if any(word in message_lower for word in ['اکانت جدید', 'حساب جدید', 'یوزر جدید']):
            return 'REQUEST_ACCOUNT'
        
        # Status check
        if any(word in message_lower for word in ['وضعیت', 'چک', 'بررسی']):
            return 'CHECK_ACCOUNT'
        
        # Config request
        if any(word in message_lower for word in ['کانفیگ', 'فایل', 'لینک']):
            return 'GET_CONFIG'
        
        # Renewal
        if any(word in message_lower for word in ['تمدید', 'شارژ', 'تجدید']):
            return 'RENEW_ACCOUNT'
        
        # Help
        if any(word in message_lower for word in ['راهنما', 'کمک', 'نصب']):
            return 'HELP_SETUP'
        
        return 'NONE'