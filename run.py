#!/usr/bin/env python3.7 ++
import requests
import logging
from telegram import ForceReply, Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

############# REPLACE THIS ###############
BOT_TOKEN = "xysysysdaiyodyx"
SIMI_API_KEY = "xysydiuasoiud9sys"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

def get_simsimi_response(text):
    try:
        URL = "https://wsapi.simsimi.com/190410/talk"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": SIMI_API_KEY
            
        }
        payload = {
            "utext": text,
            "lang": "id"  
        }
        r = requests.post(url=URL, headers=headers, json=payload)
        
        if r.status_code == 200:
            data = r.json()
            if 'atext' in data: 
                return data['atext']
            elif 'msg' in data and data['result'] == 509:
                return data['msg']  
            else:
                return "Error: Invalid response format"
        else:
            return f"Error: {r.status_code} {r.reason}"
        
    except Exception as e:
        print("Error:", e)
        return "Error occurred"
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text
    response = get_simsimi_response(user_input)
    await update.message.reply_text(response)

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT, echo))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
