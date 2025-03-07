from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone
from datetime import timezone as tz
from rest_framework.exceptions import AuthenticationFailed


class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication class that ensures token validity based on password changes.

    This class overrides the get_user method to:
    1. Extract the `pwd_changed` claim from the JWT token, which stores the timestamp of the user's last password change at login.
    2. Compare this timestamp with the user's current `last_password_change` field.
    3. Invalidate the token if the user has changed their password after the token was issued, ensuring security.

    This prevents unauthorized access with outdated tokens after password changes.
    """

    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        pwd_changed_claim = validated_token.get("pwd_changed")
        if pwd_changed_claim:
            # Convert the `pwd_changed` claim (timestamp in seconds) to a datetime object
            token_issue_time = timezone.datetime.fromtimestamp(
                pwd_changed_claim, tz=tz.utc
            )
            # user's password was changed after the token was issued
            if user.last_password_change > token_issue_time:
                raise AuthenticationFailed(
                    "Token is no longer valid. Please log in again."
                )
        return user
