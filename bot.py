from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import os

TOKEN = os.environ.get("8369100760:AAEEkuwbZz0eOghLboKeP1qN2l9tJd0OdwE")  # ya direct token

API_URL = "http://texttovideov2.alphaapi.workers.dev/api/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a text and I’ll make a video from it!")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text("Creating your video, please wait...")
    try:
        # Example request — adjust parameters per API spec
        resp = requests.post(API_URL, json={"prompt": user_text})
        resp.raise_for_status()
        data = resp.json()
        # Suppose API returns a 'video_url'
        video_url = data.get("video_url")
        if not video_url:
            await update.message.reply_text("Sorry, couldn’t get a video from API.")
            return
        # Send video to user
        await context.bot.send_video(chat_id=update.effective_chat.id, video=video_url)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()

if __name__ == "__main__":
    main()
