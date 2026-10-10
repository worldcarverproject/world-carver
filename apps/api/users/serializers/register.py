from django.contrib.auth import get_user_model
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'}
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user
    
    
class EmailVerificationSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    token = serializers.CharField(max_length=555)
    
    
class ResendVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)