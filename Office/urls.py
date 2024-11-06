from django.urls import path
from . import views

app_name = 'office'

urlpatterns = [
    path('requests/', views.RequestListCreateView.as_view(), name='request-list-create'),
    # path('requests/<int:pk>/', views.RequestDetailView.as_view(), name='request-detail'),
    # path('cases/', views.CaseListCreateView.as_view(), name='case-list-create'),
    # path('cases/<int:pk>/', views.CaseDetailView.as_view(), name='case-detail'),
    # path('notifications/', views.NotificationListCreateView.as_view(), name='notification-list-create'),
    # path('notifications/<int:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),
    # path('invoices/', views.InvoiceListCreateView.as_view(), name='invoice-list-create'),
    # path('invoices/<int:pk>/', views.InvoiceDetailView.as_view(), name='invoice-detail'),
    # path('legal-documents/', views.LegalDocumentListCreateView.as_view(), name='legal-doc-list-create'),
    # path('legal-documents/<int:pk>/', views.LegalDocumentDetailView.as_view(), name='legal-doc-detail'),
]
