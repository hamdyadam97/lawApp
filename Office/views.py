from django.shortcuts import render
from rest_framework import permissions
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView

from User.models import User, Lawyer
from User.permission import AdminRequiredPermission
from User.serializers import UserSerializer, LawyerSerializer


# Create your views here.




# Retrieve, Update, and Delete Users
class UserDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, AdminRequiredPermission]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(office=self.request.user.office)


# List and Create Lawyers
class LawyerListCreateView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, AdminRequiredPermission]
    queryset = Lawyer.objects.all()
    serializer_class = LawyerSerializer

    def get_queryset(self):
        return Lawyer.objects.filter(office=self.request.user.office)


# Retrieve, Update, and Delete Lawyers
class LawyerDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, AdminRequiredPermission]
    serializer_class = LawyerSerializer

    def get_queryset(self):
        return Lawyer.objects.filter(office=self.request.user.office)