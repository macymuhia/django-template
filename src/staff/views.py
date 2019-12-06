from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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


@login_required(login_url="/staff/")
def profile(request):

    current_user = request.user
    user_data = User.objects.get(id=current_user.id)
    user_profile = UserProfile.objects.get(id=current_user.id)

    return render(
        request,
        "registration/profile.html",
        {"user_data": user_data, "user_profile": user_profile},
    )


@login_required(login_url="/staff/")
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


def group_create_view(request):
    perms = Permission.objects.all()
    form = CustomGroupForm(request.POST)
    if form.is_valid():
        grp = form.cleaned_data['name']
        group, created = Group.objects.get_or_create(name=grp)
        if created:
            group.permissions.set(form.cleaned_data['permissions'])
        form = CustomGroupForm()
    context = {
        'form': form,
        'perms': perms,
    }
    return render(request, "groups/group_create.html", context)


def group_list_view(request):
    queryset = CustomGroup.objects.all()  # list of objects
    context = {
        "object_list": queryset
    }
    return render(request, "groups/group_list.html", context)


@transaction.atomic
def add_user_view(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, initial={
                             "password1": "Manor123", "password2": "Manor123"})
        details_form = UserDetailsForm(request.POST)
        if user_form.is_valid() and details_form.is_valid():
            user = user_form.save()
            user.profile.bio = details_form.cleaned_data.get('bio')
            group = details_form.cleaned_data.get('group')
            department = details_form.cleaned_data.get('department')
            user.profile.group.add(group[0].pk)
            dept = Department.objects.get(pk=department.pk)
            user.profile.department = dept
            user.profile.role = details_form.cleaned_data.get('role')
            user.profile.save()

            return redirect("list_users")
        else:
            # return redirect('add_user')
            user_form = UserForm()
            # return render(request, 'registration/add_user.html', {'user_form': user_form, 'details_form': details_form})
    else:
        user_form = UserForm()
        details_form = UserDetailsForm()
    return render(request, 'registration/add_user.html', {
        'user_form': user_form,
        'details_form': details_form
    })


def users_list_view(request):
    users = User.objects.all()
    return render(request, 'registration/users_list.html', {"users": users})


def set_password_view(request):
    current_user = request.user
    user = User.objects.get(id=current_user.id)
    form = UserSetPasswordForm(request.POST, instance=user)
    print(form.data)
    print(form.fields)
    if request.method == "POST":

        if form.is_valid():
            print("valid")
            password = form.cleaned_data['password2']
            form.save()
            return redirect("edit_profile")

    return render(request, 'registration/password_set_form.html', {'user': user, 'form': form})
