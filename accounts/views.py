from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

from .forms import RegisterForm


def register(request):
    if request.method == "POST":
        print("POST received")

        form = RegisterForm(request.POST)

        if form.is_valid():
            print("Form Valid")

            user = form.save()
            login(request, user)

            print("User Saved:", user.username)

            messages.success(request, "Registration Successful!")
            return redirect("home")

        else:
            print(form.errors)

    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        print("Username =", username)

        user = authenticate(
            request,
            username=username,
            password=password
        )

        print("Authenticated User =", user)

        if user is not None:

            # =========================
            # BLOCK ADMIN FROM WEBSITE
            # =========================

            if user.is_staff:
                messages.error(
                    request,
                    "Admin account cannot login to website."
                )
                return redirect("login")

            # =========================
            # NORMAL USER LOGIN
            # =========================

            login(request, user)

            messages.success(
                request,
                "Login Successful!"
            )

            return redirect("home")

        else:
            print("Login Failed")

            messages.error(
                request,
                "Invalid Username or Password"
            )

    return render(request, "accounts/login.html")


def user_logout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect("home")