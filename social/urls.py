# social/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SocialAccountViewSet

router = DefaultRouter()
router.register(r'accounts', SocialAccountViewSet, basename='socialaccount')

urlpatterns = [
    path('', include(router.urls)),
]
