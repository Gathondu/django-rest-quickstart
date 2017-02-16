
from users.models import User

class CustomBackend(object):
    """authenticate when given email, password """
    
  
        
    def get_by_email(self,email,password):
        try:
           # Try to fetch the user by searching the username or email field
            #user = User.objects.get(Q(phone_number=phone_number)|Q(email=email)|Q(secret_key=secret_key))
            
            user = User.objects.get(email=email)
            if password:
                if user.check_password(password):
                    return user
            else:
                return user
        except User.DoesNotExist:
            pass


    def authenticate(self, email=None, password=None, **kwargs):
        
        if email:
            return self.get_by_email(email, password)
        else:
            return None
            
        
        
    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None
        
        
        
        