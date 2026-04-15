from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from . import views
from api.views import  TaskViewSet

""" 
SOLO SE USA VIEWSETS
"""

router = DefaultRouter()

# 2️⃣ Registrar tu ViewSet en el router
# "tasks" = la URL que tendrás → /tasks/
# views.TaskViewSet = tu ViewSet en views.py
# basename = nombre interno para identificar las rutas
""" 
Se usa el basename task o user
Pero el sistema genra automaticamente 
    basename='task'  --->   task-list, task-detail
    basename='user'  --->   user-list, user-detail
"""
router.register(r'tasks', views.TaskViewSet, basename='task')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'users', views.UserViewSet, basename='user')

# 3️⃣ Conectar el router al urlpatterns
urlpatterns = [
    path('', include(router.urls)),  # El router genera automáticamente las rutas
]