from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    def truncated_email(self, obj):
        return "..." + obj.email[12:20] + "..."

    truncated_email.short_description = "Email"

    list_display = ("username", "truncated_email", "user_type", "is_active")
    search_fields = ("username", "email")
    list_filter = ("user_type", "is_active")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important dates",
            {"fields": ("last_login", "date_joined", "last_password_change")},
        ),
        ("Custom fields", {"fields": ("user_type", "email_verified", "phone_number")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "email",
                    "user_type",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    ordering = ("username",)
    filter_horizontal = ("groups", "user_permissions")
