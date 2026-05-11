from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json
import os
from datetime import datetime

BOT_TOKEN = "8708661936:AAEKDfMJvflGkEDXeFr2tvU9tQIDa8RENNw"
GROUP_ID = -1003839159361
ADMIN_ID = 7222663168

DATA_FILE = "data.json"

# Create data file if not exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text("✅ Salary Bot Active")

# UPDATE COMMAND
async def update_salary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    try:
        username = context.args[0]
        links = context.args[1]
        amount = context.args[2]
        status = context.args[3]
        date = " ".join(context.args[4:])

        data = load_data()

        entry = {
            "username": username,
            "links": links,
            "amount": amount,
            "status": status,
            "date": date
        }

        data.append(entry)
        save_data(data)

        message = f"""
📋 Salary Update

👤 Employee: {username}
🔗 Links Submitted: {links}
💰 Salary: ₹{amount}
📌 Status: {status.capitalize()}
📅 Date: {date}
"""

        await context.bot.send_message(chat_id=GROUP_ID, text=message)
        await update.message.reply_text("✅ Update Sent")

    except:
        await update.message.reply_text(
            "❌ Usage:\n/update @username links amount status date"
        )

# PAID COMMAND
async def paid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    try:
        username = context.args[0]
        paid_date = " ".join(context.args[1:])

        data = load_data()

        found = False

        for entry in data:
            if entry["username"] == username and entry["status"].lower() == "pending":
                entry["status"] = "paid"
                entry["date"] = paid_date
                found = True

        save_data(data)

        if found:
            message = f"""
✅ Payment Update

👤 Employee: {username}
📌 Status: Paid
📅 Paid Date: {paid_date}
"""

            await context.bot.send_message(chat_id=GROUP_ID, text=message)
            await update.message.reply_text("✅ Marked As Paid")

        else:
            await update.message.reply_text("❌ No Pending Record Found")

    except:
        await update.message.reply_text(
            "❌ Usage:\n/paid @username date"
        )

# PENDING COMMAND
async def pending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    data = load_data()

    pending_users = [
        f"👤 {x['username']} - ₹{x['amount']}"
        for x in data if x["status"].lower() == "pending"
    ]

    if pending_users:
        text = "📌 Pending Salaries\n\n" + "\n".join(pending_users)
    else:
        text = "✅ No Pending Salaries"

    await update.message.reply_text(text)

# MAIN
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("update", update_salary))
app.add_handler(CommandHandler("paid", paid))
app.add_handler(CommandHandler("pending", pending))

print("Bot Running...")
app.run_polling()
