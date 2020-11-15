from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages  # for flash messages
from .models import *
from .filters import *
# from .forms import CreateUserForm
from .forms import *


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


def landingPage(request):
    if request.user.is_authenticated:
        return redirect("forum", page=1)
    return render(request, 'forum/landingPage.html', {})

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
    # for searching
    question_filter = QuestionFilter(request.GET, queryset=questions)
    questions = question_filter.qs

    min_index = (page-1)*10
    max_index = min((page*10)-1, len(questions)-1)
    if len(questions) % 10 == 0:
        max_page = len(questions)//10
    else:
        max_page = len(questions)//10 + 1
    # if no questions
    if len(questions) == 0:
        min_index = 0
        max_index = 0
        max_page = 1
    context = {'questions': questions[min_index:max_index+1],
               'next_page': min(page+1, max_page),
               'previous_page': max(page-1, 1),
               'question_filter': question_filter
               }
    return render(request, 'forum/forum.html', context)

#
# question crud ----------------------------------------------------------------
#


@login_required(login_url='login')
def question_create(request):
    form = QuestionCreateForm()
    # if post
    if request.method == 'POST':
        form = QuestionCreateForm(request.POST)
        if form.is_valid():
            # filling the automatic fields
            question = form.save(commit=False)
            question.user_id = request.user
            question.save()
            # redirect to forum home
            return redirect("forum", page=1)
        else:
            print("form not valid")
    # if get
    context = {'form': form}
    return render(request, 'forum/question_create.html', context)


@login_required(login_url='login')
def question_display(request, id):
    question = Question.objects.get(id=id)
    author = question.user_id
    current_user = request.user
    answers = question.answer_set.all().order_by('-created_on')
    # answer_authors = []
    # for answer in answers:
    #     answer_authors.append(answer.user_id)
    context = {
        'question': question,
        'answers': answers,
        'author': author,
        # 'answer_authors': answer_authors,
        'current_user': current_user
    }
    return render(request, 'forum/question_display.html', context)


@login_required(login_url='login')
def question_update(request, id):
    question = Question.objects.get(id=id)
    # redirect if question is not owned by the current user
    if(request.user != question.user_id):
        return redirect("question_display", id=id)
    form = QuestionCreateForm(instance=question)
    if request.method == 'POST':
        form = QuestionCreateForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            # redirect to question page
            return redirect("question_display", id=id)
    context = {'form': form}
    return render(request, 'forum/question_create.html', context)


@login_required(login_url='login')
def question_delete(request, id):
    if request.method == 'POST':
        question = Question.objects.get(id=id)
        if(request.user != question.user_id):
            return redirect("question_display", id=id)
        question.delete()
        return redirect('forum', page=1)
    else:
        raise Http404("page not found")


# answer crud ------------------------------------------------------------------

@login_required(login_url='login')
def answer_create(request, question_id):
    question = Question.objects.get(id=question_id)
    # print(question)
    form = AnswerCreateForm()
    # if post
    if request.method == 'POST':
        form = AnswerCreateForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user_id = request.user
            answer.question_id = question
            form.save()
            # redirect to forum home
            return redirect("question_display", id=question_id)
        else:
            print("form not valid")
    # if get
    context = {'form': form}
    return render(request, 'forum/answer_create.html', context)


@login_required(login_url='login')
def answer_update(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    if(request.user != answer.user_id):
        return redirect("question_display", answer_id=answer.question_id)
    form = AnswerCreateForm(instance=answer)
    if request.method == 'POST':
        form = AnswerCreateForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            # redirect to question page
            return redirect("question_display", id=answer.question_id.id)
    context = {'form': form}
    return render(request, 'forum/answer_create.html', context)


@login_required(login_url='login')
def answer_delete(request, answer_id):
    if request.method == 'POST':
        answer = Answer.objects.get(id=answer_id)
        current_question_id = answer.question_id.id
        if(request.user != answer.user_id):
            return redirect("question_display", id=current_question_id)
        answer.delete()
        return redirect('question_display', id=current_question_id)
    else:
        print("invalid access")
        raise Http404("page not found")

# updates ----------------------------------------------------------------------


@login_required(login_url='login')
def updates(request):
    updates = Update.objects.all().order_by('-created_on')
    context = {'updates': updates}
    return render(request, 'forum/updates.html', context)

# reports --------------------------------------------------------------------


@login_required(login_url='login')
def question_report(request, id):
    question = Question.objects.get(id=id)
    form = QuestionReportForm()
    errors = list()
    threshold = 1
    # check of a report already filed by the same user for the same question
    prev_report = QuestionReport.objects.filter(
        question_id=question.id, user_id=request.user.id)
    # if already done
    if len(prev_report) >= 1:
        errors.append("question already reported")
        return redirect("question_display", id=question.id)
    # else (new report)
    elif request.method == "POST":
        # create a new report
        form = QuestionReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user_id = request.user
            report.question_id = question
            report.save()
        # check if the question needs to be flagged
        total_reports = QuestionReport.objects.filter(question_id=question.id)
        if len(total_reports) >= threshold:
            flagged_question = flaggedQuestion()
            flagged_question.question_id = question
            flagged_question.save()
            return redirect("question_display", id=question.id)
    context = {'form': form, 'errors': errors}
    return render(request, "forum/question_report.html", context)


@login_required(login_url='login')
def answer_report(request, id):
    answer = Answer.objects.get(id=id)
    form = AnswerReportForm()
    errors = list()
    threshold = 1
    # check of a report already filed by the same user for the same question
    prev_report = AnswerReport.objects.filter(
        answer_id=answer.id, user_id=request.user.id)
    # if already done
    if len(prev_report) >= 1:
        errors.append("question already reported")
        return redirect("question_display", id=answer.question_id.id)
    # else (new report)
    elif request.method == "POST":
        # file a new report
        form = AnswerReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user_id = request.user
            report.answer_id = answer
            report.save()
        # check if the question needs to be flagged
        total_reports = AnswerReport.objects.filter(answer_id=answer.id)
        if len(total_reports) == threshold:
            flagged_answer = flaggedAnswer()
            flagged_answer.answer_id = answer
            flagged_answer.save()
            return redirect("question_display", id=answer.question_id.id)
    context = {'form': form, 'errors': errors}
    return render(request, "forum/answer_report.html", context)

# profile ---------------------------------------------------------------------
@login_required(login_url='login')
def profile(request):
    questions = Question.objects.filter(user_id = request.user.id).order_by('-created_on')
    answers = Answer.objects.filter(user_id = request.user.id).order_by('-created_on')
    context = {'questions':questions, 'answers':answers}
    return render(request,"forum/profile.html",context)