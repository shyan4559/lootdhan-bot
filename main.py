> Earner:
# LootDhan Telegram Bot - Inline Keyboard Version

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import json, os

# Load or initialize users data
USERS_FILE = 'users.json'
if os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
else:
    users = {}

def save_users():
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)

# ✅ Your admin Telegram ID
ADMIN_ID = 6393057518
BOT_TOKEN = "7580790063:AAEcmPhLSIWtY-6nj7rlqER7LlRuzaIdt44"

# Inline button layout
keyboard = [
    [InlineKeyboardButton("💰 Tasks", callback_data='tasks'), InlineKeyboardButton("👥 Refer", callback_data='refer')],
    [InlineKeyboardButton("🎁 Daily Bonus", callback_data='bonus'), InlineKeyboardButton("📺 Watch & Earn", callback_data='watch')],
    [InlineKeyboardButton("📢 Join & Earn", callback_data='join'), InlineKeyboardButton("📊 My Balance", callback_data='balance')],
    [InlineKeyboardButton("💸 Withdraw", callback_data='withdraw')],
    [InlineKeyboardButton("🔗 Complete Task", callback_data='complete_task')]
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id not in users:
        users[user_id] = {
            "balance": 0,
            "ref": update.message.text.split(" ")[1] if len(update.message.text.split(" ")) > 1 else None,
            "has_spun": False
        }
        ref_id = users[user_id]['ref']
        if ref_id and ref_id in users:
            users[ref_id]['balance'] += 5
    save_users()
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Welcome to LootDhan Bot!\nChoose an option below 👇", reply_markup=reply_markup)

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = str(query.from_user.id)
    await query.answer()

    if query.data == 'tasks':
        await query.edit_message_text("📋 Task:\n1. Join @SamTheEarnerTeam\n2. Screenshot & send to admin\n💰 Reward: ₹3")
    elif query.data == 'refer':
        await query.edit_message_text(f"👥 Refer & Earn ₹5!\nShare this link:\nt.me/LootDhanBot?start={user_id}")
    elif query.data == 'bonus':
        if not users[user_id].get("has_spun"):
            users[user_id]['balance'] += 2
            users[user_id]['has_spun'] = True
            save_users()
            await query.edit_message_text("🎉 You got ₹2 Daily Bonus!")
        else:
            await query.edit_message_text("⚠️ You already claimed your daily bonus today.")
    elif query.data == 'watch':
        await query.edit_message_text("📺 Watch & Earn is coming soon!")
    elif query.data == 'join':
        await query.edit_message_text("📢 Join & Earn:\nJoin our channel @SamTheEarnerTeam and send screenshot to admin. Reward: ₹2")
    elif query.data == 'balance':
        bal = users.get(user_id, {}).get("balance", 0)
        await query.edit_message_text(f"📊 Your balance is ₹{bal}")
    elif query.data == 'withdraw':
        if users[user_id]['balance'] >= 10:
            users[user_id]['balance'] -= 10
            save_users()
            await query.edit_message_text("✅ Withdrawal request sent to admin. You’ll receive ₹10 soon via UPI.")
        else:
            await query.edit_message_text("❌ You need at least ₹10 to withdraw.")
    elif query.data == 'complete_task':
        await query.edit_message_text("✅ Complete this offer to earn 1000 coins!")

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Unauthorized")
        return
    total_users = len(users)
    await update.message.reply_text(f"👑 Admin Panel 👑\nTotal Users: {total_users}")

# Setup
app = ApplicationBuilder().token(BOT_TOKEN).build()

> Earner:
# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(CallbackQueryHandler(handle_buttons))

if __name__ == '__main__':
    print("Bot is starting...")
    app.run_polling()
