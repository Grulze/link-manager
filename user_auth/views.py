from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .serializers import UserListSerializer, PasswordResetSerializer

User = get_user_model()


class UserAPIList(generics.ListAPIView):
    """
    Display all registered users.
    """
    permission_classes = (AllowAny, )
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class ResetPasswordView(APIView):
    """
    Resetting the user's password to the default password ("default_password") at the transmitted email address.
    """
    permission_classes = (AllowAny, )

    @swagger_auto_schema(request_body=PasswordResetSerializer)
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        default_password = "default_password"

        if serializer.is_valid():
            email = serializer.validated_data.get("email")

            try:
                user = User.objects.get(email=email)
                user.set_password(default_password)
                user.save()
                return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
