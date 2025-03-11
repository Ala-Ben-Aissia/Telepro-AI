from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"categories", views.CampaignCategoryViewSet)
router.register(r"campaigns", views.CampaignViewSet)
router.register(r"segments", views.PatientSegmentViewSet)
router.register(r"communications", views.CommunicationLogViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
