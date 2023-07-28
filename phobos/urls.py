from django.urls import path
from . import views

app_name = 'phobos'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('create_course', views.create_course, name='create_course'),
    path('create_question/<int:assignment_id>', views.create_question, name='create_question'),
    path('courses/<int:course_id>', views.course_management, name='course_management'),
    path('courses/<int:course_id>/create_assignment',\
         views.create_assignment, name='create_assignment'),
    path('courses/create_assignment',\
    views.create_assignment, name='create_assignment'),
    path('courses/<int:course_id>/assignments/<int:assignment_id>', \
         views.assignment_management, name='assignment_management'),
    path('create_question/get_subtopics/<str:selected_topic>', views.get_subtopics, name='get_subtopics')
   
]