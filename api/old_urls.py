from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
# Para FBV
from  .import old_views
# Para Generics Y Viewset
from tasksapi.api.old_views import TaskList, TaskViewSet, UserList

""" 
RUTAS DE EJEMPLO PARA LAS ANTIGUAS VISTAS 
SE USARON FBV, APIVIEWS Y VIEWSETS
"""
urlpatterns = [
    path('tasks/',old_views.task_list),
    path('users/',old_views.user_list),
    # Por defecto en FBV O APIVIEW los details se llaman ej: task-detail
    # Entonces para coincidir debemos de agregar el name del url
    path('tasks/<int:pk>',old_views.task_detail, name='task-detail'),
    path('users/<int:pk>',old_views.user_detail, name='user-detail'),
    
    path('tasks_generic/',TaskList.as_view()), # Para generics
        # En este caso no podemos pasar el as_view vacio
        # Necesitamos pasarle argumentos
        # el post o get y los distintos metodos create, list, delete segun correspondan
        # siempre en un diccionario
    path('users_generic/', UserList.as_view()),
    path('tasks_view/',TaskViewSet.as_view({'post':'create'})), # Para viewset

]