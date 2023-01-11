from rest_framework import viewsets
from rest_framework.response import Response
from .models import User
from .serializers import UserListSerializer, UserCreateSerializer, ChangePasswordSerializer
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


class UserApiViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]

    serializer_class = UserListSerializer

    def get_queryset(self, pk = None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.all()
        return self.get_serializer().Meta.model.filter(id = pk).first()

    
    def list(self, request, pk = None):
        user = self.serializer_class(self.get_queryset(pk), many = True)
        return Response(user.data, status= status.HTTP_200_OK)


    def create(self, request):
        user_serializer = UserCreateSerializer(data= request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                'message': 'user created successfully'
            }, status= status.HTTP_200_OK)
        return Response(user_serializer.errors, status= status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk):
        user = User.objects.filter(id = pk).first()
        if user:           
            user_serializer = self.serializer_class(user, data= request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response({
                    'message': 'user updated successfully'
                }, status= status.HTTP_200_OK)
            return Response(user_serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        return Response({
            'error':'user not found'
        }, status= status.HTTP_404_NOT_FOUND)
    
    
    def destroy(self, request, pk):
        user = User.objects.filter(id = pk).first()
        if user:
            user.delete()
            return Response({
                'message': 'user deleted successfully'
            }, status= status.HTTP_200_OK)
        return Response({
            'error':'user not found'
        }, status= status.HTTP_404_NOT_FOUND)


class ChangePasswordAPIView(APIView):

    def post(self, request):
        user = User.objects.filter(id = request.data['id_user']).values('password').first()

        if user:
            user_serializer = ChangePasswordSerializer(data= request.data)
            if user_serializer.is_valid():
                
                if check_password(request.data['old_password'], user['password']):
                    User.objects.filter(id = request.data['id_user']).update(password = make_password(request.data['new_password']))
                    return Response({
                        'message': 'password change successfull'
                    }, status= status.HTTP_200_OK)
                return Response({
                    'error':'old password is not correct'
                }, status= status.HTTP_400_BAD_REQUEST)
            return Response(user_serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        return Response({
            'error':'this user does not exist'
        }, status= status.HTTP_400_BAD_REQUEST)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "{}?token={}".format(reverse('password-reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
