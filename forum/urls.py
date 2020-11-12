from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.registerPage, name="register"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path('', views.landingPage, name='landingPage'),
    path('home/', views.home, name='home'),
    path('forum/<int:page>/', views.forum, name='forum'),
    path('question/<int:id>/', views.question_display, name='question_display')

]
