from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .permissions import IsNotAuthenticated
from .serializers import (
    CustomTokenObtainPairSerializer,
    PasswordChangeSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
)

User = get_user_model()


class PatientRegistrationView(APIView):
    """Register a new patient user"""

    permission_classes = [IsNotAuthenticated]
    # need a more explicit response messages for the frontend since permissions would return {detail: "You do not have permission to perform this action."} which is not very user-friendly.

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Create the user with patient type
            user = serializer.save(user_type="PATIENT")

            # Generate JWT tokens for immediate login
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "message": "Registration successful",
                    "user_id": user.id,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token view that uses our enhanced token serializer"""

    permission_classes = [IsNotAuthenticated]
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        # Get client IP
        client_ip = request.META.get("REMOTE_ADDR", None)
        # Attempt to authenticate
        response = super().post(request, *args, **kwargs)

        # If successful login, update tracking fields
        if response.status_code == 200 and hasattr(self, "user"):
            self.user.failed_login_attempts = 0
            self.user.last_login_ip = client_ip
            self.user.save(update_fields=["failed_login_attempts", "last_login_ip"])
        # Log failed attempts
        elif response.status_code >= 400:
            username = request.data.get("username", "")
            if username:
                try:
                    user = User.objects.get(username=username)
                    user.failed_login_attempts += 1
                    user.last_login_ip = client_ip

                    # Force password reset after multiple failed attempts
                    if user.failed_login_attempts >= 5:
                        user.require_password_change = True

                    user.save(
                        update_fields=[
                            "failed_login_attempts",
                            "last_login_ip",
                            "require_password_change",
                        ]
                    )
                except User.DoesNotExist:
                    pass  # Don't reveal user existence

        return response


class UserProfileView(generics.RetrieveUpdateAPIView):
    """View for retrieving and updating the user's own profile"""

    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class PasswordChangeView(APIView):
    """View for changing the authenticated user's password"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")
        # Validate the input data
        serializer = PasswordChangeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Verify current password
        if not user.check_password(current_password):
            return Response(
                {"detail": "Current password is incorrect."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if current_password == new_password:
            return Response(
                {"detail": "New password must be different from the current password."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate and set new password
        try:
            validate_password(new_password, user)
            user.set_password(new_password)
            user.save()

            # logout the user by blacklisting the refresh token
            logout(request)

            return Response(
                {"detail": "Password changed successfully. Please login again."},
                status=status.HTTP_200_OK,
            )
        except DjangoValidationError as e:
            return Response({"detail": list(e)}, status=status.HTTP_400_BAD_REQUEST)


def logout(request):
    """Logout the user by blacklisting the refresh token"""
    refresh_token = request.data.get("refresh")
    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            pass
