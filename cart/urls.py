from django.urls import path
from cart import views



urlpatterns = [
    path('',views.CartList.as_view(),name='cart-list'),
    path('item/',views.CartItemList.as_view(),name='cart_item-list')
]