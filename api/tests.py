from django.test import TestCase
from rest_framework.test import APITestCase
#APITestCase ya tiene internamente un APIClient
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Task,Category

class TaskAPITest(APITestCase):
    
    def setUp(self):
        #Setup se ejecutara una sola vez por clase, como un Factory
        self.user = User.objects.create_user(
            username='tester',
            password='passsecure123',
            email='pass@secure.com',
        )
        self.other_user = User.objects.create_user(
            username='viewer',
            password='passsecure123',
            email='viewer@secure.com',
        )
        self.task = Task.objects.create(
            title='Prueba de tareas',
            user=self.user
        )
    def test_list_task_without_autentication(self):
        # Test que probaria que cualquiera puede ver la lista de tareas GET
        response = self.client.get('api/task/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


