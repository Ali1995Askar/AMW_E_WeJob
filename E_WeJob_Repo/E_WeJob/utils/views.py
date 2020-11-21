from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import generics
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model


class SignupWizardView(generics.CreateAPIView):
    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_data = serializer.validated_data["user"]
            self.perform_create(serializer)
            user = authenticate(
                username=user_data["username"],
                password=user_data["password"],
            )
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        "username": user.username,
                        "token": token.key,
                    },
                    status=status.HTTP_201_CREATED,
                )
        except Exception as err:
            status_code = status.HTTP_409_CONFLICT
            response = {"error": str(err)}
            return Response(response, status=status_code)
