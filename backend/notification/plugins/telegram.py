# notifications/plugins/telegram.py
import os
import telegram
import asyncio

async def _send(message):
    bot = telegram.Bot(token=os.environ["BOT_TOKEN"])
    await bot.send_message(
        chat_id=os.environ["CHAT_ID"],
        text=message
    )

def send_orders_notification(orders):
    message = "🛒 New Orders:\n"
    for order in orders:
        message += f"- {order.order_id} | {order.variant.title}\n"

    asyncio.run(_send(message))
