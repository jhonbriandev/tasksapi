from api.models import Task, User
from django.shortcuts import get_object_or_404
from api.serializers import TaskSerializer, UserSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

""" SOLAMENTE USAREMOS VIEWSET EN ESTE ARCHIVO"""

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class UserViewSet(ModelViewSet):
    # El "guardia de seguridad" — solo deja pasar si tienes token válido
    # Ademas ocultara en el API la lista de usuarios
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

 