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
    path('courses/<int:course_id>/assignments/<int:assignment_id>/questions/<int:question_id>',\
         views.answer_question, name='answer_question'),
    path('courses/<int:course_id>/assignments/<int:assignment_id>/questions/<int:landed_question_id>/validate_answer/<int:question_id>',\
         views.validate_answer, name='validate_answer'),
    path('question_nav', views.question_nav, name='question_nav'),
    path('action_menu', views.action_menu, name='action_menu'),
    path('search_question/', views.search_question, name='search_question'),
    path('compare_expressions', views.expression_compare_test, name='compare_expressions'),
    path('courses/<int:course_id>/assignments/<int:assignment_id>/questions/<int:question_id>/save_note',\
         views.save_note, name='save_note'), 
]