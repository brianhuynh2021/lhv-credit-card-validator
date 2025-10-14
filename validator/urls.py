from django.urls import path
from .views import HealthView, ValidateView


app_name = "validator"

urlpatterns = [
    path("validate/", ValidateView.as_view(), name="card_validate"),
    path("health/", HealthView.as_view(), name="health_check"),
]
