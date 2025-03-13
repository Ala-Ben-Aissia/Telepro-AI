from cryptography import fernet
from django.db import models

from config.settings import AUTH_USER_MODEL, FIELD_ENCRYPTION_KEY


def encrypt(cleartext: str) -> str:
    if not cleartext:
        return ""
    f = fernet.Fernet(FIELD_ENCRYPTION_KEY)
    return f.encrypt(cleartext.encode()).decode()


def decrypt(ciphertext: str) -> str:
    if not ciphertext:
        return ""
    f = fernet.Fernet(FIELD_ENCRYPTION_KEY)
    return f.decrypt(ciphertext.encode()).decode()


class AuditableMixin(models.Model):
    """
    An abstract base model that provides auditing fields.
    Add this to any model that contains sensitive operations.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created",
    )
    updated_by = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
    )

    class Meta:
        abstract = True
