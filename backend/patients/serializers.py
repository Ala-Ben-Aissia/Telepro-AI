from rest_framework import serializers

from .models import ConsentRecord, Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "id",
            "medical_record_number",
            "date_of_birth",
            "gender",
            "location",
            "postal_code",
            "age_group",
            "language_preference",
            "email_verified",
            "phone_verified",
            "phone_number",
            "preferred_contact_method",
            "has_active_consent",
            "engagement_score",
        ]
        read_only_fields = ["id", "engagement_score"]


class PatientPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "preferred_contact_method",
            "contact_time_preferences",
            "campaign_preferences",
            "language_preference",
        ]


class PatientConsentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["has_active_consent"]


class PatientConsentRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsentRecord
        fields = [
            "consent_type",
            "granted",
            "metadata",
            "consent_method",
            "pk",
            "timestamp",
        ]
        extra_kwargs = {"metadata": {"required": False}}
