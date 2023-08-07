from django.urls import path
from . import views

app_name = 'deimos'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('courses/<int:course_id>', views.course_management, name='course_management'),
    path('courses/<int:course_id>/assignments/<int:assignment_id>', \
         views.assignment_management, name='assignment_management'),
    path('courses/enroll/<int:course_id>', views.course_enroll, name='course_enroll'),

    path('courses/<int:course_id>/assignments/<int:assignment_id>/questions/<int:question_id>',\
         views.answer_question, name='answer_question'),
    path('question_nav', views.question_nav, name='question_nav')
]