from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"", views.PatientViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "<str:pk>/communications/",
        views.PatientViewSet.as_view({"get": "communications"}),
        name="patient-communications",
    ),
]
