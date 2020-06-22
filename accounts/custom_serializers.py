from rest_framework import serializers


class DynamicFieldsHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    """
    A ModelSerializer that takes an additional `fields`and 'read_only_fields argument that
    controls which fields should be displayed and when some fields should be set as read_only
    """

    def __init__(self,*args,**kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        read_only_fields = kwargs.pop('read_only_fields',None)
       
        # Instantiate the superclass normally
        super(DynamicFieldsHyperlinkedModelSerializer, self).__init__(*args, **kwargs)
       
       
        if fields is not None:
            
            allowed     = set(fields)
            exisiting   = set(self.fields)
            
            for field_name in exisiting-allowed:
                #remove items from dict like obj
                self.fields.pop(field_name)
    
        if read_only_fields is not None:
            try:
                self.Meta.read_only_fields

            except AttributeError:
                raise AttributeError (f"{self.__class__.__name__} does not have an "
                        "attribute read_only_fields, create an empty list in Meta class to resolve this "
                        "Class Meta: read_only_fields=[ ]")

            else:
                #using a set to prevent repetition of fields appended to 
                # read_only_frields due to user refreshing page
                model_read_only_fields = set()
                
                for field in read_only_fields:
                    model_read_only_fields.add(field)
              
                self.Meta.read_only_fields = list(model_read_only_fields)




class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields`and 'read_only_fields argument that
    controls which fields should be displayed and when some fields should be set as read_only
    """

    def __init__(self,*args,**kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
      

        read_only_fields = kwargs.pop('read_only_fields',None)
       
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
       
       
        if fields is not None:
            
            allowed     = set(fields)
            exisiting   = set(self.fields)
            
            for field_name in exisiting-allowed:
                #remove items from dict like obj
                self.fields.pop(field_name)
    
        if read_only_fields is not None:
           
            try:
                self.Meta.read_only_fields

            except AttributeError:
                raise AttributeError (f"{self.__class__.__name__} does not have an "
                        "attribute read_only_fields, create an empty list in Meta class to resolve this "
                        "Class Meta: read_only_fields=[ ]")

            else:
                #using a set to prevent repetition of fields appended to 
                # read_only_frields due to user refreshing page
                model_read_only_fields = set()
                
                for field in read_only_fields:
                    model_read_only_fields.add(field)
              
                self.Meta.read_only_fields = list(model_read_only_fields)
             