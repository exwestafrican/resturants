from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.utils import timezone
from django.contrib.auth import settings

from accounts.custom_serializers import DynamicFieldsHyperlinkedModelSerializer
user = get_user_model()


             
           
             
             
        
               


class UserSerializer(DynamicFieldsHyperlinkedModelSerializer):
    class Meta:
        model = user 
        fields = ['url','id','email','phone_number','first_name','last_name']
       


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
   #show user session start and end 
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        # session_start   = datetime.now(timezone(settings.TIME_ZONE)).strftime("%d-%m-%Y %H:%M:%S")
        # session_end     =  settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']

        data['refresh']  = str(refresh)
        data['access']   = str(refresh.access_token)
        data['message']  = f"hey, {str(self.user)} please note that this time used here is Africa/Lagos"

        data['session start']    = timezone.localtime().strftime("%d-%m-%Y %H:%M:%S")
        
        # print (session_start+session_end)
        # print(session_end)

        return data







# class CreateUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['email','password','phone_number']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = User(
#             email=validated_data['email'],
#             username=validated_data['username']
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user





# class DynamicFieldsHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
#     """
#     A ModelSerializer that takes an additional `fields`and 'read_only_fields argument that
#     controls which fields should be displayed and when some fields should be set as read_only
#     """

#     def __init__(self,*args,**kwargs):
#         # Don't pass the 'fields' arg up to the superclass
#         fields = kwargs.pop('fields', None)

#         read_only_fields = kwargs.pop('read_only_fields',None)
       
#         # Instantiate the superclass normally
#         super(DynamicFieldsHyperlinkedModelSerializer, self).__init__(*args, **kwargs)
       
       
#         if fields is not None:
            
#             allowed     = set(fields)
#             exisiting   = set(self.fields)
            
#             for field_name in exisiting-allowed:
#                 #remove items from dict like obj
#                 self.fields.pop(field_name)
    
#         if read_only_fields is not None:
#             try:
#                 self.Meta.read_only_fields

#             except AttributeError:
#                 raise AttributeError (f"{self.__class__.__name__} does not have an "
#                         "attribute read_only_fields, create an empty list in Meta class to resolve this "
#                         "Class Meta: read_only_fields=[ ]")

#             else:
#                 #using a set to prevent repetition of fields appended to 
#                 # read_only_frields due to user refreshing page
#                 model_read_only_fields = set()
                
#                 for field in read_only_fields:
#                     model_read_only_fields.add(field)
              
#                 self.Meta.read_only_fields = list(model_read_only_fields)