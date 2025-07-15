# 🤖 Marzban AI Customer Support Bot

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-green.svg)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)
![Gemini](https://img.shields.io/badge/Google-Gemini%20AI-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**یک بات پشتیبانی هوشمند برای کاربران پنل مرزبان**

[نصب و راه‌اندازی](#-نصب-و-راه‌اندازی) • [ویژگی‌ها](#-ویژگی‌ها) • [مستندات](#-مستندات) • [پشتیبانی](#-پشتیبانی)

</div>

## 🚀 معرفی

این بات یک دستیار هوشمند برای پشتیبانی از کاربران VPN است که با استفاده از هوش مصنوعی Google Gemini، به صورت خودکار به سوالات کاربران پاسخ می‌دهد و عملیات مختلف روی پنل مرزبان انجام می‌دهد.

### 🛠️ تکنولوژی‌های استفاده شده
- **Python 3.11+** - زبان برنامه‌نویسی اصلی
- **Telegram Bot API** - رابط کاربری
- **Google Gemini AI** - پردازش زبان طبیعی
- **Marzban API** - مدیریت کاربران VPN
- **Docker & Docker Compose** - containerization
- **aiohttp** - وب سرور async برای webhook ها

## ✨ ویژگی‌ها

### 🎯 خدمات خودکار
- ✅ **درخواست اکانت جدید** - ثبت درخواست و هماهنگی با پشتیبانی
- ✅ **بررسی وضعیت اکانت** - نمایش اطلاعات کامل کاربر
- ✅ **تمدید اشتراک** - راهنمایی فرآیند تمدید
- ✅ **دریافت فایل کانفیگ** - ارائه لینک اشتراک و راهنمای نصب
- ✅ **پشتیبانی چندزبانه** - فارسی و انگلیسی

### 🧠 هوش مصنوعی پیشرفته
- 🤖 **درک زبان طبیعی** - پردازش پیام‌های فارسی و انگلیسی
- 🎯 **تشخیص هدف** - شناسایی خودکار نوع درخواست کاربر
- 💬 **پاسخ‌های طبیعی** - تولید پاسخ‌های دوستانه و مفید
- 🔄 **یادگیری تطبیقی** - بهبود عملکرد بر اساس تعاملات

### 🔧 مدیریت پیشرفته
- 📊 **مانیتورینگ real-time** - نظارت بر وضعیت سیستم
- 🔔 **Webhook integration** - دریافت رویدادهای مرزبان
- 🛡️ **امنیت بالا** - احراز هویت و کنترل دسترسی
- 📝 **لاگ‌گیری کامل** - ثبت تمام فعالیت‌ها

## 🏗️ معماری سیستم

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   کاربر تلگرام   │ ←→ │   AI Bot         │ ←→ │  Marzban Panel  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              ↕                         ↕
                       ┌──────────────────┐    ┌─────────────────┐
                       │   Gemini AI      │    │   Webhooks      │
                       └──────────────────┘    └─────────────────┘
```

## 🚀 نصب و راه‌اندازی

### پیش‌نیازها
- Docker & Docker Compose
- Telegram Bot Token
- Google Gemini API Key
- دسترسی به پنل مرزبان

### نصب سریع
```bash
# کلون کردن پروژه
git clone https://github.com/your-repo/marzban-ai-bot.git
cd marzban-ai-bot

# تنظیم متغیرهای محیطی
cp .env.example .env
nano .env

# اجرای container
docker-compose up -d
```

📖 **راهنمای کامل:** [SETUP.md](SETUP.md)

## 💬 نمونه استفاده

```
👤 کاربر: سلام، اکانت جدید می‌خوام

🤖 بات: سلام! 😊
درخواست شما برای ایجاد اکانت جدید ثبت شد.
پشتیبانی ما در اسرع وقت با شما تماس خواهد گرفت.

🕐 زمان پاسخ: معمولاً کمتر از 2 ساعت
📞 پشتیبانی: @support_username

---

👤 کاربر: وضعیت اکانت user123 چطوره؟

🤖 بات: 👤 اطلاعات اکانت

🏷️ نام کاربری: user123
✅ وضعیت: active
📊 مصرف: 2.50 GB از 10.00 GB
📅 تاریخ ایجاد: 2024-01-15
⏰ انقضا: 2024-02-15

🔗 لینک اشتراک: 
`https://panel.com/sub/token123`
```

## 🔧 پیکربندی

### متغیرهای محیطی
```env
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token

# Google Gemini AI
GEMINI_API_KEY=your_gemini_key

# Marzban Panel
MARZBAN_URL=https://your-panel.com
MARZBAN_USERNAME=admin
MARZBAN_PASSWORD=password

# Security
WEBHOOK_SECRET=secure_secret
ALLOWED_USERS=123456789,987654321
```

### Docker Compose
```yaml
version: '3.8'
services:
  marzban-ai-bot:
    build: .
    restart: unless-stopped
    ports:
      - "8080:8080"
    volumes:
      - ./logs:/app/logs
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      # ... other variables
```

## 📊 مانیتورینگ

### Health Check
```bash
curl http://localhost:8080/health
```

### لاگ‌ها
```bash
# مشاهده لاگ‌های زنده
docker-compose logs -f

# لاگ‌های فایل
tail -f logs/bot.log
```

### آمار عملکرد
- 📈 تعداد پیام‌های پردازش شده
- ⚡ زمان پاسخ‌گویی
- 🎯 دقت تشخیص هدف
- 🔄 وضعیت اتصالات

## 🛡️ امنیت

- 🔐 **احراز هویت قوی** با Bearer Token
- 🔒 **رمزنگاری webhook** با HMAC-SHA256
- 👥 **کنترل دسترسی** کاربران مجاز
- 📝 **لاگ‌گیری امنیتی** تمام فعالیت‌ها
- 🛡️ **محافظت در برابر حملات** rate limiting

## 🔄 آپدیت و نگهداری

### آپدیت خودکار
```bash
# دانلود آپدیت‌ها
git pull

# rebuild و restart
docker-compose down
docker-compose up -d --build
```

### بک‌آپ
```bash
# بک‌آپ تنظیمات و لاگ‌ها
tar -czf backup-$(date +%Y%m%d).tar.gz .env logs/
```

## 🤝 مشارکت

ما از مشارکت شما استقبال می‌کنیم! 

### نحوه مشارکت:
1. Fork کردن پروژه
2. ایجاد branch جدید (`git checkout -b feature/amazing-feature`)
3. Commit تغییرات (`git commit -m 'Add amazing feature'`)
4. Push به branch (`git push origin feature/amazing-feature`)
5. ایجاد Pull Request

### گزارش باگ
لطفاً باگ‌ها را در [Issues](https://github.com/your-repo/issues) گزارش دهید.

## 📄 مجوز

این پروژه تحت مجوز MIT منتشر شده است. برای جزئیات بیشتر فایل [LICENSE](LICENSE) را مطالعه کنید.

## 📞 پشتیبانی

- 📧 **ایمیل:** support@yourcompany.com
- 💬 **تلگرام:** [@your_support_bot](https://t.me/your_support_bot)
- 🐛 **گزارش باگ:** [GitHub Issues](https://github.com/your-repo/issues)
- 📖 **مستندات:** [Wiki](https://github.com/your-repo/wiki)

---

<div align="center">

**ساخته شده با ❤️ برای جامعه ایرانی**

[⭐ ستاره بدهید](https://github.com/your-repo) • [🍴 Fork کنید](https://github.com/your-repo/fork) • [📢 اشتراک‌گذاری](https://twitter.com/intent/tweet?text=Check%20out%20this%20amazing%20Marzban%20AI%20Bot!)

</div>

## نصب و راه‌اندازی

1. تنظیم متغیرهای محیطی
2. وارد کردن workflow به n8n
3. راه‌اندازی Telegram Bot
4. اتصال به Marzban Panel

## پیکربندی

فایل `.env` را با اطلاعات زیر پر کنید:
```
TELEGRAM_BOT_TOKEN=your_bot_token
GEMINI_API_KEY=your_gemini_key
MARZBAN_URL=your_marzban_url
MARZBAN_USERNAME=admin_username
MARZBAN_PASSWORD=admin_password
```