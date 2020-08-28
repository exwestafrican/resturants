from django.urls import path
from products import views


urlpatterns = [
    path("all/", views.ProductList.as_view(), name="product-list"),
    # product variation , all
    path("category/", views.ProductCategoryList.as_view(), name="cateogry-list"),
    path(
        "category/<int:pk>/",
        views.ProductCategoryDetail.as_view(),
        name="category-detail",
    ),
    path("<int:pk>/", views.ProductDetail.as_view(), name="product-detail"),
    path(
        "variation/all/",
        views.ProductVariationListCreate.as_view(),
        name="create-product-variation",
    ),
    path(
        "<str:product_name>/<int:pk>/",
        views.ProductVariationDetail.as_view(),
        name="productvariation-detail",
    ),
    path("addons/all/", views.AddonItemList.as_view(), name="product-addons-list"),
    path(
        "addons/<str:name>/",
        views.AddonItemDetail.as_view(),
        name="product-addons-detail",
    )


    
    # path('package/',views.PackageList.as_view(),name='package-list'),
    # #package list , displays all packages and allows creation of a new one
    # path('package/<str:slug>/',views.PackageDetail.as_view(),name='package-detail'),
    # path('package/content/<int:pk>',views.PackageContentDetail.as_view(),name='package-content-detail'),
    # path('create/package/',views.CreatePackageContent.as_view(),name='create-packageContent')
]
