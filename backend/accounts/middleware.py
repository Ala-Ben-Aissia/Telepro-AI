import json
import logging

from django.utils import timezone

security_logger = logging.getLogger("security")


class SecurityLoggingMiddleware:
    """
    Middleware for logging security-related events.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process request
        response = self.get_response(request)

        # Log sensitive operations
        if self._is_sensitive_operation(request):
            self._log_operation(request, response)

        return response

    def _is_sensitive_operation(self, request):
        """Check if this is a sensitive operation that should be logged."""
        sensitive_paths = [
            "/api/accounts/token/",
            "/api/accounts/token/refresh/",
            "/api/accounts/change-password/",
            "/api/patients/consent/",
            "/admin/login/",
            "/api/accounts/register/",
        ]

        # Is this a sensitive endpoint?
        path_match = any(request.path.startswith(path) for path in sensitive_paths)

        # Is this a sensitive method?
        method_match = request.method in ["POST", "PUT", "DELETE", "PATCH"]

        return path_match and method_match

    def _log_operation(self, request, response):
        """Log the sensitive operation."""
        log_data = {
            "timestamp": timezone.now().isoformat(),
            "path": request.path,
            "method": request.method,
            "user_id": request.user.id if request.user.is_authenticated else None,
            "ip_address": self._get_client_ip(request),
            "status_code": response.status_code,
            "user_agent": request.META.get("HTTP_USER_AGENT", ""),
        }

        # Don't log passwords or sensitive data
        if hasattr(request, "data"):
            sanitized_data = self._sanitize_data(request.data)
            log_data["request_data"] = sanitized_data

        security_logger.info(json.dumps(log_data))

    def _get_client_ip(self, request):
        """Get the client IP, accounting for proxies."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def _sanitize_data(self, data):
        """Remove sensitive fields from data before logging."""
        if not data:
            return {}

        sensitive_fields = [
            "password",
            "password1",
            "password2",
            "current_password",
            "new_password",
            "token",
            "refresh",
            "access",
        ]

        sanitized = {}
        for key, value in data.items():
            if key.lower() in sensitive_fields:
                sanitized[key] = "[REDACTED]"
            else:
                sanitized[key] = value

        return sanitized
