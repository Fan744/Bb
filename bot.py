import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
import os

# Logging सेटअप (debug के लिए)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
TELEGRAM_TOKEN = '8369100760:AAEEkuwbZz0eOghLboKeP1qN2l9tJd0OdwE'  # यहां अपना token डालें
API_URL = 'https://gemini-1-5-flash.bjcoderx.workers.dev/?text=hello'  # API endpoint
API_KEY = 'YOUR_API_KEY'  # अगर API key required है, वरना '' रखें

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ /start command handler """
    await update.message.reply_text('नमस्ते! मुझे कोई text भेजें, मैं उसे video में convert करके भेज दूंगा।')

async def generate_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Text message handler: API call और video send """
    user_text = update.message.text
    await update.message.reply_text('Video generate हो रही है... थोड़ा इंतजार करें! ⏳')

    try:
        # API request payload (assume JSON format; adjust as per actual API)
        payload = {
            'text': user_text,
            'api_key': API_KEY  # अगर required हो
        }
        
        # POST request
        response = requests.post(API_URL, json=payload, timeout=60)
        response.raise_for_status()  # Error अगर status code bad हो
        
        # Assume response में video URL या base64 data है; adjust accordingly
        data = response.json()
        video_url = data.get('video_url')  # या data['video'] अगर direct URL हो
        
        if video_url:
            # Video download (अगर URL है) या direct send
            await update.message.reply_video(video=video_url, caption='यह आपकी generated video है! 🎥')
        else:
            await update.message.reply_text('Video generate नहीं हो सकी। Error: ' + str(data))
            
    except requests.exceptions.RequestException as e:
        logger.error(e)
        await update.message.reply_text('API call में error आ गई। कृपया बाद में try करें।')
    except Exception as e:
        logger.error(e)
        await update.message.reply_text('कुछ गड़बड़ हो गई। Admin को बताएं।')

def main() -> None:
    """ Bot run करने का main function """
    # Application create
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Handlers add करें
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_video))

    # Bot start
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
