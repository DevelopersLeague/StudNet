from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages  # for flash messages
from .models import *
from .forms import CreateUserForm
# for restricting users without login
from django.contrib.auth.decorators import login_required

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
                messages.success(request, 'Account was created for '+user_msg)

                # redirecting user after successful login
                # you can also place landingPage here
                return redirect('login')

        context = {'form': form}
        return render(request, 'forum/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
        # return redirect('forum/1')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            # request.POST.get('yearOfAdmission')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                # landingpage should come here DOUBTFULL, earlier it was home
                return redirect('home')
                # return redirect('forum/1')
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
    # return render(request, 'forum/main.html', {})
    return redirect("forum", page=1)


@login_required(login_url='login')
def forum(request, page):
    questions = Question.objects.all().order_by('-created_on')
    min_index = (page-1)*10
    max_index = min((page*10)-1, len(questions)-1)
    if len(questions) % 10 == 0:
        max_page = len(questions)//10
    else:
        max_page = len(questions)//10 + 1
    context = {'questions': questions[min_index:max_index+1],
               'next_page': min(page+1, max_page),
               'previous_page': max(page-1, 1)
               }
    print(max_page)
    return render(request, 'forum/forum.html', context)


@login_required(login_url='login')
def question_display(request, id):
    question = Question.objects.get(id=id)
    answers = question.answer_set.all()
    context = {'question': question, 'answers': answers}
    return render(request, 'forum/question_display.html', context)


def landingPage(request):
    return render(request, 'forum/landingPage.html', {})
