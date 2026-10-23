import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
INVITE_LINK = os.getenv("INVITE_LINK")

# তোমার নাম্বার
BKASH_NUMBER = "01706433005"
NAGAD_NUMBER = "01706433005"

ADMIN_ID = 8149546564  # @userinfobot কে /start লিখে তোমার ID এখানে বসাও

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        f"💰 **পেমেন্ট করুন**\n\n"
        f"📱 বিকাশ (Personal): `{BKASH_NUMBER}`\n"
        f"📱 নগদ (Personal): `{NAGAD_NUMBER}`\n\n"
        f"টাকা: 510 টাকা (বা তোমার নির্ধারিত)\n\n"
        f"টাকা পাঠিয়ে নিচের বাটনে ক্লিক করো 👇"
    )
    keyboard = [[InlineKeyboardButton("✅ টাকা পাঠিয়েছি", callback_data="paid")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def paid_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        "✅ ঠিক আছে!\n\n"
        "এখন **টাকা পাঠানোর স্ক্রিনশট + Transaction ID** একসাথে পাঠাও 📸\n\n"
        "যেমন: ছবির Caption এ লিখবে `TrxID: 8F9K2L1M`\n\n"
        "⚠️ স্ক্রিনশট ছাড়া Approve হবে না।"
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    caption = update.message.caption or "কোনো TrxID লেখা নেই"

    # Admin এর কাছে পাঠানো
    forward_text = (
        f"🔔 নতুন পেমেন্ট জমা!\n\n"
        f"👤 User: @{user.username}\n"
        f"🆔 ID: {user.id}\n"
        f"💬 TrxID/Caption: {caption}"
    )
    await context.bot.send_message(chat_id=ADMIN_ID, text=forward_text)
    await context.bot.forward_message(chat_id=ADMIN_ID, from_chat_id=update.effective_chat.id, message_id=update.message.message_id)
    
    keyboard = [[Inline
