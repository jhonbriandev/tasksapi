from rest_framework import serializers
from api.models import Task, User, Category

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    # Le decimos explícitamente cómo encontrar la URL del author
    # view_name='user-detail' → coincide con el basename='user' que usamos en el router
    # read_only=True → porque ya lo tenemos en read_only_fields
    author = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True
    )
    # Muestra el ID numérico
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )
    # Muestra la URL clickeable (solo lectura, para navegar)
    category_url = serializers.HyperlinkedRelatedField(
        view_name='category-detail',
        read_only=True,
        source='category'  # ← apunta al mismo campo
    )

    class Meta:
        model = Task
        fields = ['id','title','category','category_url','description','status','priority','author']
        read_only_fields = ['author','category_url']
        
    # Validacion rapida para saber si es una tarea o nota
    # Esto se visualiza en el metodo POST en generics
    # comentado porque en postman es mas estricto
    #def validate_title(self,title):
    #    if 'tarea' not in title.lower():
    #        raise serializers.ValidationError("Al parecer no es una tarea sino una nota")
    #    return title

    def create(self, validated_data):
        # El usuario viene del contexto de la request, no del JSON
        users = self.context['request'].user
        # Usamos author puesto que es el nombre del campo(FK) que vamos a comparar con la variable users
        return Task.objects.create(author=users, **validated_data)
        # Esto genera que se cree un task, tomando del contexto request el user, en este caso author
        # Posteriormente tomando todos los demas datos por eso usamos **kwargs
    
    """
    Para usarlo en postman:
    --PARA CREAR--
    {
    "title": "Tarea de pruebasa",
    "category" : 1,
    "description": "Pruebita",
    "status": "P",
    "priority": "H"
    }  
    --PARA ACTUALIZAR-- 
    {
    "id": 5,
    "title": "Tarea de prueba 3 - editada2",
    "category": 1,
    "category_url": "http://127.0.0.1:8000/api/categories/1/",
    "description": "Pruebita 3",
    "status": "P",
    "priority": "H",
    "author": "http://127.0.0.1:8000/api/users/10/"
    }
    """

class UserSerializer(serializers.HyperlinkedModelSerializer ):
    # Se crea el hypercinculo para acceder a los detalles
    # de cada usuario y verlos de manera independiente
    # IMPORTANTE USAR hyperlinkedidentity y no Reelated
    # Related se usa para las llaves foraneas
    # Identity para un campo nuevo
    url = serializers.HyperlinkedIdentityField(
        view_name = 'user-detail',
        read_only = True,      
    )
    # Para agregar el campo password hasheado
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id','url','username','email','password']
        read_only_fields = ['id'] # Solo el id es readonly, lo asigna Django automáticamente
    
    def create(self, validated_data):
        # create_user hashea la contraseña automáticamente
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
    
    def get_fields(self):
        fields = super().get_fields() # Trae todos los campos normalmente
        # Revisamos el contexto: ¿desde dónde me están llamando?
        request =self.context.get('request')
        # Si la URL termina con un ID o lookup, estamos en "detalle"
        view = self.context.get('view') 
        if view and view.action == 'retrieve':  # 'retrieve' = vista de detalle
            fields.pop('url', None) # Elimina el campo 'url', si existe
        return fields  


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','description','color']
        read_only_fields = ['id'] # Solo el id es readonly, lo asigna Django automáticamente