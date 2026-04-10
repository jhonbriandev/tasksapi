from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Task
from api.serializers import TaskSerializer

@api_view(['GET'])
def task_list(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many= True)
    return Response(serializer.data)

