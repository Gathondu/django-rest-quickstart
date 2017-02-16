
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.permissions import AllowAny

from rest_framework import generics

from rest_api import  settings
from utils.views import TransactionalViewMixin
from users.serializers import *
from users.models import User,Code




class UserList(TransactionalViewMixin,generics.ListCreateAPIView):
    """ used for user signup and listing users. to return only staff use: staff_only=true or give any variable. """
   
    serializer_class=UserSerializer
  
    
    filter_fields = ('first_name','last_name','email','groups',)
    
    search_fields=('first_name','last_name','email',)

    #authentication_classes = ()
    permission_classes = (AllowAny,)

    def perform_create(self,serializer):
        serializer.save()

    def get_queryset(self):
        user=self.request.user
        if user and user.is_authenticated():
            #return as per logged in user
            if user.is_superuser:
                return User.get_all()
            elif user.is_staff:
                return User.get_staff_and_normal()
        return User.objects.none()


    


class UserDetail(TransactionalViewMixin,generics.RetrieveUpdateAPIView):
    """ you can also mmake partial updates using PUT. 
    if password field is provided, the password will change. but no email/ notification will be sent to User
    regarding the changes
    """

    serializer_class=UserSerializer
    queryset=User.objects.all()

   
    
    def put(self, request, pk, format=None):
        user = self.get_object()
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            valid_data = serializer.validated_data
            serializer.save()

            if valid_data.get('password'):
                user.set_password(valid_data.get('password'))
                user.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_destroy(self,model_object):
        model_object.is_active=True
        model_object.save()


 
   

    



class UserChangePassword(TransactionalViewMixin,generics.CreateAPIView):
    """To change password, enter the required fields old_password,new_password,new_password_again and user.
    user will receive an email of the notification on successful reset. Also to verify email or phone number that 
    password was set to, include the field in your post request. 
    """
    
    serializer_class=UserChangePasswordSerializer
  
    error_message="All the fields are required"
    success_message="Your password was changed succesfully."
    
    
    def post(self, request,format=None):
        serializer = UserChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            valid_data=serializer.validated_data
            #chec if passwords match
            user=request.user

            old_password=valid_data.get('old_password')
            new_password=valid_data.get('new_password')
            new_password_again=valid_data.get('new_password_again')
            if new_password != new_password_again:
                #passwords do not match . fail
                self.error_message="Please enter the same password twice."
                raise serializers.ValidationError({'new_password':"Passwords do not match",
                                                   'new_password_again':"Passwords do not match"})
            
            #check if user with this password exists
            if not user.check_password(old_password):
                #not found
                self.error_message="Please enter your correct  password."
                raise serializers.ValidationError({'old_password':"Incorrect password"})
         
            #change password here also verify email if user is same.
            user.set_password(new_password)
            user.is_password_changed=True
            #if email is passed, validated email also. since user received password vial email
            if valid_data.get('email') and valid_data.get('phone_number'):
                #incorrect options for verifiyn
                raise serializers.ValidationError({'email':"Enter email or phone_number or None",
                                                   'phone_number':"Enter email or phone_number or None"})

            if user.email==valid_data.get('email'): #applies if email is unique field
                user.is_email_verified=True
            if user.phone_number==valid_data.get('phone_number'): #applies if phone number is unique field
                user.is_phone_number_verified=True
            user.save()

            #send mail
            message='body:Password Changed Successfully'
            template_id=settings.EMAIL_TEMPLATES.get('USER_SELF_PASSWORD_CHANGE')
            self.send_email(message=message,recipient=user.email,template_id=template_id)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    

    
    
class UserResetPassword(TransactionalViewMixin,generics.CreateAPIView):
    
    """
    Uses only POST
    email field is required.
    To reset password after email request you need:
    reset_code,new_password,email,new_password_again fields. 
    To request for a reset of password: 
    you required email field only.


    @todo Mosot refine these code later, to suit the password reset process we aggreed
    """
    
    serializer_class=UserResetPasswordSerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)

    error_message="Oops something went wrong"
    success_message="Success"
    

    def post(self, request,format=None):
        serializer = UserResetPasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            valid_data=serializer.validated_data
            email=valid_data.get('email')
            try:
                user=User.objects.get(email=email)
                reset_code  = self.get_reset_code()
                user.set_password(reset_code)
                user.is_password_changed = False
                #send mail /Please intergrate asychronous task for these
                user.is_active = True
                self.send_default_pass(user,reset_code)
                user.save()
                self.success_message = "We send you a temporary passcode./Plese use it as a temporary password"
                return Response(serializer.data)
            except:
                self.error_message="Oops please check that your email is correct."
                raise serializers.ValidationError({'email':"User with this email Does not exist !"})
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_reset_code(self):
        return  ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))


    def send_default_pass(self,user,reset_code):
        message = 'fname:%s,password:%s' % (user.first_name,reset_code)
        template_id = settings.EMAIL_TEMPLATES.get('PASSWORD_RESET_SUCCESS')
        self.send_email(message=message, recipient=user.email, template_id=template_id)
        if user.phone_number:
            try:
                self.send_sms(reset_code,user.phone_number)
            except:
                # @todo  mosoti how do we handle these exeception
                return True;
        else:
            return True



  

class UserVerifyEmail(TransactionalViewMixin,generics.ListCreateAPIView):
    """To verify email. For sending code, use GET for veification of the code received in email use POST
    For logged in users. 
    """
    
    serializer_class=UserVerifyEmailSerializer
    
    error_message="All the fields are required"
    success_message="Succesfully."
    
    def get_queryset(self):
        #send email verification code for looged in use 
        user=self.request.user
        code=Code.generate(user=user,reason=Code.EMAIL_VERIFICATION)
        return []

    
    def post(self, request,format=None):
        serializer = UserVerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            valid_data=serializer.validated_data
            #chec if passwords match
            user=request.user

            verification_code=valid_data.get('verification_code')
            code=Code.is_valid(user=user,reason=Code.EMAIL_VERIFICATION,code=verification_code)
            if code:
                #valid 
                user.is_email_verified=True
                user.save()
                self.success_message="Email verified"
                #remove the Code
                code.delete()
            else:
                #incorrect options for verifiyn
                raise serializers.ValidationError({'verification_code':"The code is invalid."})
                self.error_message="Please enter correct code"
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    