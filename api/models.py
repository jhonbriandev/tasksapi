from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name ='users')
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=200)

    class Status(models.TextChoices):
        PENDING = "P", "Pendiente"
        IN_PROGRESS = "I" ,"En progreso"
        COMPLETED = "C", "Completado"
    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.PENDING
    )
    class Priority(models.TextChoices):
        LOW = "L", "Bajo"
        REGULAR = "R", "Regular"
        HIGH = "H", "Alto"
    priority = models.CharField(
        max_length=1,
        choices=Priority.choices,
        default=Priority.LOW
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title

# Create your models here.
