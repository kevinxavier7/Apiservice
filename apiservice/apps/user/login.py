from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import TokenObtainSerializer, UserListSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status


class Login(TokenObtainPairView):

    serializer_class = TokenObtainSerializer

    def post(self, request, *args, **kwargs):

        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(
            username = username,
            password = password
        )

        if user:
            login_serializer = self.serializer_class(data = request.data)
            if login_serializer.is_valid():
                user_serializer = UserListSerializer(user)
                return Response({
                    'message':'login successfull',
                    'token': login_serializer.validated_data.get('access'),
                    'token-refresh': login_serializer.validated_data.get('refresh'),
                    'user': user_serializer.data
                }, status= status.HTTP_200_OK)
            return Response(status= status.HTTP_400_BAD_REQUEST)
        return Response({
            'error':'user not found'
        }, status= status.HTTP_404_NOT_FOUND)