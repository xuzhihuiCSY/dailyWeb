from django.urls import path
from .views import Ecommerce_index, product_detail, add_to_cart, remove_from_cart, cart, checkout, order_confirmation

app_name = 'ecommerce'

urlpatterns = [
    path('Ecommerce_index', Ecommerce_index, name='Ecommerce_index'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('order_confirmation/<int:order_id>/', order_confirmation, name='order_confirmation'),
]