from django.db import models
from django.utils.translation import gettext_lazy as _

from common.utils import AuditableMixin


class CampaignCategory(models.Model):
    """Categories for different types of campaigns (e.g. vaccination, dental, etc)"""

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Campaign Category")
        verbose_name_plural = _("Campaign Categories")

    def __str__(self):
        return self.name


class Campaign(AuditableMixin, models.Model):
    """Represents a communication campaign"""

    title = models.CharField(max_length=200)
    category = models.ForeignKey(
        CampaignCategory,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Targeting criteria
    target_age_groups = models.JSONField(default=list)  # List of age groups
    target_locations = models.JSONField(default=list)  # List of locations
    target_languages = models.JSONField(default=list)  # List of language codes

    # Message templates
    email_template = models.TextField(blank=True)
    sms_template = models.TextField(blank=True)

    class Meta:
        verbose_name = _("Campaign")
        verbose_name_plural = _("Campaigns")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Track who updated this campaign
        if hasattr(self, "_current_user_id") and self._current_user_id:
            if self.pk is None:  # Creating
                self.created_by_id = self._current_user_id
            self.updated_by_id = self._current_user_id
        super().save(*args, **kwargs)


class PatientSegment(models.Model):
    """Groups of patients with similar characteristics for targeting"""

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    criteria = models.JSONField(help_text="Segmentation criteria in JSON format")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Optional link to campaigns
    campaigns = models.ManyToManyField(Campaign, blank=True, related_name="segments")

    class Meta:
        verbose_name = _("Patient Segment")
        verbose_name_plural = _("Patient Segments")


class CommunicationLog(models.Model):
    """Track all communications with patients"""

    COMMUNICATION_STATUS = (
        ("PENDING", "Pending"),
        ("SENT", "Sent"),
        ("FAILED", "Failed"),
        ("DELIVERED", "Delivered"),
        ("READ", "Read"),
        ("RESPONDED", "Responded"),
    )

    # Import choices from Patient model to maintain consistency
    COMMUNICATION_TYPES = [
        ("EMAIL", "Email"),
        ("SMS", "SMS"),
        ("CALL", "Phone Call"),
        ("NONE", "No Communication"),
    ]

    campaign = models.ForeignKey(Campaign, on_delete=models.PROTECT)
    patient = models.ForeignKey("patients.Patient", on_delete=models.PROTECT)
    communication_type = models.CharField(
        max_length=10,
        choices=COMMUNICATION_TYPES,
        help_text="Type of communication channel used",
    )
    status = models.CharField(
        max_length=20, choices=COMMUNICATION_STATUS, default="PENDING"
    )
    sent_at = models.DateTimeField(null=True)
    delivered_at = models.DateTimeField(null=True)
    read_at = models.DateTimeField(null=True)
    response = models.TextField(blank=True)
    responded_at = models.DateTimeField(null=True)

    # Additional useful fields
    error_message = models.TextField(
        blank=True, help_text="Error details if communication failed"
    )
    metadata = models.JSONField(
        default=dict, help_text="Additional metadata about the communication"
    )

    class Meta:
        verbose_name = _("Communication Log")
        verbose_name_plural = _("Communication Logs")
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["sent_at"]),
            models.Index(fields=["campaign", "patient"]),
        ]
        ordering = ["-sent_at"]

    def __str__(self):
        return f"{self.communication_type} to {self.patient} for {self.campaign}"

    def mark_as_sent(self):
        """Mark the communication as sent"""
        from django.utils import timezone

        self.sent_at = timezone.now()
        self.status = "SENT"
        self.save(update_fields=["sent_at", "status"])

    def mark_as_delivered(self):
        """Mark the communication as delivered"""
        from django.utils import timezone

        self.delivered_at = timezone.now()
        self.status = "DELIVERED"
        self.save(update_fields=["delivered_at", "status"])

    def mark_as_read(self):
        """Mark the communication as read"""
        from django.utils import timezone

        self.read_at = timezone.now()
        self.status = "READ"
        self.save(update_fields=["read_at", "status"])

    def record_response(self, response_text):
        """Record a response from the patient"""
        from django.utils import timezone

        self.response = response_text
        self.responded_at = timezone.now()
        self.status = "RESPONDED"
        self.save(update_fields=["response", "responded_at", "status"])

        # Update patient's last campaign response
        self.patient.last_campaign_response = timezone.now()
        self.patient.save(update_fields=["last_campaign_response"])

    def record_failure(self, error_message):
        """Record a failed communication attempt"""
        self.status = "FAILED"
        self.error_message = error_message
        self.save(update_fields=["status", "error_message"])
