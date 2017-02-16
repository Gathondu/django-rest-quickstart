from django.conf.urls import url,include
from django.contrib import admin

from authentication.views import obtain_expiring_auth_token 
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_swagger.views import get_swagger_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^authenticate/',obtain_expiring_auth_token,name='authenticate'),
    url(r'^users/', include('users.urls',namespace='users')),
   
    url(r'^docs/$', get_swagger_view(title='REST API Documentation'))
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
