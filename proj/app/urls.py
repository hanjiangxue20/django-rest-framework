from django.urls import path, include
from rest_framework import routers

from app import views

router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet, basename='users')
router.register(r'users', views.UserViewSet)
router.register(r'group', views.GroupViewSet)
router.register(r'snippet', views.SnippetViewSet)
# router.register(r'snippet/mixins', views.SnippetListMixinsView)

urlpatterns = [
    path('', include(router.urls)),
    # path('snippet_v2', views.snippet_list), # 函数视图
    path('snippet_v2', views.SnippetList.as_view()),  # 类视图
    path('snippet_v2/<int:pk>/', views.SnippetDetail.as_view()),
    path('snippet_v3', views.SnippetList_v3.as_view()),
    path('demo', views.demo),
]
