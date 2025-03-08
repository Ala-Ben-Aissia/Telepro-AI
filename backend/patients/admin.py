from django.contrib import admin

from .models import Patient


class PatientAdmin(admin.ModelAdmin):
    def trucated_id(self, obj):
        return str(obj.id)[:8]

    list_display = ("trucated_id", "user", "is_active", "has_active_consent")
    list_filter = ("is_active", "has_active_consent", "gender", "age_group")
    search_fields = ("medical_record_number", "postal_code")
    readonly_fields = ("trucated_id", "created_at", "updated_at")
    fieldsets = (
        (
            "Basic Information",
            {"fields": ("user", "medical_record_number", "is_active", "anonymized")},
        ),
        (
            "Demographics",
            {
                "fields": (
                    "date_of_birth",
                    "gender",
                    "age_group",
                    "location",
                    "postal_code",
                    "language_preference",
                )
            },
        ),
        (
            "Contact Information",
            {
                "fields": (
                    "email_verified",
                    "phone_verified",
                    "preferred_contact_method",
                    "contact_time_preferences",
                )
            },
        ),
        ("Consent", {"fields": ("has_active_consent",)}),
        (
            "System",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                    "created_by",
                    "scheduled_deletion_date",
                )
            },
        ),
    )


admin.site.register(Patient, PatientAdmin)
