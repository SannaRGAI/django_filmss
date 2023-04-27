from rest_framework import serializers
from .models import CustomUser as User

class RegisterUserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password',
            'password_confirm'
        ]

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'User with this email alreadt exists'
            )
        return email
    
    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.pop('password_confirm')

        if p1 != p2:
            raise serializers.ValidationError(
                'Passwords do not match'
            )
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)