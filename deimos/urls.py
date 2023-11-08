from django.urls import path
from . import views

app_name = 'deimos'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
     path('forgot_password', views.forgot_password, name='forgot_password'),
     path('courses/notes/<int:course_id>', views.note_management, name='note_management'),
     path('courses/<int:student_id>/gradebook/<int:assignment_id>/assignment_grades', views.assignment_gradebook_student, name='assignment_gradebook_student'),
    path('courses/<int:course_id>', views.course_management, name='course_management'),
    path('courses/<int:course_id>/assignments/<int:assignment_id>', \
         views.assignment_management, name='assignment_management'),
    path('courses/<int:course_id>/assignments/<int:assignment_id>/questions/<int:question_id>',\
         views.answer_question, name='answer_question'),
    path('courses/<int:course_id>/assignments/<int:assignment_id>/questions/<int:question_id>/<int:student_id>/<int:upload_note_img>',\
         views.answer_question, name='answer_question'),
    path('courses/<int:course_id>/assignments/<int:assignment_id>/questions/<int:landed_question_id>/validate_answer/<int:question_id>',\
         views.validate_answer, name='validate_answer'),
     path('courses/<int:course_id>/assignments/<int:assignment_id>/questions/<int:landed_question_id>/<int:student_id>/<int:upload_note_img>/validate_answer/<int:question_id>',\
         views.validate_answer, name='validate_answer'),
     path('courses/<int:course_id>/assignments/<int:assignment_id>/questions/<int:question_id>/generate_note_qr',\
         views.generate_note_qr, name='generate_note_qr'),
     path('courses/<int:course_id>/assignments/<int:assignment_id>/questions/<int:question_id>/<int:student_id>/<int:upload_note_img>/generate_note_qr',\
         views.generate_note_qr, name='generate_note_qr'),
    path('question_nav', views.question_nav, name='question_nav'),
    path('action_menu', views.action_menu, name='action_menu'),
    path('search_question/', views.search_question, name='search_question'),
    path('compare_expressions', views.expression_compare_test, name='compare_expressions'),
    path('courses/<int:course_id>/assignments/<int:assignment_id>/questions/<int:question_id>/save_note',\
         views.save_note, name='save_note'), 
   path('courses/<int:course_id>/assignments/<int:assignment_id>/questions/<int:question_id>/<int:student_id>/<int:upload_note_img>/save_note',\
         views.save_note, name='save_note'), 
    path('courses/generate_practice_test', views.generate_practice_test, name='generate_practice_test'),
    path('courses/practice_test_settings/<int:course_id>', views.practice_test_settings, name='practice_test_settings'),
    path('courses/<int:course_id>/gradebook', views.gradebook, name='gradebook')    
]