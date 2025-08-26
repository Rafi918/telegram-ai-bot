#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
بوت تلجرام ذكي متعدد النماذج باستخدام مكتبة RanaGPT
يدعم الدردشة الخاصة والمجموعات مع أقسام ذكاء اصطناعي متعددة
"""

import logging
import asyncio
from typing import Dict, Any
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# استيراد مكتبة RanaGPT
from RanaGPT import TextAi, BlackBox, GeminiApi, ImageAi

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# توكن البوت - يجب استبداله بالتوكن الحقيقي
BOT_TOKEN = "7925535525:AAF22RBu2X6p1NFU3C6Dybe-kwcFc7v3RFw"

# تخزين اختيارات المستخدمين للنماذج
user_models: Dict[int, str] = {}

# النماذج المتاحة
AVAILABLE_MODELS = {
    "deepseek": "🧠 DeepSeek V3 (DeepInfra)",
    "blackbox_gpt4": "🤖 GPT-4 (BlackBox)",
    "blackbox_gpt4o": "⚡ GPT-4o (BlackBox)",
    "gemini": "💎 Gemini AI",
    "image_ai": "🎨 مولد الصور"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالج أمر /start"""
    user = update.effective_user
    chat_type = update.effective_chat.type
    
    if chat_type == 'private':
        # رسالة ترحيب للدردشة الخاصة
        welcome_text = f"""
🌟 مرحباً بك {user.first_name}! 🌟

أنا بوت ذكي متطور يدعم عدة نماذج ذكاء اصطناعي قوية:

🧠 **DeepSeek V3** - نموذج متقدم للمحادثات الذكية
🤖 **GPT-4** - الذكاء الاصطناعي الأشهر عالمياً  
⚡ **GPT-4o** - النسخة المحسنة والأسرع
💎 **Gemini AI** - ذكاء جوجل الاصطناعي
🎨 **مولد الصور** - لإنشاء صور مذهلة

✨ **كيفية الاستخدام:**
1️⃣ اختر النموذج المفضل لديك
2️⃣ ابدأ المحادثة واطرح أسئلتك
3️⃣ استمتع بتجربة ذكاء اصطناعي متميزة!

اختر النموذج الذي تريد التحدث معه:
        """
        
        keyboard = create_model_keyboard()
        await update.message.reply_text(welcome_text, reply_markup=keyboard)
    
    else:
        # رسالة ترحيب للمجموعة
        group_welcome = f"""
🎉 مرحباً! تم إضافتي بنجاح للمجموعة! 🎉

🤖 أنا بوت ذكي يدعم عدة نماذج ذكاء اصطناعي متطورة

📝 **للتفاعل معي في المجموعة:**
• اكتب: `ذكاء` متبوعاً بسؤالك
• مثال: `ذكاء ما هو الذكاء الاصطناعي؟`

💬 **للمحادثة الخاصة:**
• راسلني على الخاص لتجربة كاملة
• يمكنك اختيار النموذج المفضل لديك

✨ استمتعوا بتجربة الذكاء الاصطناعي!
        """
        
        await update.message.reply_text(group_welcome)

def create_model_keyboard() -> InlineKeyboardMarkup:
    """إنشاء لوحة مفاتيح لاختيار النموذج"""
    keyboard = []
    for model_key, model_name in AVAILABLE_MODELS.items():
        keyboard.append([InlineKeyboardButton(model_name, callback_data=f"model_{model_key}")])
    
    keyboard.append([InlineKeyboardButton("ℹ️ المساعدة", callback_data="help")])
    return InlineKeyboardMarkup(keyboard)

async def model_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالج اختيار النموذج"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
    if data.startswith("model_"):
        model_key = data.replace("model_", "")
        user_models[user_id] = model_key
        model_name = AVAILABLE_MODELS[model_key]
        
        success_text = f"""
✅ تم اختيار النموذج بنجاح!

🎯 **النموذج المختار:** {model_name}

💬 الآن يمكنك بدء المحادثة! اكتب أي سؤال أو طلب وسأجيبك باستخدام النموذج المختار.

🔄 لتغيير النموذج، استخدم الأمر /models
        """
        
        await query.edit_message_text(success_text)
    
    elif data == "help":
        help_text = """
📚 **دليل الاستخدام:**

🔹 **الأوامر المتاحة:**
• `/start` - بدء البوت واختيار النموذج
• `/models` - عرض وتغيير النماذج المتاحة
• `/help` - عرض هذه المساعدة

🔹 **في المجموعات:**
• اكتب `ذكاء` متبوعاً بسؤالك
• مثال: `ذكاء اشرح لي الفيزياء الكمية`

🔹 **النماذج المتاحة:**
🧠 DeepSeek V3 - للمحادثات المتقدمة
🤖 GPT-4 - للإجابات الدقيقة
⚡ GPT-4o - للاستجابة السريعة
💎 Gemini AI - لذكاء جوجل
🎨 مولد الصور - لإنشاء الصور

💡 **نصائح:**
• كن واضحاً في أسئلتك للحصول على أفضل النتائج
• جرب نماذج مختلفة لمقارنة الإجابات
• استخدم مولد الصور لإنشاء صور إبداعية
        """
        
        back_keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton("🔙 العودة للنماذج", callback_data="back_to_models")
        ]])
        
        await query.edit_message_text(help_text, reply_markup=back_keyboard)
    
    elif data == "back_to_models":
        welcome_text = """
🌟 اختر النموذج الذي تريد التحدث معه:

🧠 **DeepSeek V3** - نموذج متقدم للمحادثات الذكية
🤖 **GPT-4** - الذكاء الاصطناعي الأشهر عالمياً  
⚡ **GPT-4o** - النسخة المحسنة والأسرع
💎 **Gemini AI** - ذكاء جوجل الاصطناعي
🎨 **مولد الصور** - لإنشاء صور مذهلة
        """
        
        keyboard = create_model_keyboard()
        await query.edit_message_text(welcome_text, reply_markup=keyboard)

async def models_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالج أمر /models"""
    keyboard = create_model_keyboard()
    text = """
🎯 **اختر النموذج المفضل لديك:**

🧠 **DeepSeek V3** - نموذج متطور للمحادثات المعقدة
🤖 **GPT-4** - الذكاء الاصطناعي الأكثر شهرة
⚡ **GPT-4o** - نسخة محسنة وأسرع من GPT-4
💎 **Gemini AI** - نموذج جوجل المتقدم
🎨 **مولد الصور** - لإنشاء صور فنية مذهلة
    """
    
    await update.message.reply_text(text, reply_markup=keyboard)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالج أمر /help"""
    help_text = """
📚 **دليل استخدام البوت الذكي:**

🔹 **الأوامر الأساسية:**
• `/start` - بدء البوت واختيار النموذج
• `/models` - عرض وتغيير النماذج المتاحة  
• `/help` - عرض هذه المساعدة

🔹 **في الدردشة الخاصة:**
• اختر النموذج المفضل لديك
• اكتب سؤالك أو طلبك مباشرة
• سأجيبك باستخدام النموذج المختار

🔹 **في المجموعات:**
• اكتب `ذكاء` متبوعاً بسؤالك
• مثال: `ذكاء ما هي فوائد الذكاء الاصطناعي؟`

🔹 **النماذج المتاحة:**
🧠 **DeepSeek V3** - للمحادثات المتقدمة والتحليل العميق
🤖 **GPT-4** - للإجابات الدقيقة والشاملة
⚡ **GPT-4o** - للاستجابة السريعة والفعالة
💎 **Gemini AI** - لذكاء جوجل المتطور
🎨 **مولد الصور** - لإنشاء صور فنية وإبداعية

💡 **نصائح للاستخدام الأمثل:**
• كن واضحاً ومحدداً في أسئلتك
• جرب نماذج مختلفة لمقارنة النتائج
• استخدم مولد الصور لطلبات الصور الإبداعية
• في المجموعات، تأكد من بدء رسالتك بكلمة "ذكاء"

🌟 استمتع بتجربة الذكاء الاصطناعي المتطورة!
    """
    
    await update.message.reply_text(help_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالج الرسائل النصية"""
    user_id = update.effective_user.id
    chat_type = update.effective_chat.type
    message_text = update.message.text
    
    # التحقق من نوع الدردشة
    if chat_type == 'private':
        # دردشة خاصة
        if user_id not in user_models:
            await update.message.reply_text(
                "⚠️ يرجى اختيار نموذج أولاً باستخدام الأمر /start أو /models"
            )
            return
        
        await process_ai_request(update, context, message_text, user_models[user_id])
    
    else:
        # دردشة مجموعة - التحقق من بداية الرسالة بكلمة "ذكاء"
        if message_text.startswith("ذكاء "):
            query = message_text[4:].strip()  # إزالة "ذكاء " من البداية
            if query:
                # استخدام نموذج افتراضي للمجموعات (DeepSeek)
                await process_ai_request(update, context, query, "deepseek")
            else:
                await update.message.reply_text(
                    "💬 اكتب سؤالك بعد كلمة 'ذكاء'\nمثال: ذكاء ما هو الذكاء الاصطناعي؟"
                )

async def process_ai_request(update: Update, context: ContextTypes.DEFAULT_TYPE, query: str, model: str) -> None:
    """معالجة طلب الذكاء الاصطناعي"""
    # إرسال رسالة "يكتب..." للإشارة إلى أن البوت يعمل
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        if model == "deepseek":
            result = TextAi.DeepInfra(query, "deepseekv3")
            response = result.get("result", "عذراً، حدث خطأ في الحصول على الإجابة.")
        
        elif model == "blackbox_gpt4":
            result = BlackBox.chat(query, "gpt-4")
            response = result.get("result", "عذراً، حدث خطأ في الحصول على الإجابة.")
        
        elif model == "blackbox_gpt4o":
            result = BlackBox.chat(query, "gpt-4o")
            response = result.get("result", "عذراً، حدث خطأ في الحصول على الإجابة.")
        
        elif model == "gemini":
            result = GeminiApi.chat(query)
            response = result.get("result", "عذراً، حدث خطأ في الحصول على الإجابة.")
        
        elif model == "image_ai":
            # للصور، نحتاج معالجة خاصة
            await update.message.reply_text("🎨 جاري إنشاء الصورة... قد يستغرق هذا بعض الوقت.")
            try:
                result = ImageAi.generate(query)
                if result.get("status") == "success":
                    image_url = result.get("result")
                    await update.message.reply_photo(photo=image_url, caption=f"🎨 تم إنشاء الصورة بناءً على: {query}")
                else:
                    await update.message.reply_text("عذراً، فشل في إنشاء الصورة. حاول مرة أخرى.")
            except Exception as e:
                await update.message.reply_text(f"عذراً، حدث خطأ في إنشاء الصورة: {str(e)}")
            return
        
        else:
            response = "عذراً، النموذج المختار غير متاح حالياً."
        
        # إرسال الإجابة
        if len(response) > 4096:
            # تقسيم الرسالة إذا كانت طويلة
            for i in range(0, len(response), 4096):
                await update.message.reply_text(response[i:i+4096])
        else:
            await update.message.reply_text(response)
    
    except Exception as e:
        logger.error(f"خطأ في معالجة طلب الذكاء الاصطناعي: {e}")
        await update.message.reply_text(
            "عذراً، حدث خطأ أثناء معالجة طلبك. يرجى المحاولة مرة أخرى لاحقاً."
        )

def main() -> None:
    """الدالة الرئيسية لتشغيل البوت"""
    # التحقق من وجود التوكن
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("⚠️ يرجى استبدال BOT_TOKEN بالتوكن الحقيقي للبوت!")
        print("احصل على التوكن من @BotFather على تلجرام")
        return
    
    # إنشاء التطبيق
    application = Application.builder().token(BOT_TOKEN).build()
    
    # إضافة معالجات الأوامر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("models", models_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # إضافة معالج الأزرار المضمنة
    application.add_handler(CallbackQueryHandler(model_callback))
    
    # إضافة معالج الرسائل النصية
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # تشغيل البوت
    print("🚀 تم تشغيل البوت بنجاح!")
    print("📱 يمكنك الآن التفاعل مع البوت على تلجرام")
    application.run_polling()

if __name__ == '__main__':
    main()



# ===== ميزات إضافية =====

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """عرض إحصائيات البوت"""
    user_count = len(user_models)
    stats_text = f"""
📊 **إحصائيات البوت:**

👥 عدد المستخدمين النشطين: {user_count}
🤖 النماذج المتاحة: {len(AVAILABLE_MODELS)}

🔥 **النماذج الأكثر استخداماً:**
"""
    
    # حساب النماذج الأكثر استخداماً
    model_usage = {}
    for model in user_models.values():
        model_usage[model] = model_usage.get(model, 0) + 1
    
    sorted_models = sorted(model_usage.items(), key=lambda x: x[1], reverse=True)
    for model, count in sorted_models[:3]:
        model_name = AVAILABLE_MODELS.get(model, model)
        stats_text += f"• {model_name}: {count} مستخدم\n"
    
    await update.message.reply_text(stats_text)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معلومات حول البوت"""
    about_text = """
🤖 **حول البوت الذكي**

📝 **الوصف:**
بوت تلجرام متطور يدعم عدة نماذج ذكاء اصطناعي قوية، مصمم لتوفير تجربة محادثة ذكية ومتنوعة.

⚡ **المميزات:**
• دعم 5 نماذج ذكاء اصطناعي متقدمة
• واجهة سهلة الاستخدام مع أزرار تفاعلية
• دعم الدردشة الخاصة والمجموعات
• إنشاء صور بالذكاء الاصطناعي
• رسائل ترحيب مخصصة

🛠️ **التقنيات المستخدمة:**
• Python 3.11
• مكتبة python-telegram-bot
• مكتبة RanaGPT
• نماذج AI متعددة (DeepSeek, GPT-4, Gemini)

👨‍💻 **المطور:** تم تطويره باستخدام أحدث التقنيات

🌟 **الإصدار:** 1.0.0
📅 **تاريخ الإنشاء:** 2025

💡 استمتع بتجربة الذكاء الاصطناعي المتطورة!
    """
    
    await update.message.reply_text(about_text)

async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """إعادة تعيين اختيار النموذج"""
    user_id = update.effective_user.id
    
    if user_id in user_models:
        del user_models[user_id]
        await update.message.reply_text(
            "✅ تم إعادة تعيين اختيارك بنجاح!\n"
            "استخدم /start أو /models لاختيار نموذج جديد."
        )
    else:
        await update.message.reply_text(
            "ℹ️ لم تقم باختيار أي نموذج بعد.\n"
            "استخدم /start أو /models لاختيار نموذج."
        )

# دالة للتحقق من حالة النموذج المختار
async def current_model_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """عرض النموذج المختار حالياً"""
    user_id = update.effective_user.id
    
    if user_id in user_models:
        current_model = user_models[user_id]
        model_name = AVAILABLE_MODELS.get(current_model, "غير معروف")
        
        status_text = f"""
🎯 **النموذج المختار حالياً:**

{model_name}

🔄 لتغيير النموذج، استخدم /models
ℹ️ للمساعدة، استخدم /help
        """
        
        await update.message.reply_text(status_text)
    else:
        await update.message.reply_text(
            "⚠️ لم تقم باختيار أي نموذج بعد.\n"
            "استخدم /start أو /models لاختيار نموذج."
        )

# معالج الأخطاء
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالج الأخطاء العام"""
    logger.error(f"حدث خطأ: {context.error}")
    
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "عذراً، حدث خطأ غير متوقع. يرجى المحاولة مرة أخرى لاحقاً."
        )

# تحديث الدالة الرئيسية لإضافة الأوامر الجديدة
def main() -> None:
    """الدالة الرئيسية لتشغيل البوت"""
    # التحقق من وجود التوكن
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("⚠️ يرجى استبدال BOT_TOKEN بالتوكن الحقيقي للبوت!")
        print("احصل على التوكن من @BotFather على تلجرام")
        return
    
    # إنشاء التطبيق
    application = Application.builder().token(BOT_TOKEN).build()
    
    # إضافة معالجات الأوامر الأساسية
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("models", models_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # إضافة معالجات الأوامر الإضافية
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("reset", reset_command))
    application.add_handler(CommandHandler("current", current_model_command))
    
    # إضافة معالج الأزرار المضمنة
    application.add_handler(CallbackQueryHandler(model_callback))
    
    # إضافة معالج الرسائل النصية
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # إضافة معالج الأخطاء
    application.add_error_handler(error_handler)
    
    # تشغيل البوت
    print("🚀 تم تشغيل البوت بنجاح!")
    print("📱 يمكنك الآن التفاعل مع البوت على تلجرام")
    print("🔧 الأوامر المتاحة:")
    print("   /start - بدء البوت")
    print("   /models - اختيار النموذج")
    print("   /help - المساعدة")
    print("   /stats - الإحصائيات")
    print("   /about - حول البوت")
    print("   /reset - إعادة تعيين")
    print("   /current - النموذج الحالي")
    
    application.run_polling()

