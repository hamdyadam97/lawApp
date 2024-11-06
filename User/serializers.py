from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import AdminUser, User, Lawyer

# Serializer for Admin profile information
class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = ['id', 'username', 'email', 'address', 'phone', 'photo_path', 'lawfirm', 'office']
        read_only_fields = ['id', 'office']  # Only allow updating username, email, etc.


# Serializer for User model
class UserSerializer(serializers.ModelSerializer):
    refresh = serializers.CharField(read_only=True, source='token')
    access = serializers.CharField(read_only=True, source='token.access_token')

    def validate_password(self, data):
        validate_password(data)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'address', 'gender', 'id_document', 'photo_path', 'office',]
        read_only_fields = ['id', 'office']
        extra_kwargs = {
            'password': {'write_only': True},


        }

# Serializer for Lawyer model
class LawyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lawyer
        fields = ['id', 'username', 'email', 'phone', 'address', 'gender', 'id_document', 'photo_path', 'office']
        read_only_fields = ['id', 'office']


