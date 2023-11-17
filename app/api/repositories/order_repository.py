from datetime import datetime
from turtle import up
from ..models import Client, Item, Order, OrderItem

class OrderRepository:
    def get_all_orders(self):
        return Order.objects.prefetch_related(
            'items', 
            'client'
        ).all()

    def get_all_orders_by_date(self, date):
        return Order.objects.filter(created_at__date=date).prefetch_related(
            'items', 
            'client'
        ).all()

    def get_all_orders_by_cancelled_date(self, date):
        return Order.objects.filter(cancelled_at__date=date).prefetch_related(
            'items', 
            'client'
        ).all()
    
    def get_order_by_id(self, order_id):
        return Order.objects.get(id = order_id)
    
    def create_order(self, order_data, order_items_data):
        order = Order.objects.create(client=order_data)
        client = Client.objects.get(id=order.client.id)

        for item_data in order_items_data:
            if item_data['quantity'] > 100:
                raise ValueError("Cannot order more than 100 items of the same type.")
            item = Item.objects.get(id=item_data['item_id'])
            quantity = item_data['quantity']
            price_at_order = item.price
            subtotal = price_at_order * quantity
            vat = subtotal * item.vat_rate if not client.reduced_vat_rate else subtotal * (item.vat_rate / 2)  

            OrderItem.objects.create(
                order=order,
                item=item,
                quantity=quantity,
                subtotal= subtotal,
                vat = vat,
            )

        return order

    def create_order_by_client_name(self, order_data, order_items_data):
        try:
            client = Client.objects.get(name=order_data)
        except Client.DoesNotExist:
            raise ValueError("Client does not exist.")
        order = Order.objects.create(client=client)

        for item_data in order_items_data:
            if item_data['quantity'] > 100:
                raise ValueError("Cannot order more than 100 items of the same type.")
            item = Item.objects.get(id=item_data['item_id'])
            quantity = item_data['quantity']
            price_at_order = item.price
            subtotal = price_at_order * quantity
            vat = subtotal * item.vat_rate if not client.reduced_vat_rate else subtotal * (item.vat_rate / 2)  

            OrderItem.objects.create(
                order=order,
                item=item,
                quantity=quantity,
                subtotal= subtotal,
                vat = vat,
            )

        return order
    
    def cancel_order(self, order_id):
        return Order.objects.filter(id = order_id).update(cancelled = True, cancelled_at = datetime.now(), status = 'CANCELLED')