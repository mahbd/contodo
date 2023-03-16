from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

from .forms import UserRegisterForm, UserUpdateForm

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def update_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('main:home')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'registration/update_profile.html', {'form': form})
