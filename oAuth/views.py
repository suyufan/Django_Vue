from rest_framework import viewsets
from rest_framework.response import Response
from oAuth.models import NewUser, Books
from rest_framework import status
from django.db.models import Q
from oAuth.serializers import BookSerializer, UserSerializer
from django_vue.settings import BASE_URL
from django.core.mail import send_mail
# Create your views here.

class UserInfoViewSet(viewsets.ViewSet):
    queryset = NewUser.objects.all().order_by('-date_joined')
    http_method_names = ['get'] # 仅允许的请求方法

    def list(self, request, *args, **kwargs):
        print('OK')
        user_info = NewUser.objects.filter(id=request.user.id).values()[0]
        role = request.user.roles
        if role == 0:
            user_info['roles'] = ['admin']
        else:
            user_info['roles'] = ['user']

        return Response(user_info)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BookSerializer

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(~Q(is_delete=True)) # 重写queryset方法 排除admin类型 其他用户信息查询
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    def perform_destroy(self, instance):
        # 改写后 数据并没有被真的删除 只是is_delete标识为1 进行标记
        instance.is_delete = True
        print('OK')
        instance.save()
        # instance.delete()


class UserViewSet(viewsets.ModelViewSet):
    queryset = NewUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [] # 身份验证
    # list: get   create: post  put: update对应perform_update(整体更新,提供所有更改后的字段信息)  patch: update对应partial_update(局部更新,仅提供需要修改的信息)
    def list(self, request, *args, **kwargs):
        user = request.user
        if user.is_staff == False:
            self.queryset = self.queryset.filter(~Q(username='admin')) # 重写queryset方法 排除admin类型 其他用户信息查询
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_info = self.perform_create(serializer)
        user_info.set_password(request.data['password'])
        user_info.is_active = False
        user_info.save()
        code = user_info.code
        url = BASE_URL + '/#/user_activate?code=' + str(code)
        print(url)
        send_mail(
            '用户激活',
            url,
            '1484114039@qq.com',
            [user_info.email],
            fail_silently=False
        )
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, requset, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=requset.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class UserUUIDViewSet(viewsets.ModelViewSet):
    queryset = NewUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def retrieve(self, request, *args, **kwargs):
        # 默认是查询 id 的用户信息，比如/api/users/1
        # instance = self.get_object()
        # serializer = self.get_serializer(instance)
        # return Response(serializer.data)
        #-------------------------
        # 重写为访问带UUID的URL 激活用户状态
        instance = NewUser.objects.get(code=kwargs['pk'])
        instance.is_active = True
        instance.save()
        data = {
            'status': "success"
        }
        return Response(data, status=status.HTTP_200_OK)