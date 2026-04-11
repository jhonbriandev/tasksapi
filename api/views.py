from api.models import Task
from api.serializers import TaskSerializer
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
    serializer = TaskSerializer(tasks, many= True)
    return Response(serializer.data)

#USANDO GENERICS
class TaskList(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

#USANDO VIEWSET
class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
