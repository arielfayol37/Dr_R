from django.urls import path
from . import views

app_name = 'astros'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    #path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('all_courses', views.all_courses, name="all_courses"),
     path('course_info/<int:course_id>', views.course_info, name="course_info"),
    path('course_info/course_enroll/<int:course_id>/<int:code>',views.course_enroll, name='course_enroll'),

]