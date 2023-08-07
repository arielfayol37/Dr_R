from django.shortcuts import render
from phobos.models import Course, Professor
from deimos.models import Student, Enrollment
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
# Create your views here.
def index(request):
    return render(request, 'astros/index.html')

def login_view(request):
    return render(request, 'astros/login.html')

def register(request):
    return render(request, 'astros/register.html')

def all_courses(request):
    courses = Course.objects.all().order_by('-timestamp')
    # TODO: you may *need* to user request.user._wrapped instead
    try:
        professor = Professor.objects.get(pk=request.user.pk)
        is_professor_list = [1 if course.professors.filter(pk = request.user.pk).exists()\
                             else 0 for course in courses]
        context = {
            "courses__is_professor": zip(courses, is_professor_list),
            "is_professor": True,
            "is_student": False
        }
        return render(request, "astros/all_courses.html", context)
    except Professor.DoesNotExist:
        pass
    try:
        student = Student.objects.get(pk=request.user.pk)
        is_student_list = [1 if Enrollment.objects.filter(student=request.user, course=course).exists()\
                             else 0 for course in courses]
        context = {
            "courses__is_student": zip(courses, is_student_list),
            "is_professor": False,
            "is_student": True
        }
        return render(request, "astros/all_courses.html", context)
    
    except Student.DoesNotExist:
        pass
    return render(request, 'astros/all_courses.html', {"courses":courses})
    
