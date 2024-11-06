from django.shortcuts import render

# Create your views here.


# List and Create Invoices
class InvoiceListCreateView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, AdminRequiredPermission]
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        return Invoice.objects.filter(user__office=self.request.user.office)


# Retrieve, Update, and Delete Invoices
class InvoiceDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, AdminRequiredPermission]
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        return Invoice.objects.filter(user__office=self.request.user.office)





#
# # List and Create Legal Documents
# class LegalDocumentListCreateView(ListCreateAPIView):
#     permission_classes = [permissions.IsAuthenticated, AdminRequiredPermission]
#     serializer_class = LegalDocumentSerializer
#
#     def get_queryset(self):
#         return LegalDocument.objects.filter(admin=self.request.user)
#
#     def perform_create(self, serializer):
#         serializer.save(admin=self.request.user)
#
#
# # Retrieve, Update, and Delete Legal Documents
# class LegalDocumentDetailView(RetrieveUpdateDestroyAPIView):
#     permission_classes = [permissions.IsAuthenticated, AdminRequiredPermission]
#     serializer_class = LegalDocumentSerializer
#
#     def get_queryset(self):
#         return LegalDocument.objects.filter(admin=self.request.user)