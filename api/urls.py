from django.contrib import admin
from django.urls import path
from rest_framework import routers
# Para FBV
from  .import views
# Para Generics Y Viewset
from api.views import TaskList, TaskViewSet

#router = routers.SimpleRouter()
#router.register(r'tasks', task_list)

#urlpatterns = router.urls

urlpatterns = [
    path('tasks/',views.task_list),
    path('tasks_generic/',TaskList.as_view()), # Para generics
        # En este caso no podemos pasar el as_view vacio
        # Necesitamos pasarle argumentos
        # el post o get y los distintos metodos create, list, delete segun correspondan
        # siempre en un diccionario
    path('tasks_view/',TaskViewSet.as_view({'post':'create'})), # Para viewset

]