from django.shortcuts import render, redirect
from phobos.models import Course, Professor,EnrollmentCode,CourseInfo
from deimos.models import Student, Enrollment
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from datetime import date
import json
from django.shortcuts import get_object_or_404
from django.contrib import messages
from deimos.models import QuestionStudent, AssignmentStudent
from django.urls import reverse
from markdown2 import markdown

# Create your views here.
def index(request):
    return render(request, 'astros/index.html')

def login_view(request):
    return render(request, 'astros/login.html')

def register(request):
    return render(request, 'astros/register.html')

def all_courses(request):
    
    # TODO: you may *need* to user request.user._wrapped instead
    try:
        courses = Course.objects.all().order_by('-timestamp')
        professor = Professor.objects.get(pk=request.user.pk)
        is_professor_list = [1 if course.professors.filter(pk = request.user.pk).exists() or course.name=='Question Bank'\
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
        courses = Course.objects.exclude(name='Question Bank').order_by('-timestamp')
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

@login_required(login_url='astros:login')
def course_enroll(request, course_id, code):
    # Making sure the request is done by a Student.
    student = get_object_or_404(Student, pk=request.user.pk)
    course = get_object_or_404(Course, pk = course_id)
    if not Enrollment.objects.filter(student=student, course=course).exists():
        # Checking whether code is valid.
        try:
            code = EnrollmentCode.objects.get(course=course, code=code)
        except:
            return HttpResponse(json.dumps({'state':False,'response':'Invalid code'}))
        if code.expiring_date >= date.today():
            # If not enrolled, create a new Enrollment instance
            enrollment = Enrollment.objects.create(student=student, course=course)
            messages.info(request, message="You were successfully enrolled")
            # Now assign all the courses assignments to the student. 
            for assignment in course.assignments.all():
                assign = AssignmentStudent.objects.create(assignment=assignment, student=student)
                for question in assignment.questions.all():
                    quest = QuestionStudent.objects.create(question=question, student=student)

            return HttpResponse(json.dumps({'state': True, 'response':'valid code',\
                                            'course_management_url':reverse('deimos:course_management', \
                                                                            kwargs={'course_id':course_id})}))
        else:
            return HttpResponse(json.dumps({'state':False,'response':'Expired code'}))
    else:
        # Student is already enrolled in the course
        return HttpResponse(json.dumps({'state': True, 'response':'valid code',\
                                                'course_management_url':reverse('deimos:course_management', \
                                                                                kwargs={'course_id':course_id})}))

def course_info(request,course_id):
    course = Course.objects.get(pk = course_id)
    course_infos, created , created = CourseInfo.objects.get_or_create_or_create(course= course)
    if created:
         course_infos.save()
    course_infos_html_content= {}
    course_infos_html_content.update({'about_course':markdown(course_infos.about_course)})
    course_infos_html_content.update({'course_skills':markdown(course_infos.course_skills)})
    course_infos_html_content.update({'course_plan':markdown(course_infos.course_plan)})
    course_infos_html_content.update({'course_instructors':markdown(course_infos.course_instructors)})
    try:
        student = get_object_or_404(Student, pk=request.user.id)
        if Enrollment.objects.filter(student=student, course=course).exists():
            is_student_list = 1 
        else: is_student_list = 0 

        context = {
            'course': course,
            'course_info':course_infos_html_content,
            "is_course_stud":  is_student_list,
            "is_student": True
        }
        return render(request, 'astros/course_info.html', context)
    
    except Student.DoesNotExist:
        return HttpResponseForbidden('STUDENT PROFILE DOES NOT EXIST')
       