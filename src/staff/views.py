from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.db import transaction

from src.staff.models import *
from src.staff.forms import *


# Create your views here.
def login_user(request):
    # logout(request)
    next_page = ''
    username = password = ''
    if 'next' in request.POST:
        next_page = request.POST['next']
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if next_page:
                    return redirect(next_page)
                return redirect('dashboard')
    return render(request, 'registration/login.html')


def profile(request):

    current_user = request.user
    user_data = User.objects.get(id=current_user.id)
    user_profile = UserProfile.objects.get(id=current_user.id)

    return render(
        request,
        "registration/profile.html",
        {"user_data": user_data, "user_profile": user_profile},
    )


def edit_profile(request):

    current_user = request.user
    user = User.objects.get(id=current_user.id)

    # prepopulate UserProfileForm with retrieved user values from above.
    user_form = UserProfileForm(instance=user)

    # The sorcery begins from here, see explanation below
    ProfileInlineFormset = inlineformset_factory(
        User, UserProfile, fields=("photo", "phone", "bio")
    )
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated and request.user.id == user.id:
        if request.method == "POST":
            user_form = UserProfileForm(
                request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(
                request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(
                    request.POST, request.FILES, instance=created_user
                )

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return redirect("profile")

        return render(
            request,
            "registration/edit_profile.html",
            {"noodle": user.id, "noodle_form": user_form,
                "formset": formset, "user": user},
        )
    else:
        raise PermissionDenied
