from rest_framework import viewsets
from rest_framework.response import Response
from app01.models import Image, Task_Info, Checked_Image, Login_Info
from rest_framework import status
from django.db.models import Q
from app01.serializers import ImageSerializer, UserSerializer
from django_vue.settings import BASE_URL
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from app01 import models
# Create your views here.

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def create(self, request, args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        image = self.perform_create(serializer)
        import base64  # 引入base64模块
        with open('./static/img', 'rb') as f:  # 以二进制的方式读取图片
            encode_str = base64.decode(f.read())  # 得到 byte 编码的数据
        image = encode_str
        print('image--------------',image)
        models.Image.objects.create(image=image)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserViewSet(viewsets.ModelViewSet):
    queryset = Login_Info.objects.all()
    serializer_class = UserSerializer
