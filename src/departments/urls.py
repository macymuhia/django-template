from django.urls import path
from django.conf import settings
from . import views


urlpatterns = [
    path("", views.department_list_view, name='department_list'),
    path('create/', views.department_create_view,
         name='department_create'),
    path('search/', views.search, name='search'),

]
