from celery import shared_task

@shared_task
def fetch_orders():
    from marketplace.digikala.main import fetch_orders
    fetch_orders()