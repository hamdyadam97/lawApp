
from rest_framework.generics import  ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from Office.models import Request
from Office.serializers import RequestSerializer

from User.permission import AdminRequiredPermission




class RequestListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, AdminRequiredPermission]
    serializer_class = RequestSerializer

    def get_queryset(self):
        # Filter requests by the current admin's office
        return Request.objects.filter(office_id=self.request.user.office_id)