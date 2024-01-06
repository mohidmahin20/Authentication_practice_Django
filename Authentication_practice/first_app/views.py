from django.shortcuts import render, redirect
from . import forms
from django.contrib import messages
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    SetPasswordForm,
)
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, "home.html")


def user_register(request):
    if request.method == "POST":
        register_form = forms.RegistrationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, "Account Created Successfully")
            return redirect("login")
    else:
        register_form = forms.RegistrationForm()
        return render(
            request, "register.html", {"form": register_form, "type": "Sign Up"}
        )


def user_login(request):
    if request.method == "POST":
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            user_name = login_form.cleaned_data["username"]
            user_pass = login_form.cleaned_data["password"]
            user = authenticate(username=user_name, password=user_pass)
            if user is not None:
                messages.success(request, "User Logged In Successfully")
                login(request, user)
                return redirect("profile")
            else:
                messages.warning(request, "Login info is not correct")
                return redirect("login")
    else:
        login_form = AuthenticationForm()
        return render(request, "register.html", {"form": login_form, "type": "Log In"})


@login_required
def profile(request):
    return render(request, "profile.html")


@login_required
def pass_change(request):
    if request.method == "POST":
        pass_form = PasswordChangeForm(request.user, data=request.POST)
        if pass_form.is_valid():
            pass_form.save()
            messages.success(request, "Password Changed Successfully")
            update_session_auth_hash(request, pass_form.user)
            return redirect("profile")
    else:
        pass_form = PasswordChangeForm(user=request.user)
        return render(
            request, "register.html", {"form": pass_form, "type": "Change Password"}
        )


@login_required
def pass_change2(request):
    if request.method == "POST":
        pass_form = SetPasswordForm(request.user, data=request.POST)
        if pass_form.is_valid():
            pass_form.save()
            messages.success(request, "Password Changed Successfully")
            update_session_auth_hash(request, pass_form.user)
            return redirect("profile")
    else:
        pass_form = SetPasswordForm(user=request.user)
        return render(
            request, "register.html", {"form": pass_form, "type": "Change Password"}
        )


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect("home")