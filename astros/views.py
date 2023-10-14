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
from django.core.mail import send_mail
from django.http import JsonResponse
import random

code_base=[]

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
            "is_student": True,
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
            # Now assign all the courses assignments to the student. NOTE: CHANGING THIS TO ALLOW PROFS ASSIGN STUDENTS.

            # for assignment in course.assignments.all():
            #     assign = AssignmentStudent.objects.create(assignment=assignment, student=student)
            #     for question in assignment.questions.all():
            #         quest = QuestionStudent.objects.create(question=question, student=student)

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
@login_required(login_url="astros:login")
def course_info(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return HttpResponseForbidden('COURSE DOES NOT EXIST')
    
    try:
        student = Student.objects.get(pk=request.user.id)
    except Student.DoesNotExist:
        return HttpResponseForbidden('STUDENT PROFILE DOES NOT EXIST')

    course_infos, created = CourseInfo.objects.get_or_create(course=course)
    if created:
        course_infos.save()

    def markdown_convert(field):
        return markdown(getattr(course_infos, field))

    course_infos_html_content = {
        'about_course': markdown_convert('about_course'),
        'course_skills': markdown_convert('course_skills'),
        'course_plan': markdown_convert('course_plan'),
        'course_instructors': markdown_convert('course_instructors'),
    }
    is_student_list = Enrollment.objects.filter(student=student, course=course).exists()

    context = {
        'course': course,
        'course_info': course_infos_html_content,
        'is_course_stud': is_student_list,
        'is_student': True,
    }

    return render(request, 'astros/course_info.html', context)

def generate_auth_code(request):
    min=100000000000
    max=999999999999

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data["email"]
            code= random.randint(min,max)
            code_base.append({'email':email,'code': code})
            send_mail(
            'Authentify',                # subject
           f'enter the following authentification code on the website DR_R-{code}',    # message
            'no.reply.dr.r.valpo@gmail.com',      # from email
             [email],      # recipient list
             fail_silently=False,           # Raises an error if there's a problem
        )
            return JsonResponse({'success':True,
                         'message':'An authentification code was sent to email. Please enter the code into the box'})
        except:
            return JsonResponse({'success':False,
                         'message':'Something went wrong during the mailing process'})
    return JsonResponse({'success':False,
                         'message':'Something went wrong'})
        
def validate_auth_code(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data["email"]
            code= data["code"]
            for auth_code in code_base:
                if int(code)== int(auth_code["code"]) and str(email)== str(auth_code["email"]):
                    code_base.remove(auth_code)
                    return JsonResponse({'success':True,
                    'message':'OK'})
        except:
            return JsonResponse({'success':False,
                         'message':'Something '})
    return JsonResponse({'success':False,
                         'message':'Something '})


