from django.contrib.auth.models import Permission,Group
from rest_framework import generics
from utils.views import TransactionalViewMixin
from .serializers import *


class PermissionsList(TransactionalViewMixin,generics.ListCreateAPIView):
    
    #error_message =" "
    #success_messgae = ""
    """" used to get permissions and group permissions.
    to filter permissions use:
    group,find where group is the group id to search for permissions and find is the type 
    of permissions to return. This can be  'unselected','selected',
    where 'unselected' returns permissions not linked to the group 
    and 'selected' returns permissions that are linke to the group. 
    """

 
    serializer_class=PermissionSerializer
    
    search_fields=('codename','name',)

    
    def perform_create(self,serializer):
        serializer.save()

    def get_queryset(self):
        group=self.request.GET.get('group')
        find=self.request.GET.get('find')
     
        if not find and not group:
            #return just permissions
            return Permission.objects.all()
        elif group and find:
            #get permissions per group and find keys
            group=Group.objects.get(pk=group)
            if find=='selected':
                return group.permissions.all()
            elif find=='unselected':
                #return Permissions not selected... for the group 
                return Permission.objects.exclude(id__in=[p.id for p in group.permissions.all()])




