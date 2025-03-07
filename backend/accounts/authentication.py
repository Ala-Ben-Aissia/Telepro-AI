from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone
from datetime import timezone as tz
from rest_framework.exceptions import AuthenticationFailed


class CustomJWTAuthentication(JWTAuthentication):
    # Overriding get_user to validate the token against the user's password change timestamp.
    # The JWT token includes a custom claim "pwd_changed" that stores the timestamp (in seconds) when the token was issued (which reflects the user's last_password_change time at login).
    # If the user changes their password after the token was issued, the user's last_password_change will be more recent than the token's pwd_changed value. In that case, we raise an AuthenticationFailed exception to invalidate the token.
    def get_user(self, validated_token):
        user = super().get_user(validated_token)
        pwd_changed_claim = validated_token.get("pwd_changed")
        if pwd_changed_claim:
            # Convert the claim to a datetime object (assuming the claim is a timestamp)
            token_issue_time = timezone.datetime.fromtimestamp(
                pwd_changed_claim, tz=tz.utc
            )
            # If the password was changed after the issuance of the token, invalidate the token.
            if user.last_password_change > token_issue_time:
                raise AuthenticationFailed(
                    "Token is no longer valid. Please log in again."
                )
        return user
