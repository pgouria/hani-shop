from inventory.models import Stock

class StockChanged:
    def __init__(self, stock : Stock):
        self.stock = stock