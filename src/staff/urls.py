from django.urls import path, include, re_path
from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView, SetPasswordForm
from django.conf import settings
from src.staff import views

urlpatterns = [
    path("", views.login_user, name="login",),
    path("logout/", LogoutView.as_view(),
         {"next_page": settings.LOGOUT_REDIRECT_URL}, name="logout",),
    path('profile/', views.profile, name="profile"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('group_create/', views.group_create_view, name='create_group'),
    path('group_list/', views.group_list_view, name='group_list'),
    path('add_user/', views.add_user_view, name='add_user'),
    path('users_list/', views.users_list_view, name='list_users'),
    path("reset/", views.set_password_view, name="reset"),


]
