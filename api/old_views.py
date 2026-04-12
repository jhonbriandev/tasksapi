from api.models import Task, User
from django.shortcuts import get_object_or_404
from api.serializers import TaskSerializer, UserSerializer
# PARA FBV
from rest_framework.decorators import api_view 
from rest_framework.response import Response 
# PARA GENERICS
from rest_framework.generics import ListCreateAPIView
# PARA VIEWSET
from rest_framework.viewsets import ModelViewSet

"""Todas derivan de Class Based Views CBV"""

# USANDO APIVIEW, FBV
@api_view(['GET'])
def task_list(request):
    tasks = Task.objects.all()
    # Por el HyperVinculo debemos de agregarle contexto bajo la forma de apiview o FBV
    serializer = TaskSerializer(tasks, many= True,context={'request': request})
    return Response(serializer.data)
@api_view(['GET'])
def task_detail(request,pk):
    tasks = get_object_or_404(Task, pk=pk)
    serializer = TaskSerializer(tasks,context={'request': request})
    return Response(serializer.data)
@api_view(['GET'])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many= True,context={'request': request})
    return Response(serializer.data)
@api_view(['GET'])
def user_detail(request,pk):
    users = get_object_or_404(User, pk=pk)
    serializer = UserSerializer(users,context={'request': request})
    return Response(serializer.data)

#USANDO GENERICS
class TaskList(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    """
    perform_create es un método que generics ejecuta justo antes de guardar. 
    Es como decirle: "antes de guardar la tarea, agrégale automáticamente el usuario que está logueado"
    """
    def perform_create(self, serializer):
        serializer.save(author= self.request.user )  

class UserList(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = User


#USANDO VIEWSET
class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
