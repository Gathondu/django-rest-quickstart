
from users.models import User

class CustomBackend(object):
    """authenticate when given email, password """
    
  
    def is_phone_number(self,var):
        try:
            return int(var)
        except ValueError:
            #this is not integer its email. 
            return False

   
    def get_by_phone_number(self,phone,password):
        try:
            user = User.objects.get(phone_number=phone)
            if password:
                if user.check_password(password):
                    return user
            else:
                return user
        except User.DoesNotExist:
            return None 

    def get_by_email(self,email,password):
        try:
            user = User.objects.get(email=email)
            if password:
                if user.check_password(password):
                    return user
            else:
                return user
        except User.DoesNotExist:
            pass


    def authenticate(self, email=None, password=None, **kwargs):
        phone_number=self.is_phone_number(email) #check if email field is also phone number 
        if phone_number:
            return self.get_by_phone_number(phone_number, password)
        return self.get_by_email(email,password)

            
        
        
    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None
        
        
        
        