import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("8705352652:AAHwgTfsumylrWCeDhOgXsXhcyOeppT0jqs")

users = set()

async def capture_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user:
        users.add((user.id, user.full_name))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user:
        users.add((user.id, user.full_name))

    await update.message.reply_text(
        "Hi! I’m EchoTagBot, the automatic assistant for Telegram groups.\n\n"
        "I can mention (tag) all members of the Telegram group I’m in simultaneously.\n\n"
        "Add me to your group and use the command:\n"
        "/tagall"
    )

async def tagall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not users:
        await update.message.reply_text("No active users found yet.")
        return

    text = "📢 TAGGING ALL ACTIVE MEMBERS\n\n"

    for uid, name in users:
        text += f"[{name}](tg://user?id={uid})\n"

    await update.message.reply_text(text, parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tagall", tagall))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, capture_users))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
