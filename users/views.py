from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get("username")
            messages.success(
                request,
                f"Your account has been created. You are logged in.",
            )
            new_user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
            )
            login(request, new_user)
            return redirect("/")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(
                request,
                f"Your account has been updated!",
            )
            return redirect("profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
    context = {"user_form": user_form}
    return render(request, "users/profile.html", context=context)
