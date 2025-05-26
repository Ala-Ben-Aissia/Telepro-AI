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
            "preferred_contact_methods",
            "has_active_consent",
            "engagement_score",
        ]
        read_only_fields = ["id", "engagement_score"]


class PatientPreferencesSerializer(serializers.ModelSerializer):
    preferred_contact_methods = serializers.ListField(
        child=serializers.ChoiceField(
            choices=[
                ("EMAIL", "Email"),
                ("SMS", "SMS"),
                ("CALL", "Phone Call"),
                ("NONE", "No Communication"),
            ]
        ),
        required=False,
        allow_empty=True,
    )

    contact_time_preferences = serializers.JSONField(required=False)
    campaign_preferences = serializers.PrimaryKeyRelatedField(
        many=True,
        required=False,
        queryset=Patient.campaign_preferences.rel.model.objects.all(),
    )
    language_preference = serializers.ChoiceField(
        choices=[
            ("ar", "Arabic"),
            ("fr", "French"),
            ("en", "English"),
            ("es", "Spanish"),
            ("de", "German"),
            ("it", "Italian"),
        ],
        required=False,
    )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["campaign_preferences"] = list(
            instance.campaign_preferences.values_list("id", flat=True)
        )
        return ret

    def update(self, instance, validated_data):
        if "preferred_contact_methods" in validated_data:
            instance.preferred_contact_methods = (
                validated_data["preferred_contact_methods"] or []
            )
        if "contact_time_preferences" in validated_data:
            instance.contact_time_preferences = (
                validated_data["contact_time_preferences"] or {}
            )
        if "campaign_preferences" in validated_data:
            instance.campaign_preferences.set(
                validated_data["campaign_preferences"] or []
            )
        if "language_preference" in validated_data:
            instance.language_preference = validated_data["language_preference"]
        instance.save()
        return instance

    class Meta:
        model = Patient
        fields = [
            "preferred_contact_methods",
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
