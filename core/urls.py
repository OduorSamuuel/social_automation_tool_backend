from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),  # Include accounts API
    path('accounts/', include('allauth.urls')),
     path('api/social/', include('social.urls')),
]
