from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages # for flash messages 
from .models import *
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required   # for restricting users without login 

# Create your views here.

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user_msg = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for '+user_msg )

                # redirecting user after successful login
                return redirect('login')   # you can also place landingPage here  

        context = {'form':form}
        return render(request, 'forum/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            # request.POST.get('yearOfAdmission')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')    # landingpage should come here DOUBTFULL, earlier it was home
            else:
                messages.info(request, 'Username OR Password is incorrect')

        context = {}
        return render(request, 'forum/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('landingPage')

# @login_required(login_url='landing')
# put the below line above every view that you want to restrict if the user hasn't loggedin
# these are nothing but login decorators
@login_required(login_url='login')
def home(request):
    # context = {}
	return render(request, 'forum/main.html', {})


def landingPage(request):
    return render(request, 'forum/landingPage.html', {})

