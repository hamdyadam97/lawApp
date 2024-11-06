from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('get-edit-destroy-profile/', views.AdminProfileView.as_view(), name='admin-profile'),
    path('create-profile-admin/', views.AdminProfileCreate.as_view(), name='admin-profile-create'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('users/', views.GetAllUsersView.as_view(), name='user-create'),
    path('create-user/<str:user_type>/', views.UserCreateView.as_view(), name='user-create'),
    path('users/<str:user_type>/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
]
