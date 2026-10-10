from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import generics, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models.user import User
from utils.email_send import send_verification_email
from utils.tokens import TokenGenerator

from ..serializers import (
    RegisterSerializer,
    EmailVerificationSerializer,
    ResendVerificationSerializer
)

class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    
    def perform_create(self, serializer):
        user = serializer.save()
        # Additional logic after user creation can be added here
        send_verification_email(user, self.request)
        
class VerifyEmailView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EmailVerificationSerializer
    
    def __verify_email(self, user: User, token: str) -> bool:
        account_activation_token = TokenGenerator()      
        if user and account_activation_token.check_token(user, token):
            return True
        return False
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        uuid = serializer.validated_data['uuid']
        token = serializer.validated_data['token']
        user = get_object_or_404(get_user_model(), id=uuid)
        
        if user.is_email_verified:
            return Response({"message": "Email is already verified."}, status=400)
              
        if not self.__verify_email(user, token):
            return Response({"message": "Activation link is invalid."}, status=400)

        user.is_email_verified = True
        user.email_verified_at = timezone.now()
        user.save()
        return Response({"message": "Email verified successfully."}, status=200)
            
class ResendVerificationView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ResendVerificationSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        user = get_object_or_404(get_user_model(), email=email)
        # Additional logic after user creation can be added here
        send_verification_email(user, self.request)
        return Response({"message": "Verification email sent successfully."}, status=200)