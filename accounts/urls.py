from django.urls import path
from .views import RegisterView, LoginView, LogoutView, UserProfileView, PasswordResetRequestView, PasswordResetConfirmView, CheckLoginStatusView, GoogleAuthView

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', UserProfileView.as_view(), name='profile'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),  # Update here
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('check-login-status/', CheckLoginStatusView.as_view(), name='check-login-status'),
      path('google/', GoogleAuthView.as_view(), name='google-auth'),
    
]

