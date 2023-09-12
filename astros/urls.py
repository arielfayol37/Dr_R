from django.urls import path
from . import views

app_name = 'astros'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    #path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('all_courses', views.all_courses, name="all_courses"),
    path('Validate_enrollment_code/<int:course_id>/<int:code>',views.validate_code, name='validate_code')
]