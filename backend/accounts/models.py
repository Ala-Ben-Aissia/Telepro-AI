from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Custom user manager for proper password handling."""

    def create_user(self, username, email, password=None, **extra_fields):
        """Create and save a regular user with the given username, email, and password."""
        if not username:
            raise ValueError("Users must have a username")
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # This handles password hashing correctly
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """Create and save a superuser with the given username, email, and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("user_type", "STAFF")

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    """Extended user model for the system"""

    USER_TYPE_CHOICES = (
        ("STAFF", "Staff"),
        ("PATIENT", "Patient"),
    )

    user_type = models.CharField(
        max_length=10, choices=USER_TYPE_CHOICES, default="PATIENT"
    )
    email_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    phone_verified = models.BooleanField(default=False)

    # Additional security fields
    failed_login_attempts = models.PositiveIntegerField(default=0)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    require_password_change = models.BooleanField(default=False)
    last_password_change = models.DateTimeField(default=timezone.now)

    # Fix for the clash in reverse relations
    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="custom_user_set",  # This fixes the clash
        related_query_name="user",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="custom_user_set",  # This fixes the clash
        related_query_name="user",
    )

    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def is_patient(self):
        return self.user_type == "PATIENT"

    def is_staff_user(self):
        return self.user_type == "STAFF"

    def set_password(self, raw_password):
        self.last_password_change = timezone.now()
        return super().set_password(raw_password)
