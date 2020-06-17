from django.urls import path
from accounts import views



urlpatterns = [
    path('',views.UserList.as_view(),name='user_list'),
    path('<int:pk>/',views.UserDetail.as_view(),name='user-detail')
]