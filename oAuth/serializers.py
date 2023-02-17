from oAuth.models import NewUser, Books
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ['url', 'username', 'email', 'is_staff','is_active','roles']

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ['id', 'name', 'auther', 'is_delete']