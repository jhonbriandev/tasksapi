from django.contrib import admin
from django.urls import path
from rest_framework import routers
from  .import views

#router = routers.SimpleRouter()
#router.register(r'tasks', task_list)

#urlpatterns = router.urls

urlpatterns = [
    path('tasks/',views.task_list),
]