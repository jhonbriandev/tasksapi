from django.contrib import admin
from django.urls import path
from rest_framework import routers
# Para FBV
from  .import views
# Para Generics Y Viewset
from api.views import TaskList, TaskViewSet, UserList

#router = routers.SimpleRouter()
#router.register(r'tasks', task_list)

#urlpatterns = router.urls

urlpatterns = [
    path('tasks/',views.task_list),
    path('users/',views.user_list),
    # Por defecto en FBV O APIVIEW los details se llaman ej: task-detail
    # Entonces para coincidir debemos de agregar el name del url
    path('tasks/<int:pk>',views.task_detail, name='task-detail'),
    path('users/<int:pk>',views.user_detail, name='user-detail'),
    
    path('tasks_generic/',TaskList.as_view()), # Para generics
        # En este caso no podemos pasar el as_view vacio
        # Necesitamos pasarle argumentos
        # el post o get y los distintos metodos create, list, delete segun correspondan
        # siempre en un diccionario
    path('users_generic/', UserList.as_view()),
    path('tasks_view/',TaskViewSet.as_view({'post':'create'})), # Para viewset

]