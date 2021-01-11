from django.shortcuts import get_object_or_404
from rest_framework import permissions, generics, viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from .models import User, EmailCode, UserRole
from api.permissions import IsAdminOrAuthor, IsAdminOrProhibited
from .serializers import UsersSerializer, ConfirmathionCodeSerializer, TokenSerializer, ProfileSerializer


class ObtainConfirmationCode(generics.CreateAPIView):
    serializer_class = ConfirmathionCodeSerializer
    permission_classes = [permissions.AllowAny]

@api_view(['POST'])
@permission_classes([AllowAny])
def obtain_token(request):
    serializer = TokenSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    email = serializer.data.get('email', '')
    instance = EmailCode.objects.get(email=email)
    if User.objects.filter(email=email).exists():
        user = get_object_or_404(User, email=email)
        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)
        return Response({'access token': f'{access_token}',
                         'refresh token': f'{refresh_token}'},
                          status=status.HTTP_200_OK)
    else:
        user = User.objects.create(email=email, username=instance.username)
        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)
        return Response({'access token': f'{access_token}',
                         'refresh token': f'{refresh_token}'},
                          status=status.HTTP_201_CREATED)     
    

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrProhibited]
    lookup_field = 'username'
   
    @action(detail=False, methods=['get', 'patch'], permission_classes=[permissions.IsAuthenticated, IsAdminOrAuthor])
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = ProfileSerializer(user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        serializer = ProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)