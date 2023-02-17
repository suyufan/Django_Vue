from app01.models import Image,Login_Info
from rest_framework import serializers

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id','image']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login_Info
        fields = ['id', 'user', 'password', 'login_time','logout_time']