import json
from urllib.parse import urlparse
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
from deimos.models import AssignmentStudent, Student

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
    # Making sure the request is done by a professor.
    professor = get_object_or_404(Professor, pk=request.user.id)
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
    # Making sure the request is done by a professor.
    professor = get_object_or_404(Professor, pk=request.user.id)
    assignment = get_object_or_404(Assignment, pk = assignment_id)
    course = assignment.course
    if not course.professors.filter(pk=request.user.pk).exists():
        return HttpResponseForbidden('You are not authorized to manage this Assignment.')
    questions = Question.objects.filter(assignment = assignment)
    for question in questions:
        question.text = replace_links_with_html(question.text)
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
    # Making sure the request is done by a professor.
    professor = get_object_or_404(Professor, pk=request.user.id)
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
    # Making sure the request is done by a professor.
    professor = get_object_or_404(Professor, pk=request.user.id)
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
    creates a `Question` object.
    Will usually require the assignment id, and sometimes
    not (in case the questions are stand-alone e.g. in the question bank)
    """
    # Making sure the request is done by a professor.
    professor = get_object_or_404(Professor, pk=request.user.id)
    if request.method == 'POST':
        assignment = Assignment.objects.get(pk = assignment_id)
        quest_num = assignment.questions.count() + 1
        topic = Topic.objects.get(name=request.POST.get('topic'))
        sub_topic = SubTopic.objects.get(name=request.POST.get('sub_topic'))
        text = request.POST.get('question_text')
        if type_int != 3 and type_int != 4:
            question_answer = request.POST.get('answer')
            if len(text)==0 or len(question_answer) == 0:
                return HttpResponseForbidden('You cannot create a question without content/answer.')
        else:
            if len(text) == 0:
                return HttpResponseForbidden('You cannot create a question without content')
        new_question = Question(
            number = quest_num,
            text = text,
            topic = topic,
            sub_topic = sub_topic,
            assignment = assignment
        )
        new_question.save() # Needed here. Before saving answer
        if type_int == 3:
            for key, value in request.POST.items():
                if key.startswith('answer_value_'):
                    option_index_start = len('answer_value_')
                    info_key = 'answer_info_' + key[option_index_start:]
                    answer_info_encoding = request.POST.get(info_key)
                    answer_content = value
                    if answer_info_encoding[1] == "0": # Expression Answer
                        new_question.answer_type = QuestionChoices.MCQ_EXPRESSION
                        answer = MCQExpressionAnswer(question=new_question, content=answer_content)
                    elif answer_info_encoding[1] == "1": # Float Answer
                        new_question.answer_type = QuestionChoices.MCQ_FLOAT
                        answer = MCQFloatAnswer(question=new_question, content=answer_content)
                    elif answer_info_encoding[1] == "2": # Latex Answer
                        new_question.answer_type = QuestionChoices.MCQ_LATEX
                        answer = MCQLatexAnswer(question=new_question, content=answer_content)
                    elif answer_info_encoding[1] == "3": # Text Answer
                        new_question.answer_type = QuestionChoices.MCQ_TEXT
                        answer = MCQTextAnswer(question=new_question, content=answer_content)
                    else:
                        return HttpResponseForbidden('Something went wrong')
                    answer.is_answer = True if answer_info_encoding[0] == '1' else False
                    answer.save() # Needed here.
        elif type_int == 0:
            new_question.answer_type = QuestionChoices.STRUCTURAL_EXPRESSION
            answer = ExpressionAnswer(question=new_question, content=question_answer)
        elif type_int == 1:
            new_question.answer_type = QuestionChoices.STRUCTURAL_FLOAT
            answer = FloatAnswer(question=new_question, content=question_answer)
        elif type_int == 2:
            new_question.answer_type = QuestionChoices.STRUCTURAL_LATEX
            answer = LatexAnswer(question=new_question, content=question_answer)
        elif type_int == 4:
            # 'Free' response question
            new_question.answer_type = QuestionChoices.STRUCTURAL_TEXT
            # No answer yet, but semantic answer validation coming soon.
            answer = TextAnswer(question=new_question, content='')
        else:
            return HttpResponseForbidden('Something went wrong')
        new_question.save()
        answer.save() # Needed here too.
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



@login_required(login_url='astros:login')
def question_view(request, question_id, assignment_id=None, course_id=None):
    # Making sure the request is done by a professor.
    professor = get_object_or_404(Professor, pk=request.user.id)
    question = Question.objects.get(pk=question_id)
    question.text = replace_links_with_html(question.text)
    answers = []
    is_latex = []
    is_mcq = False
    is_fr = False # is free response
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
        # !Important: order matters here
        is_latex = [0 for _ in range(ea.count()+ta.count()+fa.count())]
        is_latex.extend([1 for _ in range(la.count())])
    else:
        if question.answer_type == QuestionChoices.STRUCTURAL_EXPRESSION:
            answers.extend(question.expression_answers.all())
        elif question.answer_type == QuestionChoices.STRUCTURAL_TEXT:
            answers.extend(question.text_answers.all())
            is_fr = True
        elif question.answer_type == QuestionChoices.STRUCTURAL_FLOAT:
            answers.extend(question.float_answers.all())
        elif question.answer_type == QuestionChoices.STRUCTURAL_LATEX:# Probably never used (because disabled on frontend)
            answers.extend(question.latex_answers.all())
            is_latex.extend([1 for _ in range(question.latex_answers.all().count())])
        else:
            return HttpResponse('Something went wrong.')
    course = Course.objects.get(pk = course_id)
    if course.professors.filter(pk=request.user.pk).exists():
       show_answer = True
    else:
        show_answer = False
    return render(request, 'phobos/question_view.html',
                  {'question':question,\
                      'show_answer':show_answer,\
                     'is_mcq':is_mcq, 'is_fr':is_fr,'answers': answers,\
                         'answers_is_latex': zip(answers, is_latex) if is_latex else None})
       

def calci(request):
    return render(request, 'phobos/calci.html')

#------------------------FETCH VIEWS-----------------------------#
def get_subtopics(request, selected_topic):
    decoded_topic = unquote(selected_topic)
    try:
        topic = Topic.objects.get(name=decoded_topic)
        subtopics = list(topic.sub_topics.values_list('name', flat=True))
    #except Topic.DoesNotExist:
    except:
        subtopics = []

    return JsonResponse({'subtopics': subtopics})

#--------------HELPER FUNCTIONS--------------------------------#
def replace_links_with_html(text):
    # Find all URLs in the input text
    words = text.split()
    new_words = []
    for word in words:
        if word.startswith('http://') or word.startswith('https://'):
            parsed_url = urlparse(word)
            link_tag = f'<a href="{word}">{parsed_url.netloc}{parsed_url.path}</a>'
            new_words.append(link_tag)
        else:
            new_words.append(word)

    return ' '.join(new_words)

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        # You can perform any image processing or validation here
        
        # Return the URL of the uploaded image in the response
        return JsonResponse({'image_url': image.url})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required(login_url='astros:login')
def gradebook(request, course_id):
    course = Course.objects.get(pk = course_id)
    enrolled_students = Student.objects.filter(enrollments__course=course)
    assignments= Assignment.objects.filter(course = course)
    student_grades = []
    for student in enrolled_students: 
        grades = []
        for assignment in assignments:
            try:
                grade = AssignmentStudent.objects.get(student=student, assignment=assignment).get_grade()
            except AssignmentStudent.DoesNotExist:
                grade = 'None'

            grades.append(grade)
        student_grades.append(grades)
                  
    return render(request,'phobos/gradebook.html',\
                {'students_grades': zip(enrolled_students,student_grades),\
                 'assignments':assignments, 'course':course})

def student_profile(request,course_id,student_id):
    student= Student.objects.get(pk =student_id)
    course = Course.objects.get(pk = course_id)
    assignments= Assignment.objects.filter(course = course)
    grades = []
    for assignment in assignments:
        try:
            grade = AssignmentStudent.objects.get(student=student, assignment=assignment).grade
        except:
            grade = 'None'

        grades.append(grade)
    
    return render(request,'phobos/student_profile.html',\
                {'student_grade': zip(assignments,grades),\
                 'student':student, 'course':course})

