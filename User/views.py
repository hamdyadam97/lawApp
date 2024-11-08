from django.shortcuts import render
from rest_framework import permissions, status, serializers
from rest_framework.exceptions import NotFound, APIException
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from User.models import User
from User.permission import AdminRequiredPermission
from User.serializers import UserProfileSerializer, UserSerializer, LawyerSerializer, LoginSerializer


# Create your views here.
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class AdminProfileCreate(CreateAPIView):
    serializer_class = UserProfileSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '')
        if User.objects.filter(email__iexact=email).exists():
            return Response({'detail': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        return self.create(request, *args, **kwargs)

# Admin Profile View (Retrieve and Update Admin)
class AdminProfileView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, AdminRequiredPermission]
    serializer_class = UserProfileSerializer

    def get_object(self):
        # If the user is an admin, the object is the admin's profile (request.user)
        user_id = self.request.query_params.get('id')
        if self.request.user.user_type == 'admin' and not user_id :
            return self.request.user

        # If it's a user or a lawyer, we need to fetch the object based on the provided ID

        if not user_id:

            raise NotFound('User ID must be provided for user/lawyer.')
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise NotFound('User not found.')


class GetAllUsersView(APIView):
    permission_classes = [permissions.IsAuthenticated, AdminRequiredPermission]

    def get(self, request, *args, **kwargs):
        # Assume the current user is an Admin with an associated office
        office_id = request.user.office_id

        # Query both User and Lawyer models filtered by office
        users = User.objects.filter(office_id=office_id)
        clients = users.filter(user_type='user')
        lawyers = users.filter(user_type='lawyer')

        # Combine users and lawyers into one list and serialize
        user_serializer = UserProfileSerializer(users, many=True)
        lawyer_serializer = UserProfileSerializer(lawyers, many=True)
        combined_data = {
            "users": user_serializer.data,
            "lawyers": lawyer_serializer.data
        }

        return Response(combined_data, status=200)





class InvalidUserTypeException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid user type specified in URL."
    default_code = "invalid_user_type"




