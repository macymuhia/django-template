from django.urls import path, include, re_path
from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView, SetPasswordForm
from django.conf import settings
from src.patients import views

urlpatterns = [
    path("add_patient", views.add_patient, name="add_patient",),
]
