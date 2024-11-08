from rest_framework.exceptions import NotFound
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from Office.models import Request, LegalDocument
from Office.serializers import RequestSerializer, LegalDocumentSerializer

from User.permission import AdminRequiredPermission


class RequestListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, AdminRequiredPermission]
    serializer_class = RequestSerializer

    def get_queryset(self):
        # Filter requests by the current admin's office
        return Request.objects.filter(office_id=self.request.user.office_id)


class RequestDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated, AdminRequiredPermission]  # Only authenticated admins can access

    def get_object(self):
        request_id = self.kwargs.get("request_id")
        try:
            req = Request.objects.get(id=request_id)
            if req.office_id != self.request.user.office_id:  # Check that office matches
                raise NotFound("Request not found")
            return req
        except Request.DoesNotExist:
            raise NotFound("Request not found")


class LegalDocumentListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, AdminRequiredPermission]
    serializer_class = LegalDocumentSerializer

    def get_queryset(self):
        # Only retrieve documents belonging to the current admin user
        return LegalDocument.objects.filter(admin_id=self.request.user.id)

    def perform_create(self, serializer):
        # Save with the current admin user as the owner
        serializer.save(admin_id=self.request.user.id)