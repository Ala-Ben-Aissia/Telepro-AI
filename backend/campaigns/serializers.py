from rest_framework import serializers

from .models import Campaign, CampaignCategory, CommunicationLog, PatientSegment


class CampaignCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignCategory
        fields = ["id", "name", "description", "is_active"]


class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = [
            "id",
            "title",
            "category",
            "description",
            "start_date",
            "end_date",
            "is_active",
            "target_age_groups",
            "target_locations",
            "target_languages",
            "email_template",
            "sms_template",
        ]


class PatientSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientSegment
        fields = [
            "id",
            "name",
            "description",
            "criteria",
            "is_active",
            "created_at",
            "updated_at",
        ]


class CommunicationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationLog
        fields = [
            "id",
            "campaign",
            "patient",
            "communication_type",
            "status",
            "sent_at",
            "delivered_at",
            "read_at",
            "response",
            "error_message",
            "metadata",
        ]
        read_only_fields = ["sent_at", "delivered_at", "read_at"]
