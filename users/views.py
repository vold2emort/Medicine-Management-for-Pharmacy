from rest_framework import generics, views, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, get_user_model

from .serializers import UserSignupSerializer, UserLoginSerializer

User = get_user_model()

# -----------------------------
# Signup API
# -----------------------------
class SignupAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        headers = self.get_success_headers(serializer.data)
        return Response({
            "message": "User created successfully",
            "token": token.key,
            "role": user.role
        }, status=status.HTTP_201_CREATED, headers=headers)

# -----------------------------
# Login API
# -----------------------------

class LoginAPIView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        # This allows the DRF browsable API to show the form
        return Response({"message": "Send POST request with username and password"})

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Login successful",
                "token": token.key,
                "role": user.role
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)