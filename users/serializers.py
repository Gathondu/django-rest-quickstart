from rest_framework import serializers
from users.models import User

import random
import string


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

class UserVerifyPhoneSerializer(serializers.Serializer):
    verification_code=serializers.CharField(max_length=50,write_only=True)
    