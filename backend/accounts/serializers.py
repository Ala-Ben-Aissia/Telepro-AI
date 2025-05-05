from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from common.utils import encrypt

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile viewing and updating
    """

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone_number",
            "email_verified",
            "phone_verified",
            "user_type",
            "date_joined",
            "last_login",
        ]
        read_only_fields = [
            "id",
            "email_verified",
            "phone_verified",
            "user_type",
            "date_joined",
            "last_login",
        ]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token serializer that includes additional user information
    """

    @classmethod
    # called on each request made using the access token
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims of the user's last password change timestamp
        token["pwd_changed"] = user.last_password_change.timestamp()
        return token

    def validate(self, attrs):
        # Get the token data from the parent
        data = super().validate(attrs)

        # Add extra response data
        data["user_id"] = self.user.id
        data["username"] = self.user.username
        data["email"] = self.user.email
        data["user_type"] = self.user.user_type

        # Add patient UUID if the user is a patient
        if self.user.user_type == "PATIENT" and hasattr(self.user, "patient_profile"):
            try:
                data["patient_uuid"] = str(self.user.patient_profile.id)
            except Exception as e:
                # If there's an error getting the patient profile, log it but don't fail
                print(f"Error getting patient UUID: {e}")
                data["patient_uuid"] = None
        else:
            data["patient_uuid"] = None

        # Update login stats
        # self.user.failed_login_attempts = 0

        # You could add the IP here if you extend the view later
        # self.user.last_login_ip = self.context['request'].META.get('REMOTE_ADDR')

        # self.user.save(update_fields=["failed_login_attempts"])
        self.user.save()

        return data


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """

    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True, write_only=True, style={"input_type": "password"}
    )

    def validate(self, attrs):
        return attrs


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration with password validation.
    """

    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    password_confirm = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "password_confirm",
        ]
        extra_kwargs = {
            "email": {"required": True},
            "phone_number": {"required": False},
        }

    def validate_email(self, value):
        """
        Ensure email is unique
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        """
        Ensure username is unique
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def validate_password(self, value):
        """
        Validate password complexity using Django's password validators
        """
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e))
        return value

    def validate(self, attrs):
        """
        Check that the two password fields match
        """
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "Passwords do not match."}
            )
        return attrs

    def create(self, validated_data):
        """
        Create and return a new user with encrypted password and user_type
        """
        # Remove password_confirm as we don't need it for creating the user
        validated_data.pop("password_confirm")

        # Extract the password to use set_password() which handles hashing
        password = validated_data.pop("password")

        # Get the user_type from context or default to PATIENT
        user_type = validated_data.get("user_type", "PATIENT")

        phone_number = validated_data.get("phone_number", "")
        if phone_number != "":
            phone_number = encrypt(phone_number)

        # Create the user instance with extra fields
        user = User.objects.create(
            username=validated_data["username"],
            email=encrypt(validated_data["email"]),
            phone_number=phone_number,
            user_type=user_type,
        )

        # Set the password properly using Django's helper method
        user.set_password(password)
        user.save()

        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset
    """

    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email address.")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming a password reset
    """

    token = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    password_confirm = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e))
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "Passwords do not match."}
            )
        return attrs


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for changing a user's password
    """

    current_password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    new_password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    new_password_confirm = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    def validate_new_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e))
        return value

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError(
                {"new_password_confirm": "Passwords do not match."}
            )
        return attrs
