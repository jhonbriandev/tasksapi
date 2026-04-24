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
            title= 'Tasks tested',
            description = 'Pruebitas',
            status = 'P',
            priority = 'L'
        )

    def test_list_task_without_authentication(self):
        # Verifica que el endpoint es público (no requiere login)
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_user_cannot_view_without_authentication(self):
        # Verifica que /api/users/ es privado — requiere autenticación
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_category_cannot_view_without_authentication(self):
        # Verifica que /api/categories/ es privado — requiere autenticac
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_user_without_authentication(self):
        # POST en /api/users/ es público: permite registrar nuevos usuarios sin login
        # Esto es intencional — un usuario nuevo no puede autenticarse antes de existir 
        response = self.client.post('/api/users/',{
            'username': 'user-test',
            'password':'passsecure123',
            'email' : 'usertested@secure.com'
            })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_task_cannot_without_authentication(self):

    # Este test verifica la capa de AUTENTICACIÓN / PERMISOS
    # No estamos probando validación de datos aquí

    # Flujo interno en DRF:
    # 1. Autenticación → request.user (AnonymousUser)
    # 2. Permisos → FALLA aquí → devuelve 401
    # 3. Serializer → NUNCA se ejecuta
    # 4. Base de datos → NUNCA se ejecuta

        response = self.client.post('/api/tasks/', {
            # No enviamos 'author' porque el backend lo asigna automáticamente
            # usando request.user (si estuviera autenticado)

            # Tampoco es necesario enviar todos los campos,
            # porque este test NO evalúa validación de datos

            # Aunque falten campos obligatorios, eso no importa aquí,
            # ya que la request será rechazada ANTES por falta de autenticación

            'category': self.category.id,
            'title': 'Tarea sin logeo'
        })

        # Esperamos 401 porque el usuario NO está autenticado
        # (no pasa la capa de permisos)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_create_task_with_authentication(self):

        # Este test verifica el flujo completo exitoso:
        # 1. Autenticación → OK (force_authenticate)
        # 2. Permisos → OK
        # 3. Serializer → valida datos
        # 4. Guardado → se crea la tarea

        # IMPORTANTE:
        # force_authenticate simula un usuario logueado sin necesidad de login real
        # request.user será igual a self.user
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/tasks/', {
            # En este caso SÍ estamos probando creación real,
            # por eso debemos enviar todos los campos requeridos

            'category': self.category.id,
            'title': 'Tarea con force autentificacion',
            'description': 'Pruebitas',

            # Estos campos tienen default en el modelo,
            # pero DRF puede requerirlos si no se configuran como opcionales
            'status': 'P',
            'priority': 'L'
        })

        # Esperamos 201 porque:
        # - Usuario autenticado
        # - Permisos correctos
        # - Datos válidos
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Además del código 201 (línea anterior),
        # verificamos que el título guardado coincide con el que enviamos
        # Esto Verifica que lo que enviamos es lo que se guardó
        self.assertEqual(response.data['title'], 'Tarea con force autentificacion')
    
    def test_update_my_task_with_authentication(self):
        self.client.force_authenticate(user=self.user)
        # Usamos PATCH (actualización parcial) en lugar de PUT (reemplazo total)
        # PATCH permite enviar solo los campos que queremos cambiar
        # PUT requeriría enviar TODOS los campos obligatoriamente
        response = self.client.patch(f'/api/tasks/{self.task.id}/',{
            'category': self.category.id,
            'title': 'Tarea con force autentificacion',
            'description': 'Pruebitas',
            'status': 'P',
            'priority': 'L'

        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_update_stranger_my_task_with_authentication(self):
        self.client.force_authenticate(user=self.other_user)
        # Este caso es similar al anterior pero con la diferencia que este
        # autor no es el mismo que creo la tarera USER != OTHER_USER
        # Por lo cual aunque este autenticado no deberia de modificar tareas que no son suyas
        response = self.client.patch(f'/api/tasks/{self.task.id}/',{
            'category' : self.category.id,
            'title' : ' Soy extrano y quiero editar esta tarea ajena',
            'description' : 'Editando tareas ajenas JJJJ',
            'status' : 'P',
            'priority' : 'L'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    

    def test_delete_my_task_with_authentication(self):
        self.client.force_authenticate(user = self.user)
        # Teniendo en cuenta que las tareas base son las que se crean en Setup y no las del test
        # Vamos a eliminar esa tarea, que pertenece al mismo usuario que tenemos en esta autenticacion
        # self.user de SetUp =  self.user de force)
        response = self.client.delete(f'/api/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_cannot_delete_stranger_my_task_with_authentication(self):
        # En este caso se hace la simulacion de autenticacion con el 'otro user'
        # El cual no es propietario de la tarea
        # Entonces el test busca probar que un extraño no puede eliminar tareas no propias
        self.client.force_authenticate(user = self.other_user)
        response = self.client.delete(f'/api/tasks/{self.task.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_filter_task_status(self):
        # Solo para ver, y filtrar no modificar
        response = self.client.get('/api/tasks/?status=P')
        # Verifica que el filtro por status funciona correctamente
        # '?status=P' filtra tareas con estado 'Pending'
        # filterset_fields en el ViewSet habilita este tipo de filtrado por query params
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # FIN DE TESTS