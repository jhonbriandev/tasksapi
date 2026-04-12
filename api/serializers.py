from rest_framework import serializers
from api.models import Task, User

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    # Le decimos explícitamente cómo encontrar la URL del author
    # view_name='user-detail' → coincide con el basename='user' que usamos en el router
    # read_only=True → porque ya lo tenemos en read_only_fields
    author = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True
    )
    class Meta:
        model = Task
        fields = ['id','title','description','status','priority','author']
        read_only_fields = ['author']
        
    # Validacion rapida para saber si es una tarea o nota
    # Esto se visualiza en el metodo POST en generics
    def validate_title(self,title):
        if 'tarea' not in title.lower():
            raise serializers.ValidationError("Al parecer no es una tarea sino una nota")
        return title

class UserSerializer(serializers.HyperlinkedModelSerializer ):
    class Meta:
        model = User
        fields = ['id','username','email','is_active']
        read_only_fields = ['id','username','email','is_active']