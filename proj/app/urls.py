from django.urls import path, include
from rest_framework import routers

from app import views

router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet, basename='users')
router.register(r'users', views.UserViewSet)
router.register(r'group', views.GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('demo', views.demo),
]
