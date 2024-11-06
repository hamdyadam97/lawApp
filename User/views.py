from django.shortcuts import render
from rest_framework import permissions, status, serializers
from rest_framework.exceptions import NotFound, APIException
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from User.models import User, Lawyer, AdminUser
from User.permission import AdminRequiredPermission
from User.serializers import AdminProfileSerializer, UserSerializer, LawyerSerializer, LoginSerializer


# Create your views here.
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class AdminProfileCreate(CreateAPIView):
    serializer_class = AdminProfileSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '')
        if AdminUser.objects.filter(email__iexact=email).exists():
            return Response({'detail': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        return self.create(request, *args, **kwargs)

# Admin Profile View (Retrieve and Update Admin)
class AdminProfileView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, AdminRequiredPermission]
    serializer_class = AdminProfileSerializer

    def get_object(self):
        return self.request.user


class GetAllUsersView(APIView):
    permission_classes = [permissions.IsAuthenticated, AdminRequiredPermission]

    def get(self, request, *args, **kwargs):
        # Assume the current user is an Admin with an associated office
        office_id = request.user.office_id

        # Query both User and Lawyer models filtered by office
        users = User.objects.filter(office_id=office_id)
        lawyers = Lawyer.objects.filter(office_id=office_id)

        # Combine users and lawyers into one list and serialize
        user_serializer = UserSerializer(users, many=True)
        lawyer_serializer = LawyerSerializer(lawyers, many=True)
        combined_data = {
            "clients": user_serializer.data,
            "lawyers": lawyer_serializer.data
        }

        return Response(combined_data, status=200)


# List and Create Users
class UserCreateView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, AdminRequiredPermission]

    def get_serializer_class(self):
        # Get `user_type` from URL parameters (kwargs)
        user_type = self.kwargs.get("user_type")
        if user_type == "lawyer":
            return LawyerSerializer
        elif user_type == "client":
            return UserSerializer
        else:
            # Raise an error if `user_type` is not valid
            raise serializers.ValidationError({"error": "Invalid user type specified in URL."})

    def create(self, request, *args, **kwargs):
        # Dynamically select serializer based on `user_type`
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)

        # Validate and save the data
        if serializer.is_valid():
            # Set the `office` based on the current user's office
            instance = serializer.save(office=request.user.office)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, Update, and Delete Users


class InvalidUserTypeException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid user type specified in URL."
    default_code = "invalid_user_type"


class UserDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, AdminRequiredPermission]

    def get_serializer_class(self):
        # Choose the appropriate serializer based on `user_type` from URL parameters
        user_type = self.kwargs.get("user_type")
        if user_type == "lawyer":
            return LawyerSerializer
        elif user_type == "client":
            return UserSerializer
        else:
           raise InvalidUserTypeException()

    def get_queryset(self):
        # Choose the appropriate queryset based on `user_type` from URL parameters
        user_type = self.kwargs.get("user_type")
        if user_type == "lawyer":
            return Lawyer.objects.filter(office=self.request.user.office)
        elif user_type == "client":
            return User.objects.filter(office=self.request.user.office)
        else:
            raise serializers.ValidationError({"error": "Invalid user type specified in URL."})


