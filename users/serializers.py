import uuid

from django.core.mail import send_mail
from rest_framework import serializers, status

from .models import User, EmailCode

class ConfirmathionCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    def create(self, validated_data):
        email = validated_data['email']
        code = uuid.uuid4()
        username = validated_data['username']

        ec = EmailCode.objects.create(email=email, confirmation_code=code, username=username)

        send_mail(
            'Successful registration', f'Welcome to yamdb, your confirmation code is {code}', 'yamdb_reg@yamdb.com', [email], fail_silently=False,
        )
        
        return ec

class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)

class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('first_name', 'last_name', 'username', 'email', 'bio', 'role')
        model = User

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('first_name', 'last_name', 'username', 'email', 'bio', 'role')
        read_only_fields = ('role',)
        model = User