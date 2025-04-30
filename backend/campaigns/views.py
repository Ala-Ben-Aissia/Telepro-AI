from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django.utils import timezone
from datetime import timedelta

from patients.models import Patient
from services.ai.prediction import CampaignPredictionService
from services.analytics import AnalyticsService
from services.optimization import CampaignOptimizationService

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
        """
        Send campaign communications to targeted patients.

        This endpoint initiates the sending of campaign communications to patients
        who match the campaign's targeting criteria and have active consent.
        """
        campaign = self.get_object()

        # Get target segment if provided
        segment_id = request.data.get("segment_id")

        if segment_id:
            try:
                segment = PatientSegment.objects.get(id=segment_id)
                from services.segmentation import SegmentationService

                patients = SegmentationService.get_patients_by_criteria(segment.criteria)
            except PatientSegment.DoesNotExist:
                return Response(
                    {"error": "Segment not found"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Use campaign's targeting criteria
            criteria = {
                "age_groups": campaign.target_age_groups,
                "locations": campaign.target_locations,
                "languages": campaign.target_languages,
                "has_active_consent": True,
            }
            from services.segmentation import SegmentationService

            patients = SegmentationService.get_patients_by_criteria(criteria)

        # Check if we have patients to target
        if not patients.exists():
            return Response(
                {
                    "error": "No patients match the targeting criteria or have active consent"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create communication logs for each patient
        from django.utils import timezone

        communication_logs = []
        for patient in patients:
            # Determine communication type based on patient preferences
            comm_type = patient.preferred_contact_method
            if comm_type == "NONE":
                continue  # Skip patients who don't want to be contacted

            # Create communication log
            log = CommunicationLog.objects.create(
                campaign=campaign,
                patient=patient,
                communication_type=comm_type,
                status="PENDING",
                metadata={"source": "campaign_send_api"},
            )
            communication_logs.append(log)

            # In a real implementation, you would queue these for actual sending
            # through an email service, SMS gateway, etc.

            # For now, just mark as sent for demonstration
            log.status = "SENT"
            log.sent_at = timezone.now()
            log.save()

            # Update patient's last_contacted_at
            patient.last_contacted_at = timezone.now()
            patient.contact_attempts += 1
            patient.save(update_fields=["last_contacted_at", "contact_attempts"])

        return Response(
            {
                "status": "Campaign sending initiated",
                "campaign_id": campaign.id,
                "communications_created": len(communication_logs),
                "target_patients": patients.count(),
            }
        )

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

    @action(detail=True, methods=["get"])
    def optimize(self, request, pk=None):
        """
        Get optimization suggestions for a campaign.

        This endpoint provides AI-driven suggestions for:
        - ML-based patient segmentation
        - Optimal sending times
        - Message content optimization
        """
        campaign = self.get_object()

        # Get optimization suggestions
        optimization = CampaignOptimizationService.optimize_campaign(campaign.id)

        return Response(optimization)

    @action(detail=True, methods=["post"])
    def apply_optimization(self, request, pk=None):
        """
        Apply optimization suggestions to a campaign.

        Request body should contain:
        {
            "apply_ml_segments": true,
            "selected_segment_ids": [1, 2, 3],
            "create_new_segments": true,
            "new_segments": [
                {
                    "name": "Segment Name",
                    "description": "Segment Description",
                    "patient_ids": ["uuid1", "uuid2"]
                }
            ],
            "apply_timing_optimization": true,
            "start_date": "2025-05-01T10:00:00Z",
            "apply_content_optimization": true,
            "email_template": "...",
            "sms_template": "..."
        }
        """
        campaign = self.get_object()

        # Apply optimization
        result = CampaignOptimizationService.apply_optimization(campaign.id, request.data)

        return Response(result)

    @action(detail=False, methods=["post"])
    def create_followup_campaign(self, request):
        """Create a new campaign targeting inactive patients"""
        # Get list of inactive patients
        days_threshold = request.data.get("days_threshold", 90)
        # default the campaign to target all patients if payload wasn't not provided
        risk_level = request.data.get("risk_level", "all")  # 'all', 'high', 'medium'
        # Validate risk level
        if risk_level not in ["all", "high", "medium"]:
            return Response(
                {"error": "Invalid risk_level parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Validate days threshold
        if not isinstance(days_threshold, (int, str)):
            return Response(
                {"error": "Invalid days_threshold parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            days_threshold = int(days_threshold)
        except (TypeError, ValueError):
            return Response(
                {"error": "Invalid days_threshold parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get inactive patients and filter by risk level if needed
        inactive_patients = CampaignPredictionService.predict_inactive_patients(
            days_threshold
        )

        if risk_level == "high":
            inactive_patients = [p for p in inactive_patients if p["risk_score"] >= 0.7]
        elif risk_level == "medium":
            inactive_patients = [
                p for p in inactive_patients if 0.5 <= p["risk_score"] < 0.7
            ]

        # Check if we have patients to target
        if not inactive_patients:
            return Response(
                {"error": "No inactive patients found matching the criteria"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get patient IDs
        patient_ids = [p["patient_id"] for p in inactive_patients]

        # Set default dates if not provided
        now = timezone.now()
        start_date = request.data.get("start_date", now.isoformat())
        end_date = request.data.get("end_date", (now + timedelta(days=30)).isoformat())

        # Create a list of target locations and age groups from the inactive patients
        target_locations = list(
            set(
                Patient.objects.filter(id__in=patient_ids).values_list(
                    "location", flat=True
                )
            )
        )
        target_age_groups = list(
            set(
                Patient.objects.filter(id__in=patient_ids).values_list(
                    "age_group", flat=True
                )
            )
        )

        # Create campaign data with all required fields
        campaign_data = {
            "title": request.data.get(
                "title", f"Follow-up Campaign ({days_threshold} days)"
            ),
            "description": request.data.get(
                "description",
                f"Campaign targeting inactive patients with {risk_level} risk level",
            ),
            "category": request.data.get("category"),
            "start_date": start_date,
            "end_date": end_date,
            "is_active": request.data.get("is_active", True),
            "email_template": request.data.get(
                "email_template",
                "<p>Hello {{username}},</p><p>We haven't heard from you in a while. "
                "Please check in with us by clicking <a href='{{appointment_link}}'>here</a>.</p>",
            ),
            "sms_template": request.data.get(
                "sms_template",
                "Hello {{username}}, we haven't heard from you in a while. "
                "Please check in with us: {{appointment_link}}",
            ),
            "target_age_groups": target_age_groups,
            "target_locations": target_locations,
            "target_languages": request.data.get("target_languages", ["fr", "en"]),
        }

        # Validate and create campaign using serializer
        serializer = self.get_serializer(data=campaign_data)
        if serializer.is_valid():
            campaign = serializer.save()
            campaign._current_user_id = request.user.id
            campaign.save()

            # Create a patient segment for this campaign with proper criteria
            segment_criteria = {
                "inactive": True,
                "days_threshold": days_threshold,
                "risk_level": risk_level,
                "patient_ids": patient_ids,  # Store specific patient IDs
            }

            segment = PatientSegment.objects.create(
                name=f"Inactive Patients ({days_threshold} days, {risk_level} risk)",
                description=f"Patients identified as inactive or at risk as of {now.strftime('%Y-%m-%d')}",
                criteria=segment_criteria,
                is_active=True,
            )
            segment.campaigns.add(campaign)

            # Return success response with detailed information
            return Response(
                {
                    "status": "success",
                    "campaign_id": campaign.id,
                    "campaign": serializer.data,
                    "targeted_patients": len(patient_ids),
                    "segment_id": segment.id,
                    "risk_level": risk_level,
                    "days_threshold": days_threshold,
                }
            )

        # Return validation errors from serializer
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientSegmentViewSet(viewsets.ModelViewSet):
    queryset = PatientSegment.objects.all()
    serializer_class = PatientSegmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["get"])
    def patients(self, request, pk=None):
        """Get all patients matching this segment's criteria"""
        segment = self.get_object()
        from services.segmentation import SegmentationService

        # Get patients matching the segment criteria
        patients = SegmentationService.get_patients_by_criteria(segment.criteria)

        # Get pagination parameters
        page = self.paginate_queryset(patients)

        # Serialize the patients
        from patients.serializers import PatientSerializer

        if page is not None:
            serializer = PatientSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PatientSerializer(patients, many=True)

        # Include segment statistics
        stats = SegmentationService.update_segment_statistics(segment)

        return Response(
            {"count": patients.count(), "patients": serializer.data, "statistics": stats}
        )


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


class StaffAnalyticsViewSet(viewsets.ViewSet):
    """ViewSet for staff-only analytics functions"""

    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    @action(detail=False, methods=["get"])
    def inactive_patients(self, request):
        """
        Get a list of patients at risk of becoming inactive
        who should be targeted for follow-up communications.
        """
        days_threshold = request.query_params.get("days", 90)
        try:
            days_threshold = int(days_threshold)
        except (TypeError, ValueError):
            days_threshold = 90

        results = CampaignPredictionService.predict_inactive_patients(days_threshold)

        return Response(
            {"count": len(results), "threshold_days": days_threshold, "patients": results}
        )
