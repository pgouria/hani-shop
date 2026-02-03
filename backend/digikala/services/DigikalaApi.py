import requests
from .models import Order, Variant, Product
from datetime import datetime
from celery import shared_task
import telegram
from telegram import Bot
import asyncio
import os

API_URL = "https://seller.digikala.com/api/v1/orders/"

@shared_task
def fetch_orders():
  
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    CHAT_ID = os.environ.get("CHAT_ID")

   
    token = os.environ.get("DIGIKALA_TOKEN")

    headers = {
        "authorization": f"{token}",
        "Content-Type": "application/json"
    }

    response = requests.get(API_URL, headers=headers)
    data = response.json()

    items = data.get('data').get('items')
    new_orders = []  # To keep track of newly added orders

    for item in items:
        variant_data = item.get('variant')
        product_data = variant_data.get('product')
        
        # Create or get Product
        product, created = Product.objects.get_or_create(
            product_id=product_data['id'],
            defaults={
                'category_id': product_data['category_id'],
                'title': product_data['title'],
                
            }
        )

        # Create or get Variant
        variant, created = Variant.objects.get_or_create(
            variant_id=variant_data['id'],
            defaults={
                'seller_id': variant_data['seller_id'],
                'site': variant_data['site'],
                'is_active': variant_data['is_active'],
                'is_archived': variant_data['is_archived'],
                'title': variant_data['title'],
                'product': product,
                'shipping_type': variant_data['shipping_type'],
                'stock_in_digikala': variant_data['stock']['in_digikala_warehouse'],
                'stock_in_seller_warehouse': variant_data['stock']['in_seller_warehouse'],
            }
        )

        # Check if the order already exists
        order_exists = Order.objects.filter(order_item_id=item['order_item_id']).exists()

        # If the order does not exist, it's a new order
        if not order_exists:
            new_order = Order.objects.create(
                order_item_id=item['order_item_id'],
                order_id=item['order_id'],
                variant=variant,
                product=product,
                quantity=item['quantity'],
                order_status=item['order_status'],
                shipment_status=item['shipment_status'],
                selling_price=item['selling_price'],
                created_at=datetime.strptime(item['created_at'], '%Y-%m-%d %H:%M:%S'),
                commitment_date=datetime.strptime(item['commitment_date'], '%Y-%m-%d %H:%M:%S'),
            )
            new_orders.append(new_order)

    if new_orders:
        # Prepare the message
        message = "New Orders:\n"
        for order in new_orders:
            message += f"Order ID: {order.order_id},Product Title : {order.variant.title}, Quantity: {order.quantity}, Status: {order.order_status}\n"
        asyncio.run(send_to_telegram(BOT_TOKEN, CHAT_ID, message))  # Run async function
 
                
    return new_orders


async def send_to_telegram(bot_token, chat_id, message):
    bot = telegram.Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)