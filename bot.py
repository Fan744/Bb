from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os, requests

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # apna token yahan set karo

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send /video <your prompt> to create a video.")

async def ask_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # user ne command /video diya
    prompt_text = " ".join(context.args)
    if not prompt_text:
        await update.message.reply_text("Please provide a prompt, e.g. /video a girl dancing")
        return
    await update.message.reply_text(f"Creating video for prompt: {prompt_text} …")
    # API call
    url = "https://texttovideov2.alphaapi.workers.dev/api/"
    try:
        res = requests.get(url, params={"prompt": prompt_text})
        res.raise_for_status()
        data = res.json()  # assuming JSON
        video_url = data.get("video_url")  # ye key API ke response pe depend karegi
        if video_url:
            await update.message.reply_text(f"Here is your video: {video_url}")
        else:
            await update.message.reply_text("Sorry, video link not available.")
    except Exception as e:
        await update.message.reply_text("Error occurred while generating video.")
        print("Error:", e)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("video", ask_video))
    app.run_polling()

if __name__ == "__main__":
    main()
