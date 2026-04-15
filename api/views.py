from api.models import Task, User, Category
from django.shortcuts import get_object_or_404
from api.serializers import TaskSerializer, UserSerializer, CategorySerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny

""" SOLAMENTE USAREMOS VIEWSET EN ESTE ARCHIVO"""

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # Por defecto necesitamos logearnos, asi lo configuramos en settings
    # pero si quisieramos verlo sin ese permiso:
    # permission_classes = [AllowAny]
class UserViewSet(ModelViewSet):
    # El "guardia de seguridad" — solo deja pasar si tienes token válido
    # Ademas ocultara en el API la lista de usuarios
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
 
 