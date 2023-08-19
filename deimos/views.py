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
from phobos.models import QuestionChoices
import random
from sympy import symbols, simplify, Eq

# Create your views here.
@login_required(login_url='astros:login') 
def index(request):
    student = get_object_or_404(Student, username=request.user.username)
    courses = student.courses.order_by('-timestamp')
    context = {
        "courses": courses
    }
    return render(request, "deimos/index.html", context)

@login_required(login_url='astros:login') 
def course_management(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    # Check if there is any Enrollment entry that matches the given student and course
    student = get_object_or_404(Student, pk = request.user.pk)
    is_enrolled = Enrollment.objects.filter(student=student, course=course).exists()

    if not is_enrolled:
        return HttpResponseForbidden('You are not enrolled in this course.')
    assignments = Assignment.objects.filter(course=course)
    context = {
        "assignments": assignments,
        "course": course
    }
    return render(request, "deimos/course_management.html", context)

@login_required(login_url='astros:login') 
def assignment_management(request, assignment_id, course_id=None):
    # Making sure the request is done by a Student.
    student = get_object_or_404(Student, pk = request.user.pk)
    
    assignment = get_object_or_404(Assignment, pk = assignment_id)
    is_assigned = AssignmentStudent.objects.filter(student=student, assignment=assignment).exists()
    if not is_assigned:
        return HttpResponseForbidden('You have not be assigned this assignment.')
    # For every question, make sure a `QuestionStudent` object exists.
    # Create one if it doesn't 
    questions = Question.objects.filter(assignment = assignment)
    context = {
        "questions": questions,
        "assignment": assignment
    }
    return render(request, "deimos/assignment_management.html", context)

@login_required(login_url='astros:login')
def course_enroll(request, course_id):
    # Making sure the request is done by a Student.
    student = get_object_or_404(Student, pk=request.user.pk)
    course = get_object_or_404(Course, pk = course_id)
    if not Enrollment.objects.filter(student=student, course=course).exists():
        # If not enrolled, create a new Enrollment instance
        enrollment = Enrollment.objects.create(student=student, course=course)
        messages.info(request, message="You were successfully enrolled")
        # Redirect to a success page or course details page
        
        # Now assign all the courses assignments to the student. 
        for assignment in course.assignments.all():
            assign = AssignmentStudent.objects.create(assignment=assignment, student=student)
            for question in assignment.questions.all():
                quest = QuestionStudent.objects.create(question=question, student=student)
            
        return redirect('deimos:course_management', course_id=course_id)
    else:
        # Student is already enrolled in the course
        return redirect('deimos:course_management', course_id=course_id)
    
# TODO: Add the action link in answer_question.html
# TODO: Implement question_view as well.
@login_required(login_url='astros:login')
def answer_question(request, question_id, assignment_id=None, course_id=None):
    # Making sure the request is done by a Student.
    student = get_object_or_404(Student, pk=request.user.pk)
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    question_ids = assignment.questions.values_list('id', flat=True)
    question_nums = assignment.questions.values_list('number', flat=True)
    question = Question.objects.get(pk=question_id)
    question_student, created = QuestionStudent.objects.get_or_create(question=question, student=student)
    question_student.save() 
    is_mcq = False #nis mcq
    is_fr = False # is free response
    answers = []
    is_latex = []
    question_type = []
    question_type_dict = {'ea': 0, 'fa':1, 'la':2, 'ta':3}
    question_type_count = {'ea': 0, 'fa': 0, 'la': 0, 'ta': 0}
    if question.answer_type.startswith('MCQ'):
        is_mcq = True
        ea = question.mcq_expression_answers.all()
        answers.extend(ea)
        ta = question.mcq_text_answers.all()
        answers.extend(ta)
        fa = question.mcq_float_answers.all()
        answers.extend(fa)
        la = question.mcq_latex_answers.all()
        answers.extend(la)
        
        question_type_count['ea'] = ea.count()
        question_type_count['fa'] = fa.count()
        question_type_count['la'] = la.count()
        question_type_count['ta'] = ta.count()
        # !Important: order matters here
        is_latex = [0 for _ in range(ea.count()+ta.count()+fa.count())]
        is_latex.extend([1 for _ in range(la.count())])
        for q_type in question_type_dict:
            question_type.extend([question_type_dict[q_type] for _ in range(question_type_count[q_type])])
        assert len(is_latex) == len(answers)
        shuffler = [counter for counter in range(len(answers))]
        random.shuffle(shuffler)  
        is_latex = [is_latex[i] for i in shuffler]
        answers = [answers[i] for i in shuffler]
    elif question.answer_type == QuestionChoices.STRUCTURAL_LATEX:# Probably never used (because disabled on frontend)
        answers.extend(question.latex_answers.all())
        is_latex.extend([1 for _ in range(question.latex_answers.all().count())]) 
        question_type = [2]  
    elif question.answer_type == QuestionChoices.STRUCTURAL_EXPRESSION:
        answers.extend(question.expression_answers.all())
        question_type = [0]
    elif question.answer_type == QuestionChoices.STRUCTURAL_FLOAT:
        answers.extend(question.float_answers.all())
        question_type = [1]
    elif question.answer_type == QuestionChoices.STRUCTURAL_TEXT:
        is_fr = True 
        answers.extend(question.text_answers.all())
        question_type = [4]     
    context = {
        'question':question,
        'question_ids_nums':zip(question_ids, question_nums),
        'assignment_id': assignment_id,
        'course_id': course_id,
        "is_mcq": is_mcq,
        "is_fr": is_fr, 
        "answers_is_latex_question_type": zip(answers, is_latex, question_type),
        'question_type': question_type, # For structural
        'answer': answers[0]
    }
    return render(request, 'deimos/answer_question.html',
                  context)
@login_required(login_url='astros:login')
def validate_answer(request, question_id, assignment_id=None, course_id=None):
    student = get_object_or_404(Student, pk=request.user.pk)
    
    if request.method == 'POST':
        correct = False
        data = json.loads(request.body)
        submitted_answer = data["answer"]
        question = Question.objects.get(pk=question_id)
        
        # Use get_or_create to avoid duplicating QuestionStudent instances
        # Normally, we should just use get because QuestionStudent object is already created
        # whenever the user opens a question for the first time, but just to be safe.
        question_student, created = QuestionStudent.objects.get_or_create(student=student, question=question)
        
        if (question_student.get_num_attempts() < question.max_num_attempts and not question_student.success):
            if data["questionType"] == 'structural':
                attempt = QuestionAttempt.objects.create(question_student=question_student)
                attempt.content = submitted_answer
                if question.answer_type == QuestionChoices.STRUCTURAL_EXPRESSION:
                    assert question.expression_answers.count() == 1
                    answer = question.expression_answers.first()
                    correct = compare_expressions(answer.content, submitted_answer)
                elif question.answer_type == QuestionChoices.STRUCTURAL_FLOAT:
                    assert question.float_answers.count() == 1
                    answer = question.float_answers.first()
                    try:
                        correct = compare_floats(answer.content, float(submitted_answer)) 
                    except ValueError:
                        # TODO: Maybe return a value to the user side that will ask them to enter a float.
                        correct = False
                if correct:
                    # Deduct points based on attempts, but ensure it doesn't go negative
                    attempt.num_points = max(0, question.num_points - (question.deduct_per_attempt * question_student.get_num_attempts()))
                    question_student.success = True
                    attempt.success = True
                    
                question_student.save()  # Save the changes to the QuestionStudent instance
                attempt.save()
        # Return a JsonResponse
        return JsonResponse({
            'correct': correct
        })
    


           
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            user = Student.objects.get(email=email)
        except Student.DoesNotExist:
            user = None

        # Authenticate the user based on the provided email and password
        if user is not None and user.check_password(password):
            # If authentication successful, log in the user
            login(request, user)
            return HttpResponseRedirect(reverse("deimos:index"))
        
        else:
            return render(request, "astros/login.html", {
                "message_deimos": "Invalid email and/or password."
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
        
        if password != confirmation:
            return render(request, "astros/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new student
        try:
            student = Student.objects.create_user(username, email, password,\
                                                 first_name = first_name,\
                                                    last_name = last_name)
            student.save()
        except IntegrityError:
            return render(request, "astros/register.html", {
                "message": "Username already taken."
            })
        login(request, student)
        return HttpResponseRedirect(reverse("deimos:index"))
    else:
        return render(request, "astros/register.html")


#---------HELPER FUNCTIONS--------
def is_student_enrolled(student_id, course_id):
    # Retrieve the Student and Course instances based on their IDs
    student = get_object_or_404(Student, pk=student_id)
    course = get_object_or_404(Course, pk=course_id)

    # Check if there is any Enrollment entry that matches the given student and course
    is_enrolled = Enrollment.objects.filter(student=student, course=course).exists()

    return is_enrolled
def compare_expressions(e1, e2):
    """ Given two strings e1 and e2,
        returns True if they are algebraically equivalent, 
        returns False otherwise
    """
    su = set(e1) | set(e2)
    so = symbols(' '.join(su))
    sym_e1 = simplify(e1, symbols=so)
    sym_e2 = simplify(e2, symbols=so)
    same = Eq(sym_e1, sym_e2)
    return True if same==True else False

def compare_floats(f1, f2):
    """
    Given two floats f1 and f2,
    returns True if they are equal,
    returns False otherwise
    """

    # TODO! Implement margin error
    if f1 == f2:
        return True
    else:
        return False
#--------------------Depecrated functions used in development--------------------
def question_nav(request):
    return render(request, 'deimos/question_nav.html', {})

def action_menu(request):
    return render(request, 'deimos/action_menu.html', {})