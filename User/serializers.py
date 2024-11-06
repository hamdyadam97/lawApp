from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import AdminUser, User, Lawyer

# Serializer for Admin profile information
class AdminProfileSerializer(serializers.ModelSerializer):
    refresh = serializers.CharField(read_only=True, source='token')
    access = serializers.CharField(read_only=True, source='token.access_token')

    def validate_password(self, data):
        validate_password(data)
        return data

    def create(self, validated_data):
        user = AdminUser.objects.create_user(**validated_data)

        return user
    class Meta:
        model = AdminUser
        fields = ['id', 'username', 'email', 'address', 'phone', 'photo', 'lawfirm', 'office',
                  'access','refresh','password','id_document','address','country','is_email_verified',
                  'email_verification_code','dob','gender','is_active','is_deactivated','date_joined',
                  ]
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
            'email_verification_code': {'read_only': True},
            'is_active': {'read_only': True},
            'is_deactivated': {'read_only': True},
            'date_joined': {'read_only': True},
            'is_email_verified': {'read_only': True},

        }

# login user
class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        try:
            super().validate(attrs)
        except AuthenticationFailed:
            raise serializers.ValidationError("Incorrect email or password")

        # Customize the response data with user information if desired
        user = self.user

        # Check the user type and select the appropriate serializer
        if isinstance(user, Lawyer):
            return LawyerSerializer(instance=user, context=self.context).data
        elif isinstance(user, AdminUser):
            return AdminProfileSerializer(instance=user, context=self.context).data
        else:
            return UserSerializer(instance=user, context=self.context).data




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
        fields = ['id', 'username', 'email', 'address', 'phone', 'photo', 'office',
                  'access', 'refresh', 'password', 'id_document', 'address', 'country', 'is_email_verified',
                  'email_verification_code', 'dob', 'gender', 'is_active', 'is_deactivated', 'date_joined',
                  ]
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
            'email_verification_code': {'read_only': True},
            'is_active': {'read_only': True},
            'is_deactivated': {'read_only': True},
            'date_joined': {'read_only': True},
            'is_email_verified': {'read_only': True},

        }

# Serializer for Lawyer model
class LawyerSerializer(serializers.ModelSerializer):
    refresh = serializers.CharField(read_only=True, source='token')
    access = serializers.CharField(read_only=True, source='token.access_token')


    def validate_password(self, data):
        validate_password(data)

    def create(self, validated_data):
        user = Lawyer.objects.create_user(**validated_data)

        return user

    class Meta:
        model = Lawyer
        fields = ['id', 'username', 'email', 'address', 'phone', 'photo', 'office',
                  'access', 'refresh', 'password', 'id_document', 'address', 'country', 'is_email_verified',
                  'email_verification_code', 'dob', 'gender', 'is_active', 'is_deactivated', 'date_joined',
                  ]
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
            'email_verification_code': {'read_only': True},
            'is_active': {'read_only': True},
            'is_deactivated': {'read_only': True},
            'date_joined': {'read_only': True},
            'is_email_verified': {'read_only': True},

        }

class CombinedUserSerializer(serializers.Serializer):
    clients = UserSerializer(many=True)
    lawyers = LawyerSerializer(many=True)