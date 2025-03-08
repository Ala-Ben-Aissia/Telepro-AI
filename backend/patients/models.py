import secrets
import uuid
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Patient(models.Model):
    """
    Core Patient model with integrated communication capabilities.

    This model stores essential patient information with a focus on:
    1. Secure storage of personally identifiable information (PII)
    2. Communication channel management
    3. Consent tracking and verification
    4. Data lifecycle management for GDPR compliance
    """

    # Primary identifiers
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the patient",
    )

    # Link to authentication
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_profile",
        help_text="User account for this patient",
    )

    # Encrypted identifying information
    medical_record_number = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        unique=True,
        help_text="Medical record number or other external identifier",
    )

    # Demographic information
    date_of_birth = models.CharField(
        max_length=10, null=True, blank=True, help_text="Patient's date of birth"
    )
    # Demographic information for segmentation
    gender = models.CharField(
        max_length=10,
        choices=[
            ("M", "Male"),
            ("F", "Female"),
            ("O", "Other"),
            ("N", "Prefer not to say"),
        ],
        null=True,
        blank=True,
        help_text="Patient's gender for demographic segmentation",
    )
    location = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="General location for geographic targeting",
    )
    postal_code = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="Postal code for geographic segmentation",
    )
    age_group = models.CharField(
        max_length=10,
        choices=[
            ("0-18", "0-18"),
            ("19-35", "19-35"),
            ("36-50", "36-50"),
            ("51-65", "51-65"),
            ("65+", "65+"),
        ],
        null=True,
        blank=True,
        help_text="Age group for demographic segmentation",
    )
    language_preference = models.CharField(
        max_length=10,
        choices=(
            ("ar", "Arabic"),
            ("fr", "French"),
            ("en", "English"),
            ("es", "Spanish"),
            ("de", "German"),
            ("it", "Italian"),
        ),
        default="fr",
        null=True,
        blank=True,
        help_text="Preferred language for communications",
    )

    # Communication channels (essential for outreach)
    email = models.EmailField(
        unique=True,
        max_length=50,
        help_text="Primary email for communications",
    )

    email_verified = models.BooleanField(
        default=False, help_text="Whether the email has been verified"
    )

    phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="Primary phone number for communications",
    )

    phone_verified = models.BooleanField(
        default=False, help_text="Whether the phone number has been verified"
    )

    # Communication preferences (for outreach campaigns)
    COMMUNICATION_PREFERENCES = [
        ("EMAIL", "Email"),
        ("SMS", "SMS"),
        ("CALL", "Phone Call"),
        ("NONE", "No Communication"),
    ]
    preferred_contact_method = models.CharField(
        max_length=10,
        choices=COMMUNICATION_PREFERENCES,
        default="NONE",
        help_text="Patient's preferred method of contact",
    )

    # Contact time preferences
    contact_time_preferences = models.JSONField(
        default=dict, help_text="JSON containing preferred contact times"
    )

    # Audit and lifecycle fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_patients",
    )

    # Data retention and GDPR compliance
    is_active = models.BooleanField(
        default=True, help_text="Whether this patient record is active"
    )
    scheduled_deletion_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date when this record should be automatically deleted",
    )
    anonymized = models.BooleanField(
        default=False, help_text="Whether this record has been anonymized"
    )

    # Consent tracking field
    has_active_consent = models.BooleanField(
        default=False,
        help_text="Whether this patient has provided active consent for data processing",
    )

    # Verification and security
    verification_token = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        help_text="Token used for email/phone verification or password reset",
    )
    token_expiry = models.DateTimeField(
        null=True, blank=True, help_text="Expiration time for the verification token"
    )

    # Outreach tracking
    last_contacted_at = models.DateTimeField(
        null=True, blank=True, help_text="When the patient was last contacted"
    )
    contact_attempts = models.PositiveIntegerField(
        default=0, help_text="Number of contact attempts made"
    )
    successful_contacts = models.PositiveIntegerField(
        default=0, help_text="Number of successful contacts"
    )

    class Meta:
        verbose_name = _("Patient")
        verbose_name_plural = _("Patients")
        indexes = [
            models.Index(fields=["is_active"]),
            models.Index(fields=["has_active_consent"]),
            models.Index(fields=["email_verified"]),
            models.Index(fields=["phone_verified"]),
            models.Index(fields=["last_contacted_at"]),
        ]
        permissions = [
            ("view_sensitive_data", _("Can view sensitive patient data")),
            ("export_patient_data", _("Can export patient data")),
            ("anonymize_patient", _("Can anonymize patient data")),
            ("contact_patient", _("Can contact patient directly")),
        ]

    def __str__(self):
        return f"Patient {self.id}"

    # Communication and verification methods
    def generate_verification_token(self, expiry_hours=48):
        """Generate a new verification token with specified expiry time"""
        self.verification_token = secrets.token_urlsafe(42)
        self.token_expiry = timezone.now() + timedelta(hours=expiry_hours)
        self.save(update_fields=["verification_token", "token_expiry"])
        return self.verification_token

    def verify_token(self, token):
        """Verify a token against the stored verification token"""
        if not self.verification_token or not self.token_expiry:
            return False

        if self.token_expiry < timezone.now():
            return False

        return secrets.compare_digest(str(self.verification_token), token)

    def verify_email(self):
        """Mark the email as verified"""
        self.email_verified = True
        self.verification_token = None
        self.token_expiry = None
        self.save(
            update_fields=[
                "email_verified",
                "verification_token",
                "token_expiry",
                "updated_at",
            ]
        )

    def verify_phone(self):
        """Mark the phone as verified"""
        self.phone_verified = True
        self.verification_token = None
        self.token_expiry = None
        self.save(
            update_fields=[
                "phone_verified",
                "verification_token",
                "token_expiry",
                "updated_at",
            ]
        )

    # Contact and outreach methods
    def can_contact(self):
        """Check if the patient can be contacted based on preferences and verification"""
        if self.preferred_contact_method == "NONE" or not self.has_active_consent:
            return False

        if self.preferred_contact_method == "EMAIL" and not self.email_verified:
            return False

        if self.preferred_contact_method in ["SMS", "CALL"] and not self.phone_verified:
            return False

        return True

    def get_contact_info(self):
        """Get the appropriate contact information based on preferences"""
        if self.preferred_contact_method == "EMAIL":
            return {
                "method": "EMAIL",
                "value": self.email,
                "verified": self.email_verified,
            }
        elif self.preferred_contact_method in ["SMS", "CALL"]:
            return {
                "method": self.preferred_contact_method,
                "value": self.phone_number,
                "verified": self.phone_verified,
            }
        return {"method": "NONE", "value": None, "verified": False}

    def record_contact_attempt(self, successful=False):
        """Record a contact attempt and update counters"""
        self.contact_attempts += 1
        self.last_contacted_at = timezone.now()

        if successful:
            self.successful_contacts += 1

        self.save(
            update_fields=[
                "contact_attempts",
                "successful_contacts",
                "last_contacted_at",
                "updated_at",
            ]
        )

    # Data management methods
    def anonymize(self):
        """
        Anonymize this patient record by removing all identifiable information
        while maintaining the record for statistical purposes.
        """
        # Generate anonymous identifiers
        anonymous_id = f"ANON-{uuid.uuid4()}"

        # Clear identifiable fields
        self.medical_record_number = anonymous_id
        self.email = f"{anonymous_id}@anonymized.example"
        self.phone_number = None
        self.date_of_birth = None

        # Update status flags
        self.anonymized = True
        self.has_active_consent = False
        self.email_verified = False
        self.phone_verified = False

        # Save changes
        fields_to_update = [
            "medical_record_number",
            "email",
            "phone_number",
            "date_of_birth",
            "anonymized",
            "has_active_consent",
            "email_verified",
            "phone_verified",
            "updated_at",
        ]
        self.save(update_fields=fields_to_update)

        # Return true to confirm anonymization
        return True

    def schedule_deletion(self, days=30):
        """Schedule this patient record for deletion after specified days"""
        self.scheduled_deletion_date = timezone.now().date() + timedelta(days=days)
        self.save(update_fields=["scheduled_deletion_date", "updated_at"])
        return self.scheduled_deletion_date

    def is_due_for_deletion(self):
        """Check if this patient record is due for deletion"""
        if not self.scheduled_deletion_date:
            return False
        return self.scheduled_deletion_date <= timezone.now().date()

    def update_age_group(self):
        """Calculate and update age group based on date of birth"""
        if not self.date_of_birth:
            return None

        try:
            # Parse the date string (assuming format is YYYY-MM-DD)
            dob = timezone.datetime.strptime(self.date_of_birth, "%Y-%m-%d").date()
            today = timezone.now().date()
            age = (
                today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            )

            # Determine age group
            if age <= 18:
                self.age_group = "0-18"
            elif age <= 35:
                self.age_group = "19-35"
            elif age <= 50:
                self.age_group = "36-50"
            elif age <= 65:
                self.age_group = "51-65"
            else:
                self.age_group = "65+"

            self.save(update_fields=["age_group"])
            return self.age_group
        except (ValueError, TypeError):
            # Handle invalid date format
            return None
