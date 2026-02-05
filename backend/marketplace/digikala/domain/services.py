import datetime
from ..models import  Product , Variant , Order

def save_orders(orders: list):
    """
    Save orders to the database and return the new orders.

    Args:
        orders (list): List of orders to save.

    Returns:
        list: List of new orders.
    """

    new_orders = []
    for item in orders:
            variant_data = item.get('variant')
            product_data = variant_data.get('product')
            
            # Create or get Product
            product, created =  Product.objects.get_or_create(
                product_id=product_data['id'],
                defaults={
                    'category_id': product_data['category_id'],
                    'title': product_data['title'],
                    
                }
            )

            # Create or get Variant
            variant, created =  Variant.objects.get_or_create(
                variant_id=variant_data['id'],
                defaults={
                    'seller_id': variant_data['seller_id'],
                    'site': variant_data['site'],
                    'is_active': variant_data['is_active'],
                    'is_archived': variant_data['is_archived'],
                    'title': variant_data['title'],
                    'product': product,
                    'shipping_type': variant_data['shipping_type'],
                    'stock_in_digikala': variant_data['stock']['in_ warehouse'],
                    'stock_in_seller_warehouse': variant_data['stock']['in_seller_warehouse'],
                }
            )

            # Check if the order already exists
            order_exists =  Order.objects.filter(order_item_id=item['order_item_id']).exists()

            # If the order does not exist, it's a new order
            if not order_exists:
                new_order =  Order.objects.create(
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
           
    
                    
        return new_orders
    else:
        return []


def save_variants(variants: list):
    """
    Save variants to the database and update the existing ones.

    Args:
        variants (list): List of variants to save.
    """

    for item in variants:

        product_data = item.get('product')
        
        # Create or get Product
        product, created =  Product.objects.get_or_create(
            product_id=product_data['id'],
            defaults={

                'category_id': product_data['category_id'],
                'title': product_data['title'],

            }
        )

        # Create or get Variant
        variant, created =  Variant.objects.get_or_create(
            variant_id=item['id'],
            defaults={
                'seller_id': item['seller_id'],
                'site': item['site'],
                'is_active': item['is_active'],
                'is_archived': item['is_archived'],
                'title': item['title'],
                'product': product,
                'shipping_type': item['shipping_type'],
                'stock_in_digikala': item['stock']['dk_stock'],
                'stock_in_seller_warehouse': item['stock']['seller_stock'],
                'fulfilment_and_delivery_cost': item['fulfilment_and_delivery_cost'],
                'buy_box_price': item['extra'].get('buy_box', {}).get('buy_box_price', 0),
                'selling_price': item['price']['selling_price'],
                'is_buy_box_winner': item['extra']['buy_box']['is_buy_box_winner'],
                'selling_stock': item['stock']['selling_stock'],

                


            }
        )
          


        # If the variant already exists, update the fields
        if not created:
         variant.variant_id=item['id']
         variant.seller_id = item['seller_id']
         variant.site = item['site']
         variant.is_active = item['is_active']
         variant.is_archived = item['is_archived']
         variant.title = item['title']
         variant.product = product
         variant.shipping_type = item['shipping_type']
         variant.stock_in_digikala = item['stock']['dk_stock']
         variant.stock_in_seller_warehouse = item['stock']['seller_stock']
         variant.fulfilment_and_delivery_cost = item['fulfilment_and_delivery_cost']
         variant.buy_box_price = item['extra'].get('buy_box', {}).get('buy_box_price', 0)
         variant.selling_price = item['price']['selling_price']
         variant.is_buy_box_winner = item['extra']['buy_box']['is_buy_box_winner']
         variant.selling_stock = item['stock']['selling_stock']
         # Save the updated variant
         variant.save() 