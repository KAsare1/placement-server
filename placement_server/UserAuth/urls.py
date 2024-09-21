from django.urls import path
from .views import ConfirmEmailView, ConfirmRegistrationView, ForgotPasswordView, LoginView, ResendConfirmationCodeView, ResetPasswordView, StudentDetailView, StudentRegistrationView, UserDetailView, UserListView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('student/<str:student_id>/', StudentDetailView.as_view(), name='student-detail'),
    path('register/', StudentRegistrationView.as_view(), name='student-register'),
    path('confirm/', ConfirmRegistrationView.as_view(), name='confirm-registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('resend-confirmation/', ResendConfirmationCodeView.as_view(), name='resend-confirmation'),
]
