# social/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('link/facebook/', views.link_facebook, name='link_facebook'),
   # path('link/instagram/', views.link_instagram, name='link_instagram'),
    # Add other social platforms here
]
