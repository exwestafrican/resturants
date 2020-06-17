from django.shortcuts import render
from django.contrib.auth import get_user_model



from rest_framework import generics
from rest_framework.response import Response
from accounts.serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.serializers import UserSerializer




user = get_user_model()

# Create your views here.
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



class UserList(generics.ListAPIView):
    """
    Allows admin create user but 
    lets none admin and admin see a list of users
    """

    queryset = user.objects.all()
    serializer_class = UserSerializer
    fields = ["url","id","email",]
    #add admin or real only permission
    #add authentication
    #add a Create method 

    def list(self, request, *args, **kwargs):
        """ 
        method runs when get is called, fields
        gets passed as a kwarg. 
        """
        queryset = self.filter_queryset(self.get_queryset())
        fields = self.fields
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset,fields=fields, many=True)
        return Response(serializer.data)


class UserDetail(generics.RetrieveAPIView):
    """returns a single user"""
    queryset = user.objects.all()
    serializer_class = UserSerializer
    fields = ['id','email','phone_number','first_name','last_name']


    def retrieve(self, request, *args, **kwargs):
        """ 
        method is run by get to retrieve element by
        pk as specified in look_up_url.and pass instance 
        to call class fields argument is added to kwargs
        to take advange of DynamicFieldsHyperlinkedModelSerializer
        """
        instance = self.get_object()
        fields = self.fields
        serializer = self.get_serializer(instance,fields=fields)
        return Response(serializer.data)




