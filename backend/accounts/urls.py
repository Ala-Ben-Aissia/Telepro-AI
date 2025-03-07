from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CustomTokenObtainPairView,
    PasswordChangeView,
    PatientRegistrationView,
    UserProfileView,
)

urlpatterns = [
    # Authentication endpoints
    path("register/", PatientRegistrationView.as_view(), name="register"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # User profile endpoints
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path("change-password/", PasswordChangeView.as_view(), name="change_password"),
]
