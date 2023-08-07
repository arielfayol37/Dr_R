import json
from urllib.parse import unquote  # Import unquote for URL decoding
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import *
from .models import *
from django.shortcuts import get_object_or_404
from django.middleware import csrf
from django.utils.timesince import timesince


# Create your views here.
@login_required(login_url='astros:login') 
def index(request):
    professor = get_object_or_404(Professor, pk = request.user.pk)
    courses = Course.objects.filter(professors__in=[professor]).order_by('-timestamp')
    context = {
        "courses": courses
    }
    return render(request, "phobos/index.html", context)

@login_required(login_url='astros:login') 
def course_management(request, course_id):
    course = get_object_or_404(Course, pk = course_id)
    if not course.professors.filter(pk=request.user.pk).exists():
        return HttpResponseForbidden('You are not authorized to manage this course.')
    assignments = Assignment.objects.filter(course=course)
    context = {
        "assignments": assignments,
        "course": course
    }
    return render(request, "phobos/course_management.html", context)

@login_required(login_url='astros:login') 
def assignment_management(request, assignment_id, course_id=None):
    # assert isinstance(request.user, Professor)
    assignment = get_object_or_404(Assignment, pk = assignment_id)
    course = assignment.course
    if not course.professors.filter(pk=request.user.pk).exists():
        return HttpResponseForbidden('You are not authorized to manage this Assignment.')
    questions = Question.objects.filter(assignment = assignment)
    context = {
        "questions": questions,
        "assignment": assignment
    }
    return render(request, "phobos/assignment_management.html", context)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
                # Check if a user with the provided email exists
        try:
            user = Professor.objects.get(email=email)
        except Professor.DoesNotExist:
            user = None

        # Authenticate the user based on the provided email and password
        if user is not None and user.check_password(password):
            # If authentication successful, log in the user
            login(request, user)
            return HttpResponseRedirect(reverse("phobos:index"))
        
        else:
            return render(request, "astros/login.html", {
                "message_phobos": "Invalid email and/or password."
            })
    else:
        return render(request, "astros/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("astros:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        department = request.POST["department"]
        if password != confirmation:
            return render(request, "astros/register.html", {
                "message_phobos": "Passwords must match."
            })

        # Attempt to create new professor
        try:
            professor = Professor.objects.create_user(username, email, password,\
                                                 first_name = first_name, department = department,\
                                                    last_name = last_name)
            professor.save()
        except IntegrityError:
            return render(request, "astros/register.html", {
                "message_phobos": "Username already taken."
            })
        login(request, professor)
        return HttpResponseRedirect(reverse("phobos:index"))
    else:
        return render(request, "astros/register.html")
    
@login_required(login_url='astros:login')    
def create_course(request):
    # assert isinstance(request.user, Professor)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request=request, message='Course created successfully!')
            return redirect('phobos:index')  
    else:
        form = CourseForm()
    return render(request, 'phobos/create_course.html', {'form': form})

@login_required(login_url='astros:login')    
def create_assignment(request, course_id=None):
    # assert isinstance(request.user, Professor)
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save()
            messages.info(request=request, message='Assignment created successfully!')
            return redirect('phobos:course_management', course_id=assignment.course.id)  
    else:
        if course_id is not None:
            course = Course.objects.get(pk = course_id)
            form = AssignmentForm({'course': course})
        else:
            form = AssignmentForm()
    return render(request, 'phobos/create_assignment.html', {'form': form})

@login_required(login_url='astros:login')
def create_question(request, assignment_id=None, type_int=None):
    """
    creates a question object.
    Will usually require the assignment id, and sometimes
    not (in case the questions are stand-alone e.g. in the question bank)
    """
    # assert isinstance(request.user, Professor)
    if request.method == 'POST':
        assignment = Assignment.objects.get(pk = assignment_id)
        quest_num = assignment.questions.count() + 1
        topic = Topic.objects.get(name=request.POST.get('topic'))
        sub_topic = SubTopic.objects.get(name=request.POST.get('sub_topic'))
        new_question = Question(
            number = quest_num,
            text = request.POST.get('question_text'),
            topic = topic,
            sub_topic = sub_topic,
            answer = request.POST.get('answer'),
            assignment = assignment
        )
        new_question.save()
        messages.info(request=request, message="Question created successfully!")
        return HttpResponseRedirect(reverse("phobos:assignment_management",\
                                            kwargs={'course_id':assignment.course.id,\
                                                    'assignment_id':assignment_id}))

    if assignment_id is not None:
        assignment = Assignment.objects.get(pk = assignment_id)
        topics = assignment.course.topics.all()

    return render(request, 'phobos/create_question.html', {
 
        'topics': topics if topics else '',
        'assignment_id': assignment_id,
    })

def get_subtopics(request, selected_topic):
    decoded_topic = unquote(selected_topic)
    try:
        topic = Topic.objects.get(name=decoded_topic)
        subtopics = list(topic.sub_topics.values_list('name', flat=True))
    #except Topic.DoesNotExist:
    except:
        subtopics = []

    return JsonResponse({'subtopics': subtopics})

@login_required(login_url='astros:login')
def question_view(request, question_id, assignment_id=None, course_id=None):
    question = Question.objects.get(pk=question_id)
    course = Course.objects.get(pk = course_id)
    if course.professors.filter(pk=request.user.pk).exists():
       show_answer = True
    else:
        show_answer = False
    return render(request, 'phobos/question_view.html',
                  {'question':question,\
                      'show_answer':show_answer})
       

def calci(request):
    return render(request, 'phobos/calci.html')


