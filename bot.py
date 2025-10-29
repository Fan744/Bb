import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import json

# Logging setup (debug के लिए)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# API endpoint
GEMINI_API_URL = "https://gemini-1.5-flash.bjcoderx.workers.dev/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bot start command का handler"""
    await update.message.reply_text('नमस्ते! मुझे कोई message भेजें, मैं Gemini AI से response दूंगा। (अगर API काम करे तो 😊)')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """User message को API भेजने का handler"""
    user_message = update.message.text
    await update.message.reply_text("Thinking... (Gemini AI से response आ रहा है)")

    # API call
    try:
        response = requests.get(f"{GEMINI_API_URL}?text={user_message}")
        data = response.json()
        
        if data.get("success"):
            ai_reply = data.get("response", "कोई response नहीं मिला।")
            await update.message.reply_text(ai_reply)
        else:
            await update.message.reply_text(f"Error: {data.get('error', 'Unknown error')}। API अभी काम नहीं कर रहा। Try again later!")
    except Exception as e:
        logger.error(f"API call failed: {e}")
        await update.message.reply_text("Sorry, कुछ technical issue है। बाद में try करें!")

def main() -> None:
    """Bot run करने का main function"""
    # Bot token replace करें
    application = Application.builder().token("8369100760:AAEEkuwbZz0eOghLboKeP1qN2l9tJd0OdwE").build()

    # Handlers add करें
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Bot start करें
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
