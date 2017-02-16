from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class UserTests(APITestCase):
    def test_create_user(self):
        """
        Ensure new user can be created
        """
        url=reverse('users:user_list')
        data={'first_name':"morfat",'last_name':'mosoti',
              'email':'morfatmosoti@test.com','password':'admin2016',
              'phone_number':'254700872844'
              }
        response=self.client.post(url,data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(),1)
        self.assertEqual(User.objects.get().email,'morfatmosoti@test.com')

