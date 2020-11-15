from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.registerPage, name="register"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path('', views.landingPage, name='landingPage'),
    path('home/', views.home, name='home'),
    # forum links
    path('forum/<int:page>/', views.forum, name='forum'),
    # question crud
    path('forum/question/create', views.question_create, name='question_create'),
    path('forum/question/<int:id>/',
         views.question_display, name='question_display'),
    path('forum/question/update/<int:id>/',
         views.question_update, name='question_update'),
    path('forum/question/delete/<int:id>/',
         views.question_delete, name='question_delete'),
    # answer crud
    path('forum/answer/create/<int:question_id>',
         views.answer_create, name='answer_create'),
    path('forum/answer/update/<int:answer_id>',
         views.answer_update, name='answer_update'),
    path('forum/answer/delete/<int:answer_id>',
         views.answer_delete, name='answer_delete'),
    # updates
    path('updates/', views.updates, name="updates"),
    # reports
    path('forum/question/report/<int:id>/',
         views.question_report, name="question_report"),
    path('forum/answer/report/<int:id>/',
         views.answer_report, name="answer_report")

]
