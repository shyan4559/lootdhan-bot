import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "7580790063:AAEcmPhLSIWtY-6nj7rlqER7LlRuzaIdt44"
ADMIN_ID = 6393057518
MIN_WITHDRAW = 10
REF_BONUS = 5
DB_FILE = "users.json"

# Load or initialize users database
def load_users():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f)

users = load_users()

def get_user(user_id):
    if str(user_id) not in users:
        users[str(user_id)] = {"balance": 0, "ref_by": None}
    return users[str(user_id)]

# MAIN MENU KEYBOARD
def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("💰 Tasks", callback_data="tasks"),
         InlineKeyboardButton("👥 Refer", callback_data="refer")],
        [InlineKeyboardButton("🎁 Daily Bonus", callback_data="bonus"),
         InlineKeyboardButton("📺 Watch & Earn", callback_data="watch")],
        [InlineKeyboardButton("📢 Join & Earn", callback_data="join"),
         InlineKeyboardButton("📊 My Balance", callback_data="balance")],
        [InlineKeyboardButton("💸 Withdraw", callback_data="withdraw")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = user.id
    args = context.args

    u = get_user(uid)
    if args:
        ref = args[0]
        if u["ref_by"] is None and ref != str(uid):
            u["ref_by"] = ref
            ref_user = get_user(ref)
            ref_user["balance"] += REF_BONUS
            await context.bot.send_message(chat_id=int(ref), text=f"🎉 You earned ₹{REF_BONUS} for referring {user.first_name}!")

    save_users(users)

    await update.message.reply_text("👋 Welcome to LootDhan Bot!\n\nChoose an option below 👇", reply_markup=get_main_menu())

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    u = get_user(uid)

    back_button = [[InlineKeyboardButton("🔙 Back", callback_data="main_menu")]]

    if query.data == "tasks":
        await query.edit_message_text("💼 Current Tasks:\n- Follow channel: @Samtheearnerteam\n- Earn ₹2 per task completed!",
                                      reply_markup=InlineKeyboardMarkup(back_button))
    elif query.data == "refer":
        ref_link = f"https://t.me/LootDhanBot?start={uid}"
        await query.edit_message_text(f"👥 Refer friends and earn ₹{REF_BONUS}!\nYour link: {ref_link}",
                                      reply_markup=InlineKeyboardMarkup(back_button))
    elif query.data == "bonus":
        u["balance"] += 1
        save_users(users)
        await query.edit_message_text("🎁 You received ₹1 daily bonus!",
                                      reply_markup=InlineKeyboardMarkup(back_button))
    elif query.data == "watch":
        u["balance"] += 2
        save_users(users)
        await query.edit_message_text("📺 You watched an ad and earned ₹2!",
                                      reply_markup=InlineKeyboardMarkup(back_button))
    elif query.data == "join":
        u["balance"] += 1
        save_users(users)
        await query.edit_message_text("📢 You earned ₹1 for joining our sponsor channel!",
                                      reply_markup=InlineKeyboardMarkup(back_button))
    elif query.data == "balance":
        await query.edit_message_text(f"💰 Your current balance: ₹{u['balance']}",
                                      reply_markup=InlineKeyboardMarkup(back_button))
    elif query.data == "withdraw":
        if u["balance"] >= MIN_WITHDRAW:
await query.edit_message_text("💸 Enter your UPI ID to receive ₹10 (Simulation only)",
                                          reply_markup=InlineKeyboardMarkup(back_button))
            u["balance"] -= MIN_WITHDRAW
            save_users(users)
        else:
            await query.edit_message_text(f"❌ Minimum withdrawal is ₹{MIN_WITHDRAW}. Your balance is ₹{u['balance']}",
                                          reply_markup=InlineKeyboardMarkup(back_button))
    elif query.data == "main_menu":
        await query.edit_message_text("👋 Welcome back to LootDhan Bot!\n\nChoose an option below 👇",
                                      reply_markup=get_main_menu())

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    text = "👮 Admin Panel\n\n"
    total = len(users)
    total_bal = sum(u["balance"] for u in users.values())
    text += f"👤 Total users: {total}\n💰 Total balance across users: ₹{total_bal}"
    await update.message.reply_text(text)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.add_handler(CommandHandler("admin", admin))
    app.run_polling()

if __name__ == "__main__":
    main()
