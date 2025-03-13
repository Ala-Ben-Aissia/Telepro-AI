from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Patient
from .serializers import (
    PatientConsentRecordSerializer,
    PatientConsentSerializer,
    PatientPreferencesSerializer,
    PatientSerializer,
)


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Staff can see all patients, patients only see themselves
        if user.user_type == "PATIENT":
            return Patient.objects.filter(user=user)
        return Patient.objects.all()

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
    def record_consent(self, request, pk=None):
        """Record a new consent decision for this patient"""
        patient = self.get_object()

        serializer = PatientConsentRecordSerializer(data=request.data)
        if serializer.is_valid():
            consent_type = serializer.validated_data["consent_type"]
            granted = serializer.validated_data["granted"]
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
                    "status": "Consent recorded",
                    "consent_type": consent_type,
                    "granted": granted,
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def active_consents(self, request, pk=None):
        """Get all active consents for this patient"""
        patient = self.get_object()
        active_consents = patient.get_active_consents()

        # Convert to serializable format
        serializable = [
            {
                "consent_type": consent_type,
                "granted_at": consent.timestamp,
                "recorded_by": consent.recorded_by.username
                if consent.recorded_by
                else "Self",
            }
            for consent_type, consent in active_consents.items()
        ]

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
