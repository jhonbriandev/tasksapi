from django.test import TestCase
from rest_framework.test import APITestCase
# APITestCase ya incluye internamente un APIClient
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Task, Category


class TaskAPITest(APITestCase):

    def setUp(self):
        # Se ejecuta antes de cada test para garantizar un estado limpio
        self.user = User.objects.create_user(
            username='tester',
            password='passsecure123',
            email='pass@secure.com'
        )
        self.other_user = User.objects.create_user(
            username='viewer',
            password='passsecure123',
            email='viewer@secure.com'
        )
        self.category = Category.objects.create(name='Familiar')

        self.task = Task.objects.create(
            author=self.user,
            category=self.category,
            title='Prueba de tareas'
        )

    def test_list_task_without_autentication(self):
        # Verifica que el endpoint es público (no requiere login)
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)