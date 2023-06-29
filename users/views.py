from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from products.models import Basket
from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm, UsersProfileForm
from django.contrib import auth

# Create your views here.
def login(request):
    if request.method=='POST':
        form=UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request,user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'form' : form}
    return render(request,'users/login.html',context)
def registration(request):
    if request.method=='POST':
        form=UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:login'))
    form=UserRegistrationForm()
    context={'form':form}
    return render(request,'users/register.html', context)

def profile(request):
    if request.method=='POST':
        form=UsersProfileForm(instance=request.user,data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            print(form.errors)
    else:
        form=UsersProfileForm(instance=request.user)
    context = {'title': 'Профиль','form':form, 'baskets': Basket.objects.filter(user=request.user)}
    return render(request,'users/profile.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))