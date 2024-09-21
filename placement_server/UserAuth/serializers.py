from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserRoles

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'student_id', 'email', 'is_active']

class StudentRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})
    role = serializers.ChoiceField(choices=UserRoles.choices, default=UserRoles.STUDENT)

    class Meta:
        model = User
        fields = ['student_id', 'email', 'password', 'password_confirm', 'role']

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ConfirmEmailSerializer(serializers.Serializer):
    code = serializers.CharField()

class ConfirmationSerializer(serializers.Serializer):
    student_id = serializers.CharField()
    confirmation_code = serializers.CharField()