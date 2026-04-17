from django.urls import path

from apps.users.views.register import (
    RegisterAPIView,
    ResendVerificationCodeAPIView,
    VerifyCodeAPIView,
)

app_name = 'users'

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('verify-code/', VerifyCodeAPIView.as_view(), name='verify-code'),
    path('resend-code/', ResendVerificationCodeAPIView.as_view(), name='resend-code'),
]
