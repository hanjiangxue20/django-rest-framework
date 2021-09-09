from django.shortcuts import render
from django.shortcuts import HttpResponse

from app.models import Snippet
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action

from django_filters.rest_framework import DjangoFilterBackend

from django.contrib.auth.models import User, Group
from app.serializers import UserSerializer, GroupSerializer, SnippetSerializer_Serializer, \
    SnippetSerializer_ModelSerializer

# Create your views here.
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(['GET'], detail=False, url_path='demo2')
    def demo(self, request, *args, **kwargs):  # 默认URL为函数名称： /app/users/demo/
        print(request.data)
        return Response(data='ok UserViewSet')


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]  # 权限
    filter_backends = (DjangoFilterBackend, OrderingFilter)  # 排序和搜索


class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    # serializer_class = SnippetSerializer_Serializer
    serializer_class = SnippetSerializer_ModelSerializer


def demo(request):
    print('ok')
    return HttpResponse('ok')


from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from app.models import Snippet
from app.serializers import SnippetSerializer_ModelSerializer


# 基于函数的视图
@csrf_exempt
def snippet_list(request):
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer_ModelSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer_ModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


# 基于类的视图 APIView
class SnippetList(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer_ModelSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer_ModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise status.Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer_ModelSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer_ModelSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 使用混合类mixins
from rest_framework import mixins, generics


# class SnippetListMixinsView(mixins.ListModelMixin,
#                             mixins.CreateModelMixin,
#                             generics.GenericAPIView):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetSerializer_ModelSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# generics
class SnippetList_v3(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer_ModelSerializer


class SnippetDetail_v3(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer_ModelSerializer
