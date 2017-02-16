from rest_framework import serializers
from users.models import User

#from drf_extra_fields.fields import Base64ImageField
import random
import string
from django.conf import settings

from django.contrib.auth.models import Permission,Group
from django.contrib.contenttypes.models import ContentType

class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=ContentType
        fields='__all__'


class UserPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Permission
        fields='__all__'

class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        #depth=1
        model=Group
        fields='__all__'

class UserGroupAddUserSerializer(serializers.Serializer):
    group=serializers.IntegerField()
    action=serializers.IntegerField()
    user=serializers.CharField(max_length=300)

class UserSerializer(serializers.ModelSerializer):
  
    permissions=serializers.ListField(read_only=True)


    class Meta:
        model=User
        exclude=('user_permissions','groups','created_by',)
        extra_kwargs={'password':{'write_only':True}}
        
    def create(self,validated_data): 
        created_by=validated_data.get('created_by')
        random_password=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
        email=validated_data.pop('email')

        #create user
        password=validated_data.pop('password')
       
       
        if created_by:
            password=random_password

        return User.objects.create_user(email=email,password=password,**validated_data)



        
class UserChangePasswordSerializer(serializers.Serializer):
    #user=serializers.CharField(max_length=200,write_only=True)
    old_password=serializers.CharField(max_length=50,write_only=True)
    new_password=serializers.CharField(max_length=50,write_only=True)
    new_password_again=serializers.CharField(max_length=50,write_only=True)
    

    
   
class UserResetPasswordSerializer(serializers.Serializer):
    email=serializers.CharField(max_length=50,write_only=True)
  

class UserVerifyEmailSerializer(serializers.Serializer):
    verification_code=serializers.CharField(max_length=50,write_only=True)
   