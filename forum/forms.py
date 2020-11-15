from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import *

# also importing user defined django form model
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password1']


class QuestionCreateForm(ModelForm):
    class Meta:
        model = Question
        fields = ['category_id', 'question_text']


class AnswerCreateForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text']


class QuestionReportForm(ModelForm):
    class Meta:
        model = QuestionReport
        fields = ['report_text']


class AnswerReportForm(ModelForm):
    class Meta:
        model = AnswerReport
        fields = ['report_text']
