from rest_framework import serializers
from users.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "password", "role"]
        read_only_fields = ["id"]
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role"]