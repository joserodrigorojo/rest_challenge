from datetime import datetime
from rest_framework import viewsets, permissions, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from api.services import order_service
from api.serializers import *
from api.models import *

class GetOrders(APIView):
    @swagger_auto_schema(responses={200: OrderSerializer(many=True)})
    def get(self, request, format=None):
        service = order_service.OrderService()
        orders = service.list_orders()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class GetOrdersByDate(APIView):
    @swagger_auto_schema(responses={200: OrderSerializer(many=True)})
    def get(self, request, day, month, year, format=None):
        date_obj = datetime.strptime(f'{day}/{month}/{year}', '%d/%m/%Y')
        service = order_service.OrderService()
        orders = service.list_orders_by_date(date_obj)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class GetOrdersByCancelledDate(APIView):
    @swagger_auto_schema(responses={200: OrderSerializer(many=True)})
    def get(self, request, date, format=None):
        service = order_service.OrderService()
        orders = service.list_orders_by_cancelled_date(date)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class GetOrderByID(APIView):
    @swagger_auto_schema(responses={200: OrderSerializer()})
    def get(self, request, order_id, format=None):
        service = order_service.OrderService()
        order = service.get_order(order_id)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

class CreateOrder(APIView):
    @swagger_auto_schema(request_body=CreateOrderSerializer, responses={201: CreateOrderSerializer()})
    def post(self, request, format=None):
        serializer = CreateOrderSerializer(data=request.data)
        if serializer.is_valid():
            service = order_service.OrderService()
            order = service.create_order(serializer.validated_data['client'], serializer.validated_data['items'])
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateOrderByClientName(APIView):
    @swagger_auto_schema(request_body=CreateOrderByClientNameSerializer, responses={201: CreateOrderByClientNameSerializer()})
    def post(self, request, format=None):
        serializer = CreateOrderByClientNameSerializer(data=request.data)
        if serializer.is_valid():
            service = order_service.OrderService()
            order = service.create_order_by_client_name(serializer.validated_data['client_name'], serializer.validated_data['items'])
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CancelOrder(APIView):
    @swagger_auto_schema(responses={200: OrderSerializer()})
    def put(self, request, order_id, format=None):
        service = order_service.OrderService()
        order = service.get_order(order_id)
        serializer = OrderSerializer(order)
        if order.cancelled:
            return Response(serializer.data, status=status.HTTP_409_CONFLICT)
        serializer = CancelOrderSerializer(order, data=request.data)
        if serializer.is_valid():
            service.cancel_order(order_id, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.AllowAny]

class ItemViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [permissions.AllowAny]

class CategoryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]