from api.models import Task, User
from django.shortcuts import get_object_or_404
from api.serializers import TaskSerializer, UserSerializer
from rest_framework.viewsets import ModelViewSet

""" SOLAMENTE USAREMOS VIEWSET EN ESTE ARCHIVO"""

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer