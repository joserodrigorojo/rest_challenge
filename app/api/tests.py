from django.test import TestCase

from api.models import *

class OrderModelTest(TestCase):
    def test_create_order(self):
        order = Order.objects.create(client=Client.objects.create(name="Test Client"))
        self.assertEqual(order.client.name, "Test Client")

    def test_get_orders(self):
        response = self.client.get('/orders/')
        self.assertEqual(response.status_code, 200)
