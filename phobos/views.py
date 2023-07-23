import json
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
    courses = Course.objects.filter(professors__in=[request.user]).order_by('-timestamp') # TODO: add filter to display only the professor's courses.
    context = {
        "courses": courses
    }
    return render(request, "phobos/index.html", context)

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
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('phobos:index')  
    else:
        form = CourseForm()
    return render(request, 'phobos/create_course.html', {'form': form})

@login_required(login_url='astros:login')
def create_question(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        mcq_answer_form = McqAnswerForm(request.POST, request.FILES)
        float_answer_form = FloatAnswerForm(request.POST)
        expression_answer_form = ExpressionAnswerForm(request.POST)

        if question_form.is_valid() and mcq_answer_form.is_valid():
            question = question_form.save()
            mcq_answer_form.instance.question = question
            mcq_answer_form.save()

            # If it's a multiple-choice question, save the MCQ answer
            if question.is_mcq():
                mcq_answer_form.save()

            # If it's a float question, save the float answer
            if question.is_float():
                float_answer_form.instance.question = question
                float_answer_form.save()

            # If it's an expression question, save the expression answer
            if question.is_expression():
                expression_answer_form.instance.question = question
                expression_answer_form.save()

            return redirect('question_list')  # Redirect to a list view of all questions or a success page
    else:
        question_form = QuestionForm()
        mcq_answer_form = McqAnswerForm()
        float_answer_form = FloatAnswerForm()
        expression_answer_form = ExpressionAnswerForm()

    return render(request, 'phobos/create_question.html', {
        'question_form': question_form,
        'mcq_answer_form': mcq_answer_form,
        'float_answer_form': float_answer_form,
        'expression_answer_form': expression_answer_form,
    })

