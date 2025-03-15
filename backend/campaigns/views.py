from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from patients.models import Patient
from services.ai.prediction import CampaignPredictionService
from services.analytics import AnalyticsService

from .models import Campaign, CampaignCategory, CommunicationLog, PatientSegment
from .serializers import (
    CampaignCategorySerializer,
    CampaignSerializer,
    CommunicationLogSerializer,
    PatientSegmentSerializer,
)


class CampaignCategoryViewSet(viewsets.ModelViewSet):
    queryset = CampaignCategory.objects.all()
    serializer_class = CampaignCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["post"])
    def send(self, request, pk=None):
        # Logic to send campaign communications
        # This would use the CommunicationService
        # to send emails or SMS based on patient preferences
        campaign = self.get_object()
        # Implementation details here...
        return Response({"status": "Campaign sending initiated"})

    def perform_create(self, serializer):
        """Track who created this campaign"""
        campaign = serializer.save()
        campaign._current_user_id = self.request.user.id
        campaign.save()

    def perform_update(self, serializer):
        """Track who updated this campaign"""
        campaign = serializer.save()
        campaign._current_user_id = self.request.user.id
        campaign.save()

    @action(detail=True, methods=["get"])
    def effectiveness(self, request, pk=None):
        campaign = self.get_object()
        effectiveness = AnalyticsService.calculate_campaign_effectiveness(campaign.id)
        return Response(effectiveness)

    @action(detail=True, methods=["get"])
    def predict_effectiveness(self, request, pk=None):
        """Predict the effectiveness of this campaign"""
        campaign = self.get_object()
        prediction = CampaignPredictionService.predict_campaign_effectiveness(campaign.id)
        return Response(prediction)

    @action(detail=True, methods=["post"])
    def predict_patient_response(self, request, pk=None):
        """Predict if a specific patient will respond to this campaign"""
        campaign = self.get_object()

        # Validate patient_id
        patient_id = request.data.get("patient_id")
        if not patient_id:
            return Response(
                {"error": "patient_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            prediction = CampaignPredictionService.predict_patient_response(
                patient_id=patient_id, campaign_id=campaign.id
            )
            return Response(prediction)
        except Patient.DoesNotExist:
            return Response(
                {"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND
            )


class PatientSegmentViewSet(viewsets.ModelViewSet):
    queryset = PatientSegment.objects.all()
    serializer_class = PatientSegmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["get"])
    def patients(self, request, pk=None):
        segment = self.get_object()
        # Logic to retrieve patients in this segment
        # You'll need to implement the criteria matching logic
        # Implementation details here...
        return Response({"count": 0, "patients": []})


class CommunicationLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CommunicationLog.objects.all()
    serializer_class = CommunicationLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = CommunicationLog.objects.all()
        campaign_id = self.request.query_params.get("campaign", None)
        patient_id = self.request.query_params.get("patient", None)

        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)

        return queryset
