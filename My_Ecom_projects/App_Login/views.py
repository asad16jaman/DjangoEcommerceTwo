from django.shortcuts import render, HttpResponseRedirect, HttpResponse,redirect
from django.urls import reverse

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .models import Profile

from .forms import Profileform, SingUpForm
from django.contrib import messages


# Create your views here.

def sign_up(request):
    form = SingUpForm()
    if request.method == 'POST':
        form = SingUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'successfully registerd.....')
            return HttpResponseRedirect(reverse('app_login:login'))
    return render(request, 'App_Login/signup.html', context={'form': form})


def login_user(request):
    if request.method=='GET':
        form = AuthenticationForm()
        return render(request, 'App_Login/login.html', context={"form": form})
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, 'you are successfully login')
            return HttpResponseRedirect(reverse('app_shop:home'))
        else:
            return render(request, 'App_Login/login.html', context={"form": form})



@login_required()
def logout_user(request):
    logout(request)
    messages.warning(request, 'logout successfully')
    return HttpResponseRedirect(reverse('app_login:login'))


@login_required()
def create_Profile(request):
    profile = Profile.objects.get(user=request.user)
    form = Profileform(instance=profile)
    if request.method == 'POST':
        form = Profileform(data=request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'successfully created profile')
            return HttpResponseRedirect(reverse('app_login:login'))
    return render(request, 'App_Login/change_profile.html', context={'form': form})

