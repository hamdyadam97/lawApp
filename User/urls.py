from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('get-edit-destroy-profile/', views.AdminProfileView.as_view(), name='admin-profile'),
    path('create-profile/', views.AdminProfileCreate.as_view(), name='admin-profile-create'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('users/', views.GetAllUsersView.as_view(), name='user-create'),
]
