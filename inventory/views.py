from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Medicine
from .serializers import MedicineSerializer
from datetime import date
from statistics import mean
from rest_framework.generics import ListCreateAPIView
from .models import Medicine
from .serializers import MedicineSerializer
from rest_framework.permissions import IsAdminUser, AllowAny


# -------------------------
# Add + Get all medicines
# -------------------------

class MedicineListCreate(ListCreateAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAdminUser()]
# -------------------------
# Get / Delete single
# -------------------------

class MedicineDetail(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        medicine = get_object_or_404(Medicine, pk=pk)
        serializer = MedicineSerializer(medicine)
        return Response(serializer.data)

    def delete(self, request, pk):
        medicine = get_object_or_404(Medicine, pk=pk)
        medicine.delete()
        return Response({"message": "Deleted successfully"})


# -------------------------
# Expiry Alert API
# -------------------------

class ExpiryAlert(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        today = date.today()
        alerts = []
        
        medicines = Medicine.objects.all()

        for med in medicines:
            days_left = (med.expiry_date - today).days

            if days_left <= 30:   # threshold (1 month)
                alerts.append({
                    "medicine": med.name,
                    "expired_since": f"{abs(days_left)} days",
                    "expiry_date": med.expiry_date
                })

        return Response(alerts)


# -------------------------
# Demand Forecast (Moving Average)
# -------------------------

class DemandForecast(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        """
        Expected input:
        {
          "medicine_id": 1,
          "past_sales": [10,12,11,14,13],
          "window_size": 3,
          "reorder_level": 20
        }
        """

        med_id = request.data["medicine_id"]
        past_sales = request.data["past_sales"]
        window = request.data["window_size"]
        reorder_level = request.data["reorder_level"]

        medicine = get_object_or_404(Medicine, id=med_id)

        # ---- Moving Average Logic ----
        if len(past_sales) < window:
            return Response(
                {"error": "Not enough data"},
                status=400
            )

        recent_data = past_sales[-window:]
        forecast = sum(recent_data) / window

        alert = False
        if medicine.quantity < forecast + reorder_level:
            alert = True

        return Response({
            "medicine": medicine.name,
            "current_stock": medicine.quantity,
            "forecast_demand": round(forecast, 2),
            "reorder_level": reorder_level,
            "demand_alert": alert
        })
