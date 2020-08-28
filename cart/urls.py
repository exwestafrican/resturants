from django.urls import path
from cart import views


urlpatterns = [
    path("", views.CartList.as_view(), name="cart-list"),
    path(
        "create-empty-cart/", views.CreateEmptyCart.as_view(), name="create-empty-cart"
    ),
    path(
        "item/<int:pk>/", views.EditDestroyCartItem.as_view(), name="cart-item-detail",
    ),
    path("item/", views.AddItemsToCart.as_view(), name="cart_item-list"),
]

