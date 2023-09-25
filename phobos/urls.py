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
    path('create_question/<int:assignment_id>/<int:type_int>',views.create_question,
         name='create_question'
    ),
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
         ## for export question implementation
     path('courses/<int:course_id>/assignments/<int:assignment_id>/<int:question_id>/export_question_to/<int:exp_assignment_id>',
          views.export_question_to, name='export_question'),
     #path('courses/<int:course_id>/assignments/<int:assignment_id>/<int:question_id>/get_assignments/<int:exp_course_id>', \
     #   views.get_assignments, name='get_assignments'),
          ##
     path('calci', views.calci, name='calci'),
     path('create_question/upload-image/', views.upload_image, name='upload_image'),
     path('courses/<int:course_id>/gradebook', views.gradebook, name='gradebook'),
     path('courses/<int:course_id>/<int:student_id>/student_profile', views.student_profile, name='student_profile'),
     path('courses/<int:course_id>/gradebook/student_search',views.student_search, name="student_search"),
     path('courses/<int:course_id>/<int:student_id>/get_questions/<int:assignment_id>',
          views.get_questions,name='get_questions'),
     path('search_question/', views.search_question, name='search_question'),
     path('sidebar/', views.sidebar, name='sidebar'),

     path('courses/<int:course_id>/enrollment_code/<str:expiring_date>',views.enrollmentCode, name = 'enrollment_code'),
     path('courses/<int:course_id>/display_enrollment_codes',views.display_codes, name='display_codes'),
     path('courses/<int:course_id>/manage_enrollment_codes', views.manage_enrollment_codes, name='manage_enrollment_codes'),
     path('courses/<int:course_id>/manage_course_info', views.manage_course_info, name='manage_course_info'),
     path('courses/<int:course_id>/<str:categori>/save_course_info', views.save_course_info, name='save_course_info'),

         path('courses/<int:course_id>/assignments/<int:assignment_id>/<str:new_date>/edit_assignment_due_date', \
         views.edit_assignment_due_date, name='assignment_due_date'),
          path('courses/<int:course_id>/<int:student_id>/student_profile/<int:assignment_id>/<str:new_date>/edit_student_assignment_due_date', \
         views.edit_student_assignment_due_date, name='assignmentstudent_due_date'),
    
]