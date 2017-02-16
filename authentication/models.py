from django.db import models


from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from rest_framework import exceptions

from datetime import timedelta

class ExpiringTokenAuthentication(TokenAuthentication):
    model=Token
    def authenticate_credentials(self, key):

        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid Token')
        
        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User is inactive or deleted')

        if token.created < timezone.now() - timedelta(minutes=6000):
            raise exceptions.AuthenticationFailed('Token has expired')
        
        #update token created date for active users
        token.created = timezone.now()
        token.save() 

        return token.user, token
    