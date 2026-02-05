from celery import shared_task

@shared_task
def fetch_orders():
    from marketplace.digikala.application.sync_orders import sync_orders
    sync_orders()