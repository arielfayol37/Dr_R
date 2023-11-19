from django.urls import path
from . import views

app_name = 'phobos'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
     #
     path('forgot_password', views.forgot_password, name='forgot_password'),
     #
    path('create_course', views.create_course, name='create_course'),
    path('create_question/<int:assignment_id>', views.create_question, name='create_question'),
    path('create_question/<int:assignment_id>/<str:question_nums_types>',views.create_question,
         name='create_question'
    ),
    path('edit_question/<int:question_id>',views.edit_question,
         name='edit_question'
    ),
    path('question_bank', views.question_bank, name='question_bank'),
    path('courses/<int:course_id>', views.course_management, name='course_management'),
    path('courses/<int:course_id>/create_assignment',\
         views.create_assignment, name='create_assignment'),
    path('courses/create_assignment',\
    views.create_assignment, name='create_assignment'),
    path('courses/<int:course_id>/assignments/<int:assignment_id>', \
         views.assignment_management, name='assignment_management'),
    path('courses/<int:course_id>/assignments/<int:assignment_id>/assign', \
         views.assign_assignment, name='assign_assignment'),    
    path('create_question/get_subtopics/<str:selected_topic>', views.get_subtopics, name='get_subtopics'),
    path('courses/<int:course_id>/assignments/<int:assignment_id>/<int:question_id>',
         views.question_view, name='question_view'),
       
     path('courses/<int:course_id>/assignments/<int:assignment_id>/<int:question_id>/export_question_to/<int:exp_assignment_id>',
          views.export_question_to, name='export_question'),

     path('calci', views.calci, name='calci'),
     path('courses/<int:course_id>/gradebook', views.gradebook, name='gradebook'),
     path('courses/<int:course_id>/<int:student_id>/student_profile', views.student_profile, name='student_profile'),
     #####
     path('courses/<int:course_id>/<int:student_id>/student_profile/modify_question_student_score/<str:new_score>/<str:question_student_id>', \
          views.modify_question_student_score, name='modify_question_score'),
     ######
     path('courses/<int:course_id>/gradebook/student_search',views.student_search, name="student_search"),
     path('courses/<int:course_id>/<int:student_id>/get_questions/<int:assignment_id>',
          views.get_questions,name='get_questions'),
     path('search_question/', views.search_question, name='search_question'),
     path('sidebar/', views.sidebar, name='sidebar'),

     path('courses/<int:course_id>/enrollment_code/<str:expiring_date>',views.enrollmentCode, name = 'enrollment_code'),
     path('courses/<int:course_id>/display_enrollment_codes',views.display_codes, name='display_codes'),
     path('courses/<int:course_id>/manage_enrollment_codes', views.manage_enrollment_codes, name='manage_enrollment_codes'),
     path('courses/<int:course_id>/manage_course_info', views.manage_course_info, name='manage_course_info'),
     path('courses/<int:course_id>/save_course_info', views.save_course_info, name='save_course_info'),

     path('courses/<int:course_id>/assignments/<int:assignment_id>/<str:new_date>/edit_assignment_due_date', \
         views.edit_assignment_due_date, name='assignment_due_date'),
     path('courses/<int:course_id>/student_profile/<int:assignment_id>/edit_student_assignment_due_date', \
         views.edit_student_assignment_due_date, name='assignmentstudent_due_date'),
     path('courses/<int:course_id>/<int:student_id>/student_profile/<int:assignment_id>/edit_student_assignment_due_date', \
         views.edit_student_assignment_due_date, name='assignmentstudent_due_date'),   
     path('courses/edit_course_cover', views.edit_course_cover, name='edit_course_cover'),
     path('courses/<int:course_id>/edit_course_cover_page', views.edit_course_cover_page, name='edit_course_cover_page'),

     path('courses/<int:course_id>/assignments/<int:assignment_id>/edit_grading_scheme', \
         views.edit_grading_scheme, name='edit_grading_scheme'),

    
]