from django.urls import path
from products import views



urlpatterns = [
    path('all/',views.ProductList.as_view(),name='product-list'),
    path('category/',views.ProductCategoryList.as_view(),name='cateogry-list'),
    path('category/<str:slug>/',views.ProductCategoryDetail.as_view(),name='category-detail'),
    path('<int:pk>/',views.ProductDetail.as_view(),name='product-detail'),
    path('variation/create/',views.ProductVariationCreate.as_view(),name='create-product-variation'),
    path('variation/<int:pk>/',views.ProductVariationDetail.as_view(),name='productvariation-detail'),
    
    
]