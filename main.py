import telebot
from datetime import datetime

BOT_TOKEN = "8708661936:AAEKDfMJvflGkEDXeFr2tvU9tQIDa8RENNw"

# PUT YOUR GROUP ID HERE
GROUP_ID = -1003839159361

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot is active ✅")

@bot.message_handler(commands=['report'])
def report(message):
    try:
        data = message.text.split()

        username = data[1]
        links = data[2]
        salary = data[3]
        status = data[4]

        if status.lower() == "credited":
            status_text = "Credited ✅"
        else:
            status_text = "Pending ⏳"

        today = datetime.now().strftime("%d %B %Y")

        text = f"""
📢 WORK UPDATE

👤 Employee: {username}
🔗 Links Collected: {links}
💰 Salary Earned: ₹{salary}
💳 Salary Status: {status_text}
📅 Date: {today}
"""

        bot.send_message(GROUP_ID, text)

        bot.reply_to(message, "Report sent to group ✅")

    except:
        bot.reply_to(
            message,
            "Usage:\n/report @username links salary credited/pending"
        )

print("Bot Running...")
bot.infinity_polling()
