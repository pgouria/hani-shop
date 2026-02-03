import telegram
import asyncio
import os
from core.domain.events import OrdersCreated



def send_to_telegram(event : OrdersCreated):
    
    
    bot_token = os.environ.get("BOT_TOKEN")
    chat_id = os.environ.get("CHAT_ID")
    message = f"Orders Created: {event.orders}"
    asyncio.run(_send(bot_token, chat_id, message))

    


    async def _send(token, chat_id, message):
        if token and chat_id:
            bot = telegram.Bot(token=token)
            await bot.send_message(chat_id=chat_id, text=message)
        else :
            raise Exception("Token or Chat ID is not provided")
      
        

