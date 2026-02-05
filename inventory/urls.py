from django.urls import path
from .views import (
    MedicineListCreate,
    MedicineDetail,
    ExpiryAlert,
    DemandForecast
)

urlpatterns = [
    path('medicines/', MedicineListCreate.as_view()),
    path('medicines/<int:pk>/', MedicineDetail.as_view()),
    path('expiry-alerts/', ExpiryAlert.as_view()),
    path('forecast/', DemandForecast.as_view()),
]
