from rest_framework import serializers
from api.models import *

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class ItemSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs['price'] < 0:
            raise serializers.ValidationError("Price cannot be negative")
        if attrs['name'] == "":
            raise serializers.ValidationError("Name cannot be empty")
        if attrs['description'] == "":
            raise serializers.ValidationError("Description cannot be empty")
        return attrs

    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'category']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class ListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name']

class OrderItemSerializer(serializers.ModelSerializer):
    item_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = OrderItem
        fields = fields = ['item_id', 'quantity']

class ListOrderItemSerializer(serializers.ModelSerializer):
    item = ListItemSerializer()
    class Meta:
        model = OrderItem
        fields = ['item', 'quantity', 'unit_price', 'subtotal', 'vat', 'total']

class OrderSerializer(serializers.ModelSerializer):
    total = serializers.FloatField()
    subtotal = serializers.FloatField()
    vat = serializers.FloatField()
    items = ListOrderItemSerializer(source='orderitem_set', many=True, read_only=True)
    client_name = serializers.CharField(source='client.name', read_only=True)
    created_at = serializers.DateTimeField(format="%d-%m-%Y", read_only=True)
    cancelled_at = serializers.DateTimeField(format="%d-%m-%Y", read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

class CreateOrderSerializer(serializers.ModelSerializer):
    client_id = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), source='client')
    items = OrderItemSerializer(many=True, write_only=True)

    def validate(self, attrs):
        if len(attrs['items']) == 0:
            raise serializers.ValidationError("Order must have at least one item")
        return attrs
    
    class Meta:
        model = Order
        fields = ['client_id', 'items']

class CreateOrderByClientNameSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField()
    items = OrderItemSerializer(many=True, write_only=True)

    def validate(self, attrs):
        if len(attrs['items']) == 0:
            raise serializers.ValidationError("Order must have at least one item")
        return attrs
    
    class Meta:
        model = Order
        fields = ['client_name', 'items']

class CancelOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id']