import django_filters
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from patients.models import ConsentRecord

from services.ai.clustering import PatientClusteringService
from services.proactive_identification import ProactiveIdentificationService

from .models import Patient
from .serializers import (
    PatientConsentRecordSerializer,
    PatientConsentSerializer,
    PatientPreferencesSerializer,
    PatientSerializer,
)

from campaigns.models import CommunicationLog


class PatientFilter(django_filters.FilterSet):
    """Filter for the Patient model"""

    age_group = django_filters.CharFilter(lookup_expr="exact")
    location = django_filters.CharFilter(lookup_expr="icontains")
    gender = django_filters.CharFilter(lookup_expr="exact")
    preferred_contact_method = django_filters.CharFilter(lookup_expr="exact")
    has_active_consent = django_filters.BooleanFilter()
    created_at_after = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    created_at_before = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )
    anonymized = django_filters.BooleanFilter(field_name="anonymized")

    class Meta:
        model = Patient
        fields = [
            "age_group",
            "location",
            "gender",
            "preferred_contact_method",
            "has_active_consent",
            "created_at_after",
            "created_at_before",
            "anonymized",
        ]


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = PatientFilter

    def get_queryset(self):
        user = self.request.user
        # Staff can see all patients, patients only see themselves

        if user.user_type == "PATIENT":
            return Patient.objects.filter(user=user)
        filter = self.request.query_params.get("filter", None)
        if filter == "active":
            return Patient.objects.filter(has_active_consent=True)
        elif filter == "inactive":
            return Patient.objects.filter(has_active_consent=False)
        return Patient.objects.all()

    @action(
        detail=True,
        methods=["get", "patch"],
        url_path="consents(?:/(?P<consent_id>[^/.]+))?",
    )
    def consents(self, request, pk=None, consent_id=None):
        """
        Return all consent records for this patient or a specific consent record by ID.
        """
        patient = self.get_object()
        patient_consents = patient.get_active_consents()
        if consent_id is None:
            if request.method == "PATCH":
                for consent in patient_consents:
                    new_consent_data = next(
                        (
                            c
                            for c in request.data.get("consents", [])
                            if c["pk"] == consent.id
                        ),
                        None,
                    )
                    if new_consent_data:
                        consent.granted = new_consent_data["granted"]
                        consent.save()

        if consent_id:
            consent_record = patient.consent_records.filter(id=consent_id).first()
            if not consent_record:
                return Response(
                    {"error": "Consent record not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            granted = request.data.get("granted", consent_record.granted)
            consent_record.granted = granted
            consent_record.save()
            serializer = PatientConsentRecordSerializer(consent_record, many=False)
        else:
            serializer = PatientConsentRecordSerializer(patient_consents, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def communications(self, request, pk):
        """Get communication history for a specific patient"""
        patient = Patient.objects.get(pk=pk)
        recent_logs = CommunicationLog.objects.filter(patient=patient).order_by(
            "-sent_at"
        )[:10]

        serialized_logs = [
            {
                "id": log.id,
                "campaign": log.campaign.title if log.campaign else None,
                "communication_type": log.communication_type,
                "status": log.status,
                "sent_at": log.sent_at.isoformat() if log.sent_at else None,
                "delivered_at": log.delivered_at.isoformat()
                if log.delivered_at
                else None,
                "read_at": log.read_at.isoformat() if log.read_at else None,
            }
            for log in recent_logs
        ]
        return Response(serialized_logs)

    @action(detail=True, methods=["get", "patch"])
    def preferences(self, request, pk=None):
        patient = self.get_object()
        if request.method == "GET":
            serializer = PatientPreferencesSerializer(patient)
            return Response(serializer.data, status=200)
        else:
            serializer = PatientPreferencesSerializer(
                patient, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get", "patch"])
    def consent(self, request, pk=None):
        patient = self.get_object()
        if request.method == "GET":
            serializer = PatientConsentSerializer(patient)
            return Response(serializer.data)
        else:
            serializer = PatientConsentSerializer(patient, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def anonymize(self, request, pk=None):
        patient = self.get_object()
        if patient.anonymized:
            return Response({"status": "Patient data has already been anonymized"})
        patient.anonymize()
        return Response({"status": "Patient data has been anonymized"})

    @action(detail=True, methods=["post"])
    def schedule_deletion(self, request, pk=None):
        patient = self.get_object()
        days = request.data.get("days", 30)
        deletion_date = patient.schedule_deletion(days)
        return Response({"status": "Deletion scheduled", "scheduled_date": deletion_date})

    @action(detail=True, methods=["post"])
    def record_consent(self, request, pk=None, granted=True):
        """Record a new consent decision for this patient"""
        patient = self.get_object()

        serializer = PatientConsentRecordSerializer(data=request.data)
        if serializer.is_valid():
            consent_type = serializer.validated_data["consent_type"]
            granted = serializer.validated_data.get("granted", granted)
            metadata = serializer.validated_data.get("metadata", {})

            # Record the consent with IP tracking
            ip_address = request.META.get("REMOTE_ADDR", None)
            patient.record_consent(
                consent_type=consent_type,
                granted=granted,
                user=request.user,
                ip_address=ip_address,
                metadata=metadata,
            )

            return Response(
                {
                    "status": "Consent granted" if granted else "Consent denied",
                    "consent_type": consent_type,
                    "granted": granted,
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get", "patch", "post"])
    def active_consents(self, request, pk=None):
        """Get all active consents for this patient"""
        patient = self.get_object()
        active_consents = patient.get_active_consents()
        # Convert to serializable format
        if request.method == "POST" and request.user.is_staff:
            consents = request.data.get("consents", [])
            ConsentRecord.objects.filter(patient=patient).delete()
            for consent in consents:
                patient.record_consent(
                    consent_type=consent["consent_type"],
                    granted=consent.get("granted", True),
                    user=request.user,
                )
                patient.save()
            return Response(
                {
                    "status": "Consents created",
                    "consents": PatientConsentRecordSerializer(
                        ConsentRecord.objects.filter(patient=patient), many=True
                    ).data,
                }
            )
        serializable = PatientConsentRecordSerializer(active_consents, many=True).data
        if request.method == "PATCH":
            for consent in active_consents:
                for new_consent in request.data.get("consents", []):
                    if new_consent["consent_type"] == consent.consent_type:
                        consent.granted = new_consent.get("granted", consent.granted)
                        print(consent)
                        consent.save()
                        break
            serialized_active_consents = PatientConsentRecordSerializer(
                patient.get_active_consents(), many=True
            ).data
            return Response(serialized_active_consents)

        return Response(serializable)

    @action(detail=True, methods=["post"])
    def export_data(self, request, pk=None):
        """Export patient data in structured format (GDPR right to data portability)"""
        patient = self.get_object()
        from services.gdpr import GDPRService

        data = GDPRService.export_patient_data(patient)

        # Log this export for audit purposes
        from django.contrib.admin.models import CHANGE, LogEntry
        from django.contrib.contenttypes.models import ContentType

        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(patient).pk,
            object_id=patient.id,
            object_repr=str(patient),
            action_flag=CHANGE,
            change_message=f"Patient data exported by {request.user.username}",
        )

        return Response({"data": data, "exported_at": timezone.now().isoformat()})

    @action(detail=False, methods=["get"])
    def clusters(self, request):
        """Get patient clusters based on similarities"""
        # Only staff can access clustering for all patients
        if not request.user.is_staff and not request.user.is_superuser:
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        n_clusters = int(request.query_params.get("n_clusters", 5))
        consent_only = request.query_params.get("consent_only", "true").lower() == "true"

        result = PatientClusteringService.cluster_patients(
            n_clusters=n_clusters, include_only_with_consent=consent_only
        )

        return Response(result)

    @action(detail=True, methods=["get"])
    def cluster_info(self, request, pk=None):
        """Get cluster information for a specific patient"""
        patient = self.get_object()
        n_clusters = int(request.query_params.get("n_clusters", 5))

        result = PatientClusteringService.get_patient_cluster(
            patient_id=str(patient.id), n_clusters=n_clusters
        )

        return Response(result)

    @action(detail=True, methods=["get"], url_path="follow-up-recommendations")
    def follow_up_recommendations(self, request, pk=None):
        """
        Get personalized follow-up recommendations for a specific patient.

        This endpoint provides:
        - Best contact method based on historical engagement
        - Optimal contact timing
        - Personalized follow-up recommendations
        """
        patient = self.get_object()

        # Get follow-up recommendations
        result = ProactiveIdentificationService.get_follow_up_recommendations(
            str(patient.id)
        )

        return Response(result)
