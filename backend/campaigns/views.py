from typing import override
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django.utils import timezone
from datetime import timedelta

from patients.models import Patient
from services.ai.prediction import CampaignPredictionService
from services.analytics import AnalyticsService
from services.optimization import CampaignOptimizationService
from services.ml_segmentation import MLSegmentationService
from services.personalization import PersonalizationService
from services.proactive_identification import ProactiveIdentificationService
from services.enhanced_analytics import EnhancedAnalyticsService

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

    @override
    def get_queryset(self):
        is_active = self.request.query_params.get("active", None)
        if is_active is None:
            return Campaign.objects.all()
        else:
            return Campaign.objects.filter(is_active=is_active)

    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {"error": "Only staff members can create campaigns"},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().create(request, *args, **kwargs)

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
            comm_type = patient.preferred_contact_methods
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
    def analytics(self, request, pk=None):
        """
        Get detailed analytics for this campaign.

        Query parameters:
        - days: Number of days to look back (default: 90)
        """
        campaign = self.get_object()
        days = request.query_params.get("days", 90)

        try:
            days = int(days)
        except (TypeError, ValueError):
            days = 90

        results = EnhancedAnalyticsService.get_campaign_performance(
            campaign_id=campaign.id, days=days
        )

        return Response(results)

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

    @action(detail=True, methods=["get"])
    def personalized_templates(self, request, pk=None):
        """
        Get personalized message templates for a campaign.

        Query parameters:
        - patient_id: Optional ID of a specific patient to personalize for
        """
        campaign = self.get_object()

        # Get patient ID from query parameters
        patient_id = request.query_params.get("patient_id")

        # Get personalized templates
        templates = PersonalizationService.suggest_personalized_templates(
            campaign.id, patient_id
        )

        return Response(templates)

    @action(detail=True, methods=["post"])
    def personalize_message(self, request, pk=None):
        """
        Personalize a message template for a specific patient.

        Request body should contain:
        {
            "template_content": "Hello {{first_name}}...",
            "patient_id": "uuid"
        }
        """
        campaign = self.get_object()

        # Validate request data
        template_content = request.data.get("template_content")
        patient_id = request.data.get("patient_id")

        if not template_content:
            return Response(
                {"error": "template_content is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not patient_id:
            return Response(
                {"error": "patient_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Personalize the message
        result = PersonalizationService.personalize_message(
            template_content, patient_id, campaign.id
        )

        return Response(result)

    @action(detail=True, methods=["get"])
    def message_effectiveness(self, request, pk=None):
        """
        Analyze the effectiveness of different message templates.
        """
        campaign = self.get_object()

        # Analyze message effectiveness
        analysis = PersonalizationService.analyze_message_effectiveness(campaign.id)

        return Response(analysis)

    @action(detail=False, methods=["get"])
    def template_variables(self, request):
        """
        Get a list of available template variables.
        """
        # Get template variables
        variables = PersonalizationService.get_template_variables()

        return Response(variables)

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

    @action(detail=True, methods=["get"])
    def analyze(self, request, pk=None):
        """
        Analyze a segment to extract key characteristics and patterns.

        This endpoint provides detailed analysis of the segment, including:
        - Demographic breakdown
        - Engagement metrics
        - Communication preferences
        - Campaign response history
        """
        segment = self.get_object()

        # Use ML segmentation service to analyze the segment
        analysis = MLSegmentationService.analyze_segment(segment.id)

        return Response(analysis)

    @action(detail=False, methods=["post"])
    def create_ml_segments(self, request):
        """
        Create ML-driven segments using clustering algorithms.

        Request body should contain:
        {
            "algorithm": "kmeans",  # or "dbscan"
            "n_clusters": 3,
            "name_prefix": "ML Segment"
        }
        """
        # Get parameters from request
        algorithm = request.data.get("algorithm", "kmeans")
        n_clusters = request.data.get("n_clusters", 3)
        name_prefix = request.data.get("name_prefix", "ML Segment")

        # Validate parameters
        if algorithm not in ["kmeans", "dbscan"]:
            return Response(
                {"error": "Invalid algorithm. Must be 'kmeans' or 'dbscan'"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            n_clusters = int(n_clusters)
            if n_clusters < 2 or n_clusters > 10:
                return Response(
                    {"error": "n_clusters must be between 2 and 10"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except (ValueError, TypeError):
            return Response(
                {"error": "n_clusters must be an integer"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create ML segments
        result = MLSegmentationService.create_ml_segments(
            algorithm=algorithm, n_clusters=n_clusters, name_prefix=name_prefix
        )

        return Response(result)

    @action(detail=False, methods=["get"])
    def recommend_for_campaign(self, request):
        """
        Recommend segments for a campaign based on targeting criteria.

        Query parameters:
        - campaign_id: ID of the campaign
        """
        # Get campaign ID from query parameters
        campaign_id = request.query_params.get("campaign_id")

        if not campaign_id:
            return Response(
                {"error": "campaign_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Get segment recommendations
        recommendations = MLSegmentationService.recommend_segments_for_campaign(
            campaign_id
        )

        return Response(recommendations)

    @action(detail=True, methods=["post"])
    def link_to_campaign(self, request, pk=None):
        """
        Link a segment to a campaign.

        Request body should contain:
        {
            "campaign_id": 123
        }
        """
        segment = self.get_object()

        # Get campaign ID from request
        campaign_id = request.data.get("campaign_id")

        if not campaign_id:
            return Response(
                {"error": "campaign_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Link segment to campaign
        result = MLSegmentationService.link_segment_to_campaign(segment.id, campaign_id)

        return Response(result)


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

    # permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    @action(detail=False, methods=["get"])
    def inactive_patients(self, request):
        """
        Get a list of patients at risk of becoming inactive
        who should be targeted for follow-up communications.

        Query parameters:
        - days: Number of days since last contact (default: 90)
        - min_risk_score: Minimum risk score to include (default: 0.5)
        """
        days_threshold = request.query_params.get("days", 90)
        min_risk_score = request.query_params.get("min_risk_score", 0.5)

        try:
            days_threshold = int(days_threshold)
        except (TypeError, ValueError):
            days_threshold = 90

        try:
            min_risk_score = float(min_risk_score)
        except (TypeError, ValueError):
            min_risk_score = 0.5

        results = ProactiveIdentificationService.identify_inactive_patients(
            days_threshold=days_threshold, min_risk_score=min_risk_score
        )

        return Response(results)

    @action(detail=False, methods=["get"])
    def declining_engagement(self, request):
        """
        Identify patients with declining engagement over time.

        Query parameters:
        - lookback_days: Number of days to look back (default: 180)
        - engagement_drop_threshold: Minimum drop in engagement score (default: 0.2)
        """
        lookback_days = request.query_params.get("lookback_days", 180)
        engagement_drop_threshold = request.query_params.get(
            "engagement_drop_threshold", 0.2
        )

        try:
            lookback_days = int(lookback_days)
        except (TypeError, ValueError):
            lookback_days = 180

        try:
            engagement_drop_threshold = float(engagement_drop_threshold)
        except (TypeError, ValueError):
            engagement_drop_threshold = 0.2

        results = ProactiveIdentificationService.identify_declining_engagement(
            lookback_days=lookback_days,
            engagement_drop_threshold=engagement_drop_threshold,
        )

        return Response(results)

    @action(detail=False, methods=["get"])
    def follow_up_candidates(self, request):
        """
        Identify patients who need specific follow-up based on condition type.

        Query parameters:
        - condition_type: Type of condition to filter by (e.g., "vaccination", "dental", "chronic)
        - days_since_last_contact: Minimum days since last contact (default: 60)
        """
        condition_type = request.query_params.get("condition_type")
        days_since_last_contact = request.query_params.get("days_since_last_contact", 60)

        try:
            days_since_last_contact = int(days_since_last_contact)
        except (TypeError, ValueError):
            days_since_last_contact = 60

        results = ProactiveIdentificationService.identify_follow_up_candidates(
            condition_type=condition_type, days_since_last_contact=days_since_last_contact
        )

        return Response(results)

    @action(detail=True, methods=["get"], url_path="follow-up-recommendations")
    def follow_up_recommendations(self, request, pk=None):
        """
        Get personalized follow-up recommendations for a specific patient.
        """
        patient_id = pk

        results = ProactiveIdentificationService.get_follow_up_recommendations(patient_id)

        return Response(results)

    @action(detail=False, methods=["get"], url_path="dashboard")
    def dashboard(self, request):
        """
        Get comprehensive data for the engagement dashboard.

        Query parameters:
        - days: Number of days to look back (default: 90)
        """
        days = request.query_params.get("days", 90)

        try:
            days = int(days)
        except (TypeError, ValueError):
            days = 90

        results = EnhancedAnalyticsService.get_dashboard_data(days=days)

        return Response(results)

    @action(detail=False, methods=["get"], url_path="engagement-overview")
    def engagement_overview(self, request):
        """
        Get an overview of patient engagement metrics.

        Query parameters:
        - days: Number of days to look back (default: 30)
        """
        days = request.query_params.get("days", 30)

        try:
            days = int(days)
        except (TypeError, ValueError):
            days = 30

        results = EnhancedAnalyticsService.get_engagement_overview(days=days)

        return Response(results)

    @action(detail=False, methods=["get"], url_path="engagement-trends")
    def engagement_trends(self, request):
        """
        Get engagement trends over time.

        Query parameters:
        - days: Number of days to look back (default: 90)
        - interval: Time interval for grouping (day, week, month) (default: week)
        """
        days = request.query_params.get("days", 90)
        interval = request.query_params.get("interval", "week")

        try:
            days = int(days)
        except (TypeError, ValueError):
            days = 90

        if interval not in ["day", "week", "month"]:
            interval = "week"

        results = EnhancedAnalyticsService.get_engagement_trends(
            days=days, interval=interval
        )

        return Response(results)

    @action(detail=False, methods=["get"], url_path="campaign-performance")
    def campaign_performance(self, request):
        """
        Get performance metrics for campaigns.

        Query parameters:
        - campaign_id: Optional ID of a specific campaign
        - days: Number of days to look back (default: 90)
        """
        campaign_id = request.query_params.get("campaign_id")
        days = request.query_params.get("days", 90)

        try:
            days = int(days)
        except (TypeError, ValueError):
            days = 90

        results = EnhancedAnalyticsService.get_campaign_performance(
            campaign_id=campaign_id, days=days
        )

        return Response(results)

    @action(detail=False, methods=["get"], url_path="segment-performance")
    def segment_performance(self, request):
        """
        Get performance metrics for patient segments.

        Query parameters:
        - segment_id: Optional ID of a specific segment
        - days: Number of days to look back (default: 90)
        """
        segment_id = request.query_params.get("segment_id")
        days = request.query_params.get("days", 90)

        try:
            days = int(days)
        except (TypeError, ValueError):
            days = 90

        results = EnhancedAnalyticsService.get_segment_performance(
            segment_id=segment_id, days=days
        )

        return Response(results)

    @action(detail=False, methods=["get"], url_path="channel-metrics")
    def channel_metrics(self, request):
        """
        Get performance metrics for different communication channels.

        Query parameters:
        - days: Number of days to look back (default: 90)
        """
        days = request.query_params.get("days", 90)
        campaign_id = request.query_params.get("campaign_id")
        try:
            days = int(days)
        except (TypeError, ValueError):
            days = 90

        results = EnhancedAnalyticsService.get_communication_channel_metrics(
            campaign_id=campaign_id, days=days
        )

        return Response(results)

    @action(detail=False, methods=["get"], url_path="time-metrics")
    def time_metrics(self, request):
        """
        Get performance metrics for different times of day.

        Query parameters:
        - days: Number of days to look back (default: 90)
        """
        days = request.query_params.get("days", 90)

        try:
            days = int(days)
        except (TypeError, ValueError):
            days = 90

        results = EnhancedAnalyticsService.get_time_of_day_metrics(days=days)

        return Response(results)

    @action(detail=False, methods=["post"], url_path="test-sms")
    def test_sms(self, request):
        """
        Send a test SMS message to a specified phone number.

        Request body should contain:
        {
            "phone_number": "+21622492052",
            "message": "Test message content"
        }
        """
        # Validate request data
        phone_number = request.data.get("phone_number")
        message = request.data.get("message")

        if not phone_number:
            return Response(
                {"error": "phone_number is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not message:
            return Response(
                {"error": "message is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Import the SMS service
        # from services.communications import SMSService

        # Send the test SMS
        # try:
        #     result = SMSService.send_test_sms(phone_number, message)
        #     print("To: ", phone_number)
        #     return Response(result)
        # except Exception as e:
        #     return Response(
        #         {"error": f"Failed to send SMS: {str(e)}"},
        #         status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #     )

        # Debug prints instead
        print("Would send SMS to:", phone_number)
        print("Message content:", message)
        return Response(
            {
                "status": "Test SMS simulation successful",
                "phone": phone_number,
                "message": message,
            }
        )
