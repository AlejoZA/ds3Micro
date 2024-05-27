from django.test import TestCase
from rest_framework.test import APITestCase 
from rest_framework import status 
from django.urls import reverse
from .models import OtpCode
from . import urls

#Tests
# Se crea una nueva instancia para testear los endpoints

class UserAccountAPITest(APITestCase):
     
    def setUp(self):
        self.client.post(reverse('users:login'), {'username_or_email' , 'password'})


    def test_add_info_user(self):
        data = {'username_or_email':"laura@gmail.com" , 'password':"123456789"}
        response = self.client.post(reverse('users:login'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)   


    def test_get_info_user(self):
        response = self.client.get(reverse('users:login', kwargs={'username_or_email':"laura@gmail.com"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_update_info_user(self):
        data = {'username_or_email':"lauraMurillas@gmail.com", 'password': "123456789"}
        response = self.client.put(reverse('users:login', kwargs={'username_or_email':"laura@gmail.com"}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_info_user(self):
        response = self.client.delete(reverse('users:login', kwargs={'username_or_email':"laura@gmail.com"}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) 

   
    #def tearDown(self):
        #Limpia la ejecución después de cada método de prueba.
    #    pass
   

