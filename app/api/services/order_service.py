from api.models import Item
from ..repositories import order_repository

class OrderService:
    def __init__(self):
        self.repository = order_repository.OrderRepository()

    def list_orders(self):
        return self.repository.get_all_orders()

    def list_orders_by_date(self, date):
        return self.repository.get_all_orders_by_date(date)

    def list_orders_by_cancelled_date(self, date):
        return self.repository.get_all_orders_by_cancelled_date(date)
    
    def get_order(self, order_id):
        return self.repository.get_order_by_id(order_id)
    
    def create_order(self, order_data, order_items_data):
        return self.repository.create_order(order_data, order_items_data)

    def create_order_by_client_name(self, order_data, order_items_data):
        return self.repository.create_order_by_client_name(order_data, order_items_data)
    
    def cancel_order(self, order_id):
        return self.repository.cancel_order(order_id)