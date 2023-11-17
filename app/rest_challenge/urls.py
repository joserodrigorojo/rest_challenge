from django.urls import include, path, register_converter
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from api import views
from django.contrib import admin
from . import converters

schema_view = get_schema_view(
   openapi.Info(
      title="Senior Backend Software Engineer - Technical Challenge",
      default_version='v1',
      description="Job Application Challenge by Rodrigo Negrete",
      terms_of_service="https://rodrigonegrete.dev",
      contact=openapi.Contact(email="mail@rodrigonegrete.dev"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'clients', views.ClientViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'items', views.ItemViewSet)

register_converter(converters.FourDigitYearConverter, "yyyy")
register_converter(converters.TwoDigitMonthConverter, "mm")
register_converter(converters.TwoDigitDayConverter, "dd")

urlpatterns = [
    path('', include(router.urls)),
    path('orders/', views.GetOrders.as_view()),
    path('orders/<dd:day>/<mm:month>/<yyyy:year>/', views.GetOrdersByDate.as_view()),
    path('orders/cancelled/<dd:day>/<mm:month>/<yyyy:year>/', views.GetOrdersByCancelledDate.as_view()),
    path('orders/<int:order_id>/', views.GetOrderByID.as_view()),
    path('orders/create/', views.CreateOrder.as_view()),
    path('orders/create-by-client-name/', views.CreateOrderByClientName.as_view()),
    path('orders/<int:order_id>/cancel/', views.CancelOrder.as_view()),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
