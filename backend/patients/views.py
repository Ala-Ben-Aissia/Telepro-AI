from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Patient
from .serializers import (
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
