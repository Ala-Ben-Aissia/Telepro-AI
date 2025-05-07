from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"categories", views.CampaignCategoryViewSet)
router.register(r"segments", views.PatientSegmentViewSet, basename="segments")
router.register(r"communications", views.CommunicationLogViewSet)
router.register(r"analytics", views.StaffAnalyticsViewSet, basename="analytics")
router.register(r"", views.CampaignViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
