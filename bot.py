import telebot
from telebot import types
import os, random

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHANNEL_ID = -1004450817952
INVITE_LINK = os.getenv("INVITE_LINK")

BKASH_NUMBERS = ["017XX-XXXXXX"]
NAGAD_NUMBERS = ["018XX-XXXXXX"]

bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}

@bot.message_handler(commands=['start','pay'])
def pay(m):
    text = f"💰 Payment\nবিকাশ: {random.choice(BKASH_NUMBERS)}\nনগদ: {random.choice(NAGAD_NUMBERS)}\n\nটাকা পাঠিয়ে ক্লিক করো 👇"
    mk = types.InlineKeyboardMarkup()
    mk.add(types.InlineKeyboardButton("✅ টাকা পাঠিয়েছি", callback_data="paid"))
    bot.send_message(m.chat.id, text, reply_markup=mk)

@bot.callback_query_handler(func=lambda c: c.data=="paid")
def ask_num(call):
    msg = bot.send_message(call.message.chat.id, "কোন নাম্বার থেকে পাঠিয়েছো?")
    bot.register_next_step_handler(msg, ask_trx)

def ask_trx(message):
    user_data[message.chat.id] = {'sender': message.text}
    msg = bot.send_message(message.chat.id, "TrxID দাও:")
    bot.register_next_step_handler(msg, send_admin)

def send_admin(message):
    sender = user_data[message.chat.id]['sender']
    trxid = message.text
    txt = f"🔔 New Payment\nUser: @{message.from_user.username} ({message.from_user.id})\nSender: {sender}\nTrxID: {trxid}"
    mk = types.InlineKeyboardMarkup()
    mk.row(types.InlineKeyboardButton("✅ Approve", callback_data=f"approve_{message.chat.id}"), types.InlineKeyboardButton("❌ Reject", callback_data=f"reject_{message.chat.id}"))
    bot.send_message(ADMIN_CHANNEL_ID, txt, reply_markup=mk)
    bot.send_message(message.chat.id, "✅ Request পাঠানো হয়েছে।")

@bot.callback_query_handler(func=lambda c: c.data.startswith("approve_"))
def approve(call):
    uid = int(call.data.split("_")[1])
    bot.send_message(uid, f"✅ Verified! Link: {INVITE_LINK}")

@bot.callback_query_handler(func=lambda c: c.data.startswith("reject_"))
def reject(call):
    uid = int(call.data.split("_")[1])
    bot.send_message(uid, "❌ ভুল। আবার /pay দাও।")

bot.infinity_polling()
