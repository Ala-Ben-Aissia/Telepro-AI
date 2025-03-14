from django.contrib import admin
from django.urls import include, path, re_path
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
    re_path(
        r"^api/swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^api/swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^api/redoc/$",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
