from django.urls import path
from . import views

app_name = 'phobos'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('create_course', views.create_course, name='create_course'),
    path('create_question', views.create_question, name='create_question'),
   
]