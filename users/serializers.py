from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

# -----------------------------
# Signup Serializer
# -----------------------------
class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # hash the password
        user.save()
        return user

# -----------------------------
# Login Serializer
# -----------------------------
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
