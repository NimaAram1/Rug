from rest_framework.views import APIView, Response
from django.contrib.auth import get_user_model
from rest_framework import status
from .serializers import (
    RegisterationSerializer
) 

# getting user model
User = get_user_model()

class RegisterationApiView(APIView):
    """
    Get username, email, name, and password from the user
    and save it in the database
    """
    def post(self, request):
        if request.user.is_anonymous:
            data = RegisterationSerializer(data=request.data)
            if data.is_valid():
                User.objects.create_user(email=data.validated_data["email"], username=data.validated_data["username"],
                password=data.validated_data["password"], name=data.validated_data["name"])
                return Response({
                "message": f'{data.validated_data["email"]} account created successfully'
                }, status=status.HTTP_201_CREATED)
            
            else:
                return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": "You already authorized"
            }, status=status.HTTP_400_BAD_REQUEST)   