"""
API REST basada en Django REST Framework usando ModelViewSet.

Intención de la API:
- Permitir acceso público de lectura (GET) en recursos principales como tareas y usuarios.
- Restringir acciones de escritura (POST, PUT, PATCH, DELETE) según el rol:
    - Tareas: solo el autor o un administrador puede modificar.
    - Usuarios: cada usuario solo puede modificar su propio perfil.
    - Categorías: solo administradores pueden crear o modificar.
- Mantener separación clara entre:
    - Acceso general (has_permission)
    - Acceso a objetos específicos (has_object_permission)

Este diseño sigue el patrón:
👉 "lectura abierta + escritura protegida"
"""

from api.models import Task, User, Category
from api.serializers import TaskSerializer, UserSerializer, CategorySerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

""" SOLAMENTE USAREMOS VIEWSET EN ESTE ARCHIVO"""

# Permiso Personalizado para Tarea
class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        # Lectura para cualquiera, escritura solo autenticados
        # Esto permite que usuarios no autenticados puedan hacer GET (list/retrieve)
        if request.method in permissions.SAFE_METHODS:
            # En SAFE_METHODS estan incluidos GET, HEAD, OPTIONS (Metodos Lectura) 
            return True
        # Para POST, PUT, PATCH, DELETE requiere autenticación
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Permite leer cualquier objeto
        if request.method in permissions.SAFE_METHODS:
            return True 
        # Solo el autor puede modificar su propia tarea
        return obj.author == request.user


# Permiso Personalizado para Usuario
class IsOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        # Solo usuarios autenticados pueden acceder a endpoints protegidos
        # (ej: update, delete, retrieve propio)
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Solo el mismo usuario puede acceder/modificar su propio registro
        # obj aquí es una instancia del modelo User
        return obj == request.user
    

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    # Uso de OR (|):
    # - IsAuthorOrReadOnly permite lectura pública y escritura al autor
    # - IsAdminUser permite control total al administrador
    # Resultado:
    # 👉 Autor O Admin pueden modificar
    permission_classes = [IsAuthorOrReadOnly | IsAdminUser]


class UserViewSet(ModelViewSet):
    # El "guardia de seguridad" — solo deja pasar si tienes token válido
    # Ademas ocultara en el API la lista de usuarios
    #permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    """
    Usaremos esto para personalizar las acciones que 
    requieren permisos especificos
    """

    # Funcion para obtener permisos
    def get_permissions(self):
        # Si la accion es crear obtenemos una lista con la clase vacia,
        # Es decir no necesitamos permisos
        if self.action == 'create':
            self.permission_classes = [AllowAny]

        # IMPORTANTE:
        # Actualmente cualquier usuario autenticado puede intentar acceder a otros usuarios,
        # pero será bloqueado en has_object_permission (IsOwner).
        # Esto permite:
        # - list (GET) visible según autenticación
        # - retrieve/update/delete solo para el propio usuario

        # Si la accion es otra cualquiera, obtenemos una lista con la clase autenticada
        else:
            self.permission_classes = [IsOwner]

        # En todo caso tenemos una list comprehension donde la lista a o b se convertira en objeto
        return [permission () for permission in self.permission_classes]


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        # Son acciones de permissions, revisar documentacion para mas acciones

        # Si la accion esta en la lista necesitaremos permisos de admin
        if self.action in ['create','update','partial_update','destroy']:
            self.permission_classes = [IsAdminUser]

        # Si la accion es otra cualquiera(list = ver), obtenemos una lista con la clase autenticada
        else:
            self.permission_classes = [IsAuthenticated]

        # En todo caso tenemos una list comprehension donde la lista a o b se convertira en objeto
        return [permission () for permission in self.permission_classes]