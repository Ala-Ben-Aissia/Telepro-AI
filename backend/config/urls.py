from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from drf_yasg import openapi, views
from rest_framework import permissions

schema_view = views.get_schema_view(
    openapi.Info(
        title="Telepro-AI API",
        default_version="v1",
        description="API for patient teleprospection with AI",
        terms_of_service="https://www.teleproai.com/terms/",
        contact=openapi.Contact(email="contact@teleproai.com"),
        license=openapi.License(name="Private License"),
    ),
    public=False,
    permission_classes=[permissions.IsAuthenticated],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/accounts/", include("accounts.urls")),
    path("api/patients/", include("patients.urls")),
    path("api/campaigns/", include("campaigns.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
