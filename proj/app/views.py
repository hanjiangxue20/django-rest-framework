from django.shortcuts import render
from django.shortcuts import HttpResponse
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from django.contrib.auth.models import User, Group
from app.serializers import UserSerializer, GroupSerializer

# Create your views here.
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend, OrderingFilter)  # 排序和搜索


def demo(request):
    print('ok')
    return HttpResponse('ok')
