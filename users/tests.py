from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.urlresolvers import reverse

#Tests
# Se crea una nueva instancia para testear los endpoints

class UserAccountAPITest(APITestCase):
     
    def setUp(self):
        self.client.post(reverse('user-account-add'), {'username': "fulanito", 'password': 123456789})


    def test_get_info_user(self):
        response = self.client.get(reverse('info-user-get', kwargs={'id': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_info_user(self):
        data = {'client': "sultanita", 'password': 123456789}
        response = self.client.post(reverse('info-user-add'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)    

    def tearDown(self):
        #Limpia la ejecución después de cada método de prueba.
        pass