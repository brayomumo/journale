from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from rest_framework import viewsets
from journale.wenyeji.forms import NewUserForm

from journale.wenyeji.models import User
from journale.wenyeji.serializers import UserSerializer


def user_register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(
        request=request,
        template_name="users/register.html",
        context={"register_form": form},
    )


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(
        request=request, template_name="users/login.html", context={"login_form": form}
    )


def user_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")


# API VIEWS
class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
