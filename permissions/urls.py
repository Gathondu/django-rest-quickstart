from django.conf.urls import url

from .views import *

urlpatterns=[
           
            url('^$',PermissionsList.as_view()),
           
             ]
