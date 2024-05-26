from django.test import TestCase
from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse

#Tests
# Se crea una nueva instancia para testear los endpoints

class UserAccountAPITest(APITestCase):
     
    def setUp(self):
        #La configuración se ejecuta antes de cada método de prueba.
        pass

    def tearDown(self):
        #Limpia la ejecución después de cada método de prueba.
        pass