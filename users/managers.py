
from django.contrib.auth.base_user import BaseUserManager



class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email,phone_number,id_number, password, **extra_fields):
        #do validations
        if not email:
            raise ValueError('The given email must be set')
        if not phone_number:
            raise ValueError('The Phone Number is needed ')
        if not id_number:
            raise ValueError('The given ID Number  must be set')
        email = self.normalize_email(email)

        user = self.model(email=email,phone_number=phone_number,id_number=id_number, **extra_fields)
        #set default passwords and send email
        if user.is_superuser:
            user.level=1
        elif user.is_staff:
            user.level=2
        

        user.set_password(password)
        user.is_active=True
        user.save(using=self._db)
        return user

    def create_user(self, email,phone_number,id_number,password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email,phone_number,id_number,password,**extra_fields)
        
    
   
    

    def create_superuser(self, email, phone_number,id_number,password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email,phone_number,id_number, password, **extra_fields)
        
        

