#python3 phobos:views.py
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
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import transaction
from django.middleware import csrf
from django.utils.timesince import timesince
from django.utils import timezone
from datetime import datetime
from deimos.models import AssignmentStudent, Student, QuestionStudent, Enrollment, QuestionModifiedScore
from datetime import date
from sklearn.metrics.pairwise import cosine_similarity
from Dr_R.settings import BERT_TOKENIZER, BERT_MODEL
import heapq
from markdown2 import markdown
from .utils import *
from django.core.mail import send_mail
from django.core.files.storage import default_storage


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
    is_question_bank = course.name =='Question Bank'
    if not course.professors.filter(pk=request.user.pk).exists() and not is_question_bank:
        return HttpResponseForbidden('You are not authorized to manage this course.')
    assignments = Assignment.objects.filter(course=course).order_by('-timestamp')
    context = {
        "assignments": assignments,
        "course": course,
        "is_question_bank":is_question_bank
    }
    return render(request, "phobos/course_management.html", context)

@login_required(login_url='astros:login') 
def assignment_management(request, assignment_id, course_id=None):
    # Making sure the request is done by a professor.
    professor = get_object_or_404(Professor, pk=request.user.id)
    assignment = get_object_or_404(Assignment, pk = assignment_id)
    course = assignment.course
    is_question_bank = course.name == 'Question Bank'
    if not course.professors.filter(pk=request.user.pk).exists() and not is_question_bank:
        return HttpResponseForbidden('You are not authorized to manage this Assignment.')
    questions = Question.objects.filter(assignment = assignment, parent_question=None)
    
    # for question in questions:
    #    question.text = replace_links_with_html(question.text)
    context = {
        "questions": questions,
        "assignment": assignment,
        'is_question_bank':is_question_bank,
        'course':course
    }
    return render(request, "phobos/assignment_management.html", context)

@login_required(login_url='astros:login')
def question_bank(request):
    if not Professor.objects.filter(pk=request.user.pk).exists():
        return HttpResponse('You are not allowed to view the QUESTION BANK')
    qbank_course_id = Course.objects.get(name='Question Bank').pk
    return course_management(request, qbank_course_id)

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
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)
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

def forgot_password(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data["email"].strip()
        password= data['new_password'].strip()

        try:
            user = Professor.objects.get(email=email)
        except Professor.DoesNotExist:
            return JsonResponse({'success':False,
                        'message':"Profile with this email does not exist"})

        user.set_password(password)
        user.save()
        return JsonResponse({'success':True,
            'message':'Password Succesfully changed'})
    return JsonResponse({'success':False,
                         'message':'Something went wrong'})


def register(request):
    if request.method == "POST":
        username = request.POST["username"].strip()
        email = request.POST["email"].strip()
        password = request.POST["password"].strip()
        first_name = request.POST["first_name"].strip().title()
        last_name = request.POST["last_name"].strip().title()
        department = request.POST["department"].strip().title()

        try: 
            prof = Professor.objects.get(username=username)
            username = str(username) + str(random.randint(1, 1000000))
        except:
            pass

        try:
            checking_prof = Professor.objects.get(email=email)
            if checking_prof:
                return render(request, "astros/register.html", {
                "message": "Student profile with this email already exists."
            })
        except Professor.DoesNotExist:
            pass
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
            return redirect('phobos:index')  
    else:
        form = CourseForm()
    return render(request, 'phobos/create_course.html', {'form': form})




@login_required(login_url='astros:login')    
def create_assignment(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)  # Don't save to DB yet
            assignment.course = course  # Set the course field
            # Getting the grading scheme
            gs_pk = int(request.POST['grading_scheme_pk'])
            if gs_pk == -1:
                # Creating a new grading scheme
                name= request.POST['new_scheme_name']
                # checking if scheme with same name already exists
                exists = GradingScheme.objects.filter(name=name, course=course).exists()
                if exists:
                    old_gs = GradingScheme.objects.get(name=name, course=course)
                    try:
                        name = name + str(int(old_gs.name[-1]) + 1) # Not expecting the
                                                                    # integer to be more than
                                                                    # two digits.
                    except:
                        name = name + str(1)
                scheme = GradingScheme.objects.create(
                    course = course,
                    name= name,
                    num_points = request.POST['num_points'],
                    mcq_num_attempts = request.POST['max_mcq_num_attempts'],
                    struct_num_attempts = request.POST['max_num_attempts'],
                    deduct_per_attempt = request.POST['deduct_per_attempt'],
                    mcq_deduct_per_attempt = request.POST['mcq_deduct_per_attempt'],
                    margin_error = request.POST['margin_error'],
                    percentage_pts_units = request.POST['percentage_pts_units'],
                    units_num_attempts = request.POST['units_num_attempts'],
                    late_sub_deduct = request.POST['late_sub_deduct'],
                    floor_percentage = request.POST['floor_percentage']    
                    )
                scheme.save()
                
            else:
                scheme = GradingScheme.objects.get(pk=gs_pk)
            assignment.grading_scheme = scheme
            assignment.save()  # Now save to DB
            return redirect('phobos:course_management', course_id=assignment.course.id)
    else:
        form = AssignmentForm(course=course)
        gs_exists = GradingScheme.objects.filter(course=course).exists()
        if not gs_exists:
            default_gs, created = GradingScheme.objects.get_or_create(course=course, name="Default")
            default_gs.save()
        default_gs = GradingScheme.objects.get(course=course, name="Default")
        grading_schemes = list(course.grading_schemes.all())
        grading_schemes.reverse()
    return render(request, 'phobos/create_assignment.html', {'form': form,
        'course':course, 'default_gs':default_gs, 'grading_schemes':grading_schemes})

def format_date(due_date_str):
    # Check if due_date_str is already a datetime object
    if isinstance(due_date_str, datetime):
        due_date = due_date_str
    else:
        # Parsing the date string
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d %H:%M:%S%z')
    # Getting the day with the appropriate suffix
    day = int(due_date.strftime('%d'))
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = 'th'
    else:
        suffix = ['st', 'nd', 'rd'][day % 10 - 1]

    # Formatting the date in the desired format
    formatted_date = due_date.strftime(f'%B {day}{suffix}, %Y at %I:%M%p')
    return formatted_date

@login_required(login_url='astros:login')
@csrf_exempt
def assign_assignment(request, assignment_id, course_id=None):
    assignment = get_object_or_404(Assignment, pk = assignment_id)
    course = assignment.course
    email_list = []
    if not course.professors.filter(pk=request.user.pk).exists():
        return JsonResponse({'message': 'You are not authorized to manage this Assignment.', 'success':False})
    if request.method == 'POST':
        students = Student.objects.filter(enrollments__course=course)
        for student in students:
            email_list.append(student.email)
            assignment_student, created = AssignmentStudent.objects.get_or_create(assignment=assignment, student=student)
            for question in assignment.questions.all():
                    # ASSINGING EVERY QUESTION IN THE ASSIGNMENT TO STUDENTS
                    # If QuestionStudent already exists, we delete it (just in case).
                    quest, created = QuestionStudent.objects.get_or_create(question=question, student=student)
                    if not created:
                        quest.delete()
                        quest = QuestionStudent.objects.create(question=question, student=student)
                    quest.save()
        assignment.is_assigned = True
        
        send_mail(
            'New Assignment',                # subject
           f'You have {assignment.name} to be completed before {format_date(assignment.due_date)}. Good luck!',    # message
            'no.reply.dr.r.valpo@gmail.com',      # from email
             email_list,      # recipient list
             fail_silently=True,           # Raises an error if there's a problem
        )
        assignment.save()
        return JsonResponse({
            'message':'Assignment assigned successfully.', 'success':True
        })
    return JsonResponse({'message':'Something went wrong.','success':False})

def create_mcq_expression_answer(new_question, answer_content):
    return MCQExpressionAnswer(question=new_question, content=answer_content)

def create_mcq_float_answer(new_question, answer_content):
    return MCQFloatAnswer(question=new_question, content=answer_content)

def create_mcq_variable_float_answer(new_question, answer_content):
    return MCQVariableFloatAnswer(question=new_question, content=answer_content)

def create_mcq_latex_answer(new_question, answer_content):
    return MCQLatexAnswer(question=new_question, content=answer_content)

def create_mcq_text_answer(new_question, answer_content): 
    return MCQTextAnswer(question=new_question, content=answer_content)

# Function to determine which MCQ float answer to create
def create_appropriate_mcq_float_answer(new_question, answer_content, vars_dict):
    if answer_content.startswith('@{') and answer_content.endswith('}@'):
        if vars_dict:
            return create_mcq_variable_float_answer(new_question, answer_content)
        else:
            raise ValueError('Expected variable expression but got no variable.')
    else:
        return create_mcq_float_answer(new_question, answer_content)

def create_expression_answer(new_question, question_answer, answer_unit, answer_preface):
    return ExpressionAnswer(question=new_question, content=question_answer,
                            answer_unit=answer_unit, preface=answer_preface)

def create_float_answer(new_question, question_answer, answer_unit, answer_preface):
    return FloatAnswer(question=new_question, content=question_answer,
                       answer_unit=answer_unit, preface=answer_preface)

def create_variable_float_answer(new_question, question_answer, answer_unit, answer_preface):
    return VariableFloatAnswer(question=new_question, content=question_answer,
                               answer_unit=answer_unit, preface=answer_preface)

def create_latex_answer(new_question, question_answer):
    return LatexAnswer(question=new_question, content=question_answer)

def create_text_answer(new_question):
    return TextAnswer(question=new_question, content='')

def create_appropriate_float_answer(new_question, question_answer, answer_unit, answer_preface,vars_dict):
    if question_answer.startswith('@{') and question_answer.endswith('}@'):
        if vars_dict:
            return create_variable_float_answer(new_question, question_answer, answer_unit, answer_preface)
        else:
            raise ValueError('Expected variable expression but got no variable.')
    else:
        return create_float_answer(new_question, question_answer, answer_unit, answer_preface)

def create_matching_pairs(request, new_question, q_num):
    num_of_mps_approx = int(request.POST[q_num + '_num_of_mps'])
    for l in range(num_of_mps_approx):
        mp_a = request.POST.get(q_num + '_' + str(l) + '_mp_a')
        mp_b = request.POST.get(q_num + '_' + str(l) + '_mp_b')
        if mp_a is not None and mp_b is not None:
            answer = MatchingAnswer.objects.create(
                question=new_question, part_a=mp_a, part_b=mp_b
            )
    return answer




@transaction.atomic
@login_required(login_url='astros:login')
def create_question(request, assignment_id=None, question_nums_types=None):
    """
    creates a `Question` object.
    Will usually require the assignment id, and sometimes
    not (in case the questions are stand-alone e.g. in the question bank)
    """
    # Making sure the request is done by a professor.
    professor = get_object_or_404(Professor, pk=request.user.id)
    
    if request.method == 'POST':
        # Getting the question pairs.
        num_type_pairs = []
        for string_pair in question_nums_types.split("$")[1:]: # From the JS, the first item will be empty
            question_num, question_type = string_pair.split("-")
            num_type_pairs.append((question_num, question_type))
        assignment = Assignment.objects.get(pk = assignment_id)
        quest_num = assignment.questions.filter(parent_question=None).count() + 1
        parent_question = None
        counter = 0
        vars_dict = {}
        topic = Topic.objects.get(name=request.POST.get('topic'))
        sub_topic = SubTopic.objects.get(name=request.POST.get('sub_topic'))

        difficulty = request.POST.get('question_difficulty', 'MEDIUM')
        for q_num, q_type in num_type_pairs:
            counter += 1
            type_int = int(q_type)

            text = request.POST.get(q_num + '_question_text')
            answer_unit = request.POST.get(q_num + '_answer_unit')
            answer_preface = request.POST.get(q_num + '_answer_preface')
            if answer_unit == '':
                answer_unit = None
            if type_int != 3 and type_int != 4:
                question_answer = request.POST.get(q_num + '_answer')
            new_question = Question(
                number = quest_num if counter == 1 else str(quest_num) + chr(64 + counter),
                text = text,
                topic = topic,
                sub_topic = sub_topic,
                assignment = assignment,
                parent_question = parent_question 
            )
            
            new_question.save()  # the settings object is automatically created in the save

            num_points = request.POST.get(q_num + '_num_points')
            struct_max_num_attempts = request.POST.get(q_num + '_max_num_attempts')
            struct_deduct_per_attempt = request.POST.get(q_num + '_deduct_per_attempt')
            margin_error = request.POST.get(q_num + '_margin_error')
            mcq_max_num_attempts = request.POST.get(q_num + '_max_mcq_num_attempts')
            mcq_deduct_per_attempt = request.POST.get(q_num + '_mcq_deduct_per_attempt')
            percentage_pts_units = request.POST.get(q_num + '_percentage_pts_units')
            units_num_attempts = request.POST.get(q_num + '_units_num_attempts')

            for key, value in request.POST.items():
                if key.startswith('domain') and counter==1: # Creating the variables
                    # variables will be associated only to the parent question.
                    _, bound_type, var_symbol, bound_number = key.split('#')
                    bound_value = value
                    if var_symbol not in vars_dict:
                        vars_dict[var_symbol] = {}
                    if bound_type not in vars_dict[var_symbol]:
                        vars_dict[var_symbol][bound_type] = []
                    vars_dict[var_symbol][bound_type].append(bound_value)
                
                elif key.startswith(q_num + '_question_image_label_'):
                    image_number = key[len(q_num + '_question_image_label_'):]
                    label_name = q_num + '_question_image_label_' + image_number
                    image_name = q_num + '_question_image_file_' + image_number
                    image = request.FILES.get(image_name)
                    label = request.POST.get(label_name)
                    question_image = QuestionImage(question=new_question, image=image, label=label)
                    question_image.save()
                # creating the hints
                elif key.startswith(q_num + '_hint_'):
                    hint_text = value
                    hint = Hint.objects.create(question=new_question, text=hint_text)
                    hint.save()
            if counter == 1:
                for var_symbol in vars_dict:
                    step_size = request.POST[f'step#size#{var_symbol}']
                    is_integer = not bool(int(request.POST[f'var#type#{var_symbol}'])) # Front End will return 0 for integer. 
                    new_variable = Variable(question=new_question, symbol=var_symbol, step_size=step_size, is_integer=is_integer)
                    new_variable.save()
                    assert len(vars_dict[var_symbol]['lb']) == len(vars_dict[var_symbol]['ub'])
                    for bound_index in range(len(vars_dict[var_symbol]['lb'])):
                        var_interval = VariableInterval(variable=new_variable, \
                                                        lower_bound = vars_dict[var_symbol]['lb'][bound_index],\
                                                        upper_bound = vars_dict[var_symbol]['ub'][bound_index])
                        var_interval.save()
            if type_int == 3:
                for key, value in request.POST.items():
                    if key.startswith(q_num + '_answer_value_'):
                        option_index_start = len(q_num + '_answer_value_')
                        info_key = q_num + '_answer_info_' + key[option_index_start:]
                        answer_info_encoding = request.POST.get(info_key)
                        answer_content = value
                        # Really, all thsoe QuestionChoices don't matter for two reasons:
                            # 1) If there are different types of mcq answers which is often the case
                            #     the answer_type will end up being just the type of the last answer
                            # 2) All what the other parts of the programs care about is whether the question
                            #     is an MCQ or not.    
                        # Map encoding values to functions and QuestionChoices
                        # Map encoding values to functions and QuestionChoices
                        answer_creation_map = {
                            "0": (create_mcq_expression_answer, QuestionChoices.MCQ_EXPRESSION),
                            "1": (create_appropriate_mcq_float_answer, None),  # Placeholder for QuestionChoices, determined in function
                            "2": (create_mcq_latex_answer, QuestionChoices.MCQ_LATEX),
                            "3": (create_mcq_text_answer, QuestionChoices.MCQ_TEXT)
                        }

                        # Get the answer type encoding
                        answer_type_encoding = answer_info_encoding[1]

                        # Create the answer based on the encoding
                        if answer_type_encoding in answer_creation_map:
                            creation_func, question_choice = answer_creation_map[answer_type_encoding]
                            # Special handling for float answers to determine the correct QuestionChoices
                            if answer_type_encoding == "1":
                                answer = creation_func(new_question, answer_content, vars_dict)
                                if answer_content.startswith('@{') and answer_content.endswith('}@'):
                                    if vars_dict:
                                        new_question.answer_type = QuestionChoices.MCQ_VARIABLE_FLOAT
                                    else:
                                        raise ValueError('Expected variable expression but got no variable.')
                                else:
                                    new_question.answer_type = QuestionChoices.MCQ_FLOAT
                            else:
                                new_question.answer_type = question_choice
                                answer = creation_func(new_question, answer_content)
                        else:
                            return HttpResponseForbidden('Something went wrong: unexpected mcq encoding')

                        # Set if the answer is correct based on the encoding
                        answer.is_answer = answer_info_encoding[0] == '1'
                        answer.save()  # Save the answer
                
                # Getting the MCQ images
                for key, value in request.FILES.items():
                    if key.startswith(q_num + '_answer_value_'):
                        option_index_start = len(q_num + '_answer_value_')
                        info_key = q_num + '_answer_info_' + key[option_index_start:]
                        answer_info_encoding = request.POST.get(info_key)
                        image = value
                        if answer_info_encoding[1] == '7': # Image answer
                            new_question.answer_type = QuestionChoices.MCQ_IMAGE
                            # image = request.FILES.get(info_key)
                            label = request.POST.get(q_num + '_image_label_' + key[option_index_start:])
                            answer = MCQImageAnswer(question=new_question, image=image, label=label)
                        else:
                            return HttpResponseForbidden('Something went wrong: unexpected encoding for mcq image answer')
                        answer.is_answer = True if answer_info_encoding[0] == '1' else False
                        answer.save() # Needed here.                
                        
            else:
                # Map type_int values to functions and QuestionChoices
                answer_creation_map = {
                    0: (create_expression_answer, QuestionChoices.STRUCTURAL_EXPRESSION),
                    1: (create_appropriate_float_answer, None),  # Placeholder for QuestionChoices, determined in function,
                    2: (create_latex_answer, QuestionChoices.STRUCTURAL_LATEX),
                    4: (create_text_answer, QuestionChoices.STRUCTURAL_TEXT),
                    8: (create_matching_pairs, QuestionChoices.MATCHING_PAIRS)
                }
                # Create the answer based on type_int
                if type_int in answer_creation_map:
                    creation_func, question_choice = answer_creation_map[type_int]
                    if type_int != 1: # will handle this particular case below
                        new_question.answer_type = question_choice
                    if type_int == 8:
                        answer = creation_func(request, new_question, q_num)
                    elif type_int == 4:
                        answer = creation_func(new_question)
                    elif type_int == 2:
                        answer = creation_func(new_question, question_answer)
                    else:
                        if type_int == 1:
                            answer = creation_func(new_question, question_answer,\
                                                answer_unit, answer_preface, vars_dict)
                            if question_answer.startswith('@{') and question_answer.endswith('}@'):
                                if vars_dict:
                                    new_question.answer_type = QuestionChoices.STRUCTURAL_VARIABLE_FLOAT
                                else:
                                    raise ValueError('Expected variable expression but got no variable.')
                            else:
                                new_question.answer_type = QuestionChoices.STRUCTURAL_FLOAT
                        else:
                            answer = creation_func(new_question, question_answer,\
                                                answer_unit, answer_preface)

                else:
                    return HttpResponseForbidden('Something went wrong: unexpected question type_int')
                
            new_question.save(save_settings=True)
            
            if counter == 1:
                parent_question = new_question
            answer.save() # Needed here too.
           
            # Saving the settings.
            if new_question.answer_type.startswith(('MCQ', 'MATCHING')): # if MCQ or Matching Pair
                question_settings = new_question.mcq_settings
                question_settings.mcq_max_num_attempts = int(mcq_max_num_attempts)
                question_settings.mcq_deduct_per_attempt = float(mcq_deduct_per_attempt)
            else:
                question_settings = new_question.struct_settings
                question_settings.units_num_attempts = int(units_num_attempts)
                question_settings.max_num_attempts = int(struct_max_num_attempts)
                question_settings.percentage_pts_units = float(percentage_pts_units)
                question_settings.deduct_per_attempt = float(struct_deduct_per_attempt)
                question_settings.margin_error = float(margin_error)
            question_settings.num_points = int(num_points)
            question_settings.difficulty_level = difficulty
            question_settings.save()
        return HttpResponseRedirect(reverse("phobos:assignment_management",\
                                            kwargs={'course_id':assignment.course.id,\
                                                    'assignment_id':assignment_id}))

    if assignment_id is not None:
        assignment = Assignment.objects.get(pk = assignment_id)
        topics = assignment.course.topics.all()
        # question_difficulties = DifficultyChoices.choices
        question_difficulties = ['EASY', 'MEDIUM', 'DIFFICULT']
    return render(request, 'phobos/create_question.html', {
 
        'topics': topics if topics else '',
        'assignment': assignment,
        'question_difficulties': question_difficulties
    })  

@transaction.atomic
@login_required(login_url='astros:login')
def delete_question(request, question_id):
    # Making sure the request is done by a professor.
    professor = get_object_or_404(Professor, pk=request.user.id)
    question = get_object_or_404(Question, pk=question_id)
    if not question.assignment.course.professors.filter(pk=request.user.pk).exists():
        return HttpResponseForbidden('You are not authorized delete this question.')
    # delete question
    question.delete()
    if question.assignment.course.name != 'Question Bank':
        renumber_assignment_questions(question.assignment)
    # redirect to assignment management
    return HttpResponseRedirect(reverse("phobos:assignment_management",\
                                            kwargs={'course_id':question.assignment.course.id,\
                                                    'assignment_id':question.assignment.id}))

def renumber_assignment_questions(assignment):
        number = 0
        # Renumber the questions in the assignment.
        for parent_quest in assignment.questions.filter(parent_question=None):
            # Increment number by 1
            number += 1
            sub_questions = list(parent_quest.sub_questions.all())
            sub_questions.insert(0, parent_quest)
            
            for sub_question in sub_questions:
                qnum = sub_question.number 
                if qnum[-1].isalpha():
                    new_num = str(number) + qnum[-1]
                else: 
                    new_num = str(number)
                sub_question.number = new_num
                sub_question.save(update_fields=['number'])


# NOTE: The function below was to be useD for a better front end design of the export question functionality.
# The function was to enable the prof select a course then select an assignment in that course.
#this function raises an ATTRIBUTE ERROR. WHY ???  
# the function work, fix the bug but too late. Might be useful some other time.

# def get_assignments(request, question_id, exp_course_id, assignment_id=None, course_id=None):    # #for Export question implementation
#     course=[] #Course.objects.filter(pk = exp_course_id)
#     assignments=[] #Assignment.objects.filter(course= course[0])
#     content=[]
#     for assignment in assignments:
#         content.append({'assignment_id':assignment.pk,'assignment_name':assignment.name})
#     return JsonResponse("{'assignments':content}")


# Define a mapping of answer types to their corresponding attributes
answer_type_to_attributes = {
    'MCQ': [
        'mcq_expression_answers', 'mcq_text_answers', 'mcq_float_answers',
        'mcq_variable_float_answers', 'mcq_image_answers', 'mcq_latex_answers'
    ],
    'STRUCT':{
        QuestionChoices.STRUCTURAL_EXPRESSION: 'expression_answer',
        QuestionChoices.STRUCTURAL_TEXT: 'text_answer',
        QuestionChoices.STRUCTURAL_FLOAT: 'float_answer',
        QuestionChoices.STRUCTURAL_LATEX: 'latex_answer',
        QuestionChoices.STRUCTURAL_VARIABLE_FLOAT: 'variable_float_answer'
    }
}

@login_required(login_url='astros:login')
def question_view(request, question_id, assignment_id=None, course_id=None):
    # Making sure the request is done by a professor.
    professor = get_object_or_404(Professor, pk=request.user.id)
    assignments=[]                              # actual assignment for Export question implementation
    course= Course.objects.get(pk= course_id)                  #for Export question implementation
    courses= Course.objects.filter(professors=professor)
    if course.professors.filter(pk=request.user.pk).exists() or course.name=='Question Bank':
       show_answer = True
    else:
        show_answer = False
    for course_ in courses: # Watch out variable names here
        assignments.append((course_.id, Assignment.objects.filter(course = course_)))                  #for front-end Export question implementation
        
    question_0 = Question.objects.get(pk=question_id)
    if question_0.parent_question: 
        question_0 = question_0.parent_question
    questions = list(Question.objects.filter(parent_question=question_0))
    questions.insert(0, question_0)

    questions_dictionary = {}
    for index, question in enumerate(questions):
        question.text = replace_links_with_html(question.text)
        # replace_image_labels_with_links() should come after replace_links_with_html()
        labels_urls_list = [(question_image.label, question_image.image.url) for question_image in \
                            question.images.all()]
        question.text = replace_image_labels_with_links(question.text, labels_urls_list)
        question.text = question.text.replace('@{', '')
        question.text = question.text.replace('}@', '')
        answers = []
        qtype = ''
        # Check if the answer type starts with MCQ or STRUCT
        if question.answer_type.startswith('MCQ'):
            qtype = 'mcq'
            for attr in answer_type_to_attributes['MCQ']:
                answer_list = getattr(question, attr).all()
                answers.extend(answer_list)

        elif question.answer_type.startswith('STRUCT'):
            qtype = 'struct'
            attr = answer_type_to_attributes['STRUCT'][question.answer_type]
            answer = getattr(question, attr)
            # Special handling for variable float answers
            if question.answer_type == QuestionChoices.STRUCTURAL_VARIABLE_FLOAT:
                answer.content = answer.content.replace('@{', '').replace('}@', '')
            answers.extend([answer])
            # Set qtype for text answers
            if question.answer_type == QuestionChoices.STRUCTURAL_TEXT:
                qtype = 'fr'
            answers[0].preface = '' if not answers[0].preface else answers[0].preface + "\quad = \quad" # This is to display well in the front end.
            answers[0].answer_unit = '' if not answers[0].answer_unit else "\quad " + answers[0].answer_unit
        elif question.answer_type.startswith('MATCHING'):
            qtype = 'mp'
            answers = question.matching_pairs.all()
        else:
            return HttpResponse('Something went wrong.')
        questions_dictionary[index] = {'question':question,\
                      'show_answer':show_answer,
                     'qtype':qtype,'answers': answers}

    return render(request, 'phobos/question_view.html', {'courses':zip(range(len(courses)),courses),\
                                                         'questions_dict':questions_dictionary, \
                                                         'question':questions[0],
                                                         'assignments':assignments,
                                                         'is_questionbank': True if course.name=='Question Bank' else False })


@login_required(login_url='astros:login') 
def edit_question(request, question_id):
    question = Question.objects.get(pk = question_id)
    question_0 = Question.objects.get(pk=question_id)
    if question_0.parent_question: 
        question_0 = question_0.parent_question
    questions = list(Question.objects.filter(parent_question=question_0))
    questions.insert(0, question_0)
    question_difficulties = ['EASY', 'MEDIUM', 'DIFFICULT']
    questions_dictionary = {}
    js_qtype = ''
    for index, question in enumerate(questions):
        answers = []
        qtype = ''
        # Check if the answer type starts with MCQ or STRUCT
        if question.answer_type.startswith('MCQ'):
            qtype, js_qtype = 'mcq', 'm-answer'
            for attr in answer_type_to_attributes['MCQ']:
                answer_list = getattr(question, attr).all()
                answers.extend(answer_list)
                # Add to is_latex list, 1 if latex answers, else 0
        elif question.answer_type.startswith('STRUCT'):
            qtype = 'struct'
            attr = answer_type_to_attributes['STRUCT'][question.answer_type]
            answer = getattr(question, attr)
            answers.extend([answer])
            # Set qtype for text answers
            if question.answer_type == QuestionChoices.STRUCTURAL_TEXT:
                qtype = 'fr'
            elif question.answer_type in [QuestionChoices.STRUCTURAL_VARIABLE_FLOAT, QuestionChoices.STRUCTURAL_FLOAT]:
                js_qtype = 'f-answer'
            elif question.answer_type == QuestionChoices.STRUCTURAL_EXPRESSION:
                js_qtype = 'e-answer'
            else:
                raise ValueError(f'Expected structural answer type, but got {question.answer_type}')
        elif question.answer_type.startswith('MATCHING'):
            qtype, js_qtype = 'mp', 'mp-answer'
            answers = question.matching_pairs.all()
        else:
            return HttpResponse('Something went wrong.')
        questions_dictionary[index] = {'question':question,\
                     'qtype':qtype,'answers': answers, 'js_qtype':js_qtype,     
                     'answer':answers[0], # for structural
                     }

    return render(request, 'phobos/edit_question.html', {
    'question': questions[0],
    'questions':questions,
    'question_difficulties': question_difficulties,
    'questions_dict':questions_dictionary
    })  



@login_required(login_url='astros:login')  
def manage_enrollment_codes(request, course_id):
    # Making sure the request is done by a professor.
    professor = get_object_or_404(Professor, pk=request.user.id)
    course = get_object_or_404(Course, pk = course_id)
    if not course.professors.filter(pk=request.user.pk).exists():
        return HttpResponseForbidden('You are not authorized to manage the enrollments for this course.')
    return render(request, 'phobos/manage_enrollment_codes.html', {'course':course})



def calci(request):
    return render(request, 'phobos/calci.html')
def sidebar(request):
    return render(request, 'phobos/sidebar.html')

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
    student = Student.objects.get(pk =student_id)
    course = Course.objects.get(pk = course_id)
    assignments = Assignment.objects.filter(course = course)
    grades = []
    for assignment in assignments:
        try:
            grade = AssignmentStudent.objects.get(student=student, assignment=assignment).get_grade()
        except:
            grade = 'None'

        grades.append(grade)
    
    return render(request,'phobos/student_profile.html',\
                {'student_grade': zip(assignments, grades),\
                 'student':student, 'course':course})


def get_questions(request, student_id, assignment_id, course_id=None):
    assignment= Assignment.objects.get(id=assignment_id)
    questions= Question.objects.filter(assignment= assignment ) 
    student= Student.objects.get(id=student_id)
    assignment_student, created = AssignmentStudent.objects.get_or_create(assignment=assignment, student=student)
    question_details=[{'name':assignment.name,'assignment_id':assignment_id,'Due_date':str(assignment_student.due_date).split(' ')[0]}]
    for question in questions:
        if question.answer_type.startswith(('MCQ', 'MATCHING')):
            num_pts = question.mcq_settings.num_points
        else:
            num_pts = question.struct_settings.num_points
        try:
            question_student = QuestionStudent.objects.get(student= student, question=question)
            question_modified_score, is_created= QuestionModifiedScore.objects.get_or_create(question_student=question_student)
            if question_modified_score.is_modified:
                question_details.append({'Question_number':'Question ' + question.number,\
                                    'score':f"{round(question_modified_score.score, 2)} / {num_pts}", \
                                        'num_attempts': question_student.get_num_attempts(),\
                                        'original_score':f"{question_student.get_num_points()} / {num_pts}", \
                                            'id': question_student.pk})
            else:
                        question_details.append({'Question_number':'Question ' + question.number,\
                                    'score':f"{round(question_student.get_num_points(), 2)} / {num_pts}", \
                                        'num_attempts': question_student.get_num_attempts(),\
                                    'original_score':f"{question_student.get_num_points()} / {num_pts}", \
                                            'id': question_student.pk})

        except QuestionStudent.DoesNotExist:
            question_details.append({'Question_number':'Question ' + question.number,\
                                     'score':f"0 / {num_pts}",'num_attempts': "0",\
                                     'original_score':f"0 / {num_pts}",'id': "-1"})    
        
    question_details= json.dumps(question_details)
    return HttpResponse(question_details)

def modify_question_student_score(request,question_student_id,new_score,course_id=None,student_id=None):
    professor = get_object_or_404(Professor, pk=request.user.id)
    course = get_object_or_404(Course, pk = course_id)
    if not course.professors.filter(pk=request.user.pk).exists():
        return HttpResponseForbidden('You are not authorized to change the scores of a student in this course.')
    try:
         new_score= float(new_score)
    except:
         return JsonResponse({'success':False,'result':'Enter a real number'})
    try:
        question_student_id = int(question_student_id)
    except:
        return JsonResponse({'success':False, 'result': 'something went wrong'})
    try:
        question_student= QuestionStudent.objects.get(pk= question_student_id)
    except QuestionStudent.DoesNotExist:
        return JsonResponse({
            'success': False, 'result':"Can't modify grade when student has not even attempted question!"
        })
        # question_student = QuestionStudent.objects.create(question, student) # Needs the question and student
        # question_student.save()
    question_modified_score, is_created= QuestionModifiedScore.objects.get_or_create(question_student=question_student)
    try:
        # print(question_student_id)
        question_modified_score.score= new_score
        question_modified_score.is_modified= True
        question_modified_score.save()
        return JsonResponse({'success':True,'result':'Grade successfully edited.'})
    except:
        return JsonResponse({'success':False,'result':'Something Went Wrong'})

def search_question(request):
    if request.method == 'POST':
        input_text = request.POST.get('search_question','')
        # Tokenize and encode the input text
        max_length = 512  # BERT's maximum sequence length
        input_tokens = BERT_TOKENIZER.encode(input_text, add_special_tokens=True, max_length=max_length, truncation=True, padding='max_length')
        with torch.no_grad():
            input_tensor = torch.tensor([input_tokens])
            attention_mask = (input_tensor != 0).float()  # Create attention mask
            encoded_output = BERT_MODEL(input_tensor, attention_mask=attention_mask)[0]  # Take the hidden states

        # Apply attention-based pooling to encoded output
        encoded_output_pooled = attention_pooling(encoded_output, attention_mask)

        # Retrieve all question objects from the database
        all_questions = Question.objects.all()

        # Calculate cosine similarity with stored question encodings
        similar_questions = []
        for question in all_questions:
            question_encoded_output_pooled = torch.tensor(question.embedding)  # Load pre-computed encoding

            similarity_score = cosine_similarity(encoded_output_pooled, question_encoded_output_pooled).item()
            similar_questions.append({'question': question, 'similarity': similarity_score})

        # Sort by similarity score and get top 10
        top_n = 10
        top_similar_questions = heapq.nlargest(top_n, similar_questions, key=lambda x: x['similarity'])
        return render(request, 'phobos/search_question.html', {'similar_questions': top_similar_questions,\
                                                               'search_text': input_text}) 
                                       

    return render(request,'phobos/search_question.html')

@login_required(login_url='astros:login')
def enrollmentCode(request, course_id, expiring_date):
    # Making sure the request is done by a professor.
    professor = get_object_or_404(Professor, pk=request.user.id)
    course= Course.objects.get(pk = course_id)
    if not course.professors.filter(pk=request.user.pk).exists():
        return JsonResponse({'message': 'You are not allowed to ceate enrollment codes for this course.'})
    min=10000
    max=99999
    enrollment_code = EnrollmentCode(course = course, 
                                     code = random.randint(min,max),
                                      expiring_date = expiring_date)
    enrollment_code.save()
    return JsonResponse({'code': enrollment_code.code,
                         'ex_date':enrollment_code.expiring_date,
                         'message':'enrollment code created successfully'})
    
def display_codes(request,course_id):
    if request.method == "GET":
        course = Course.objects.get(pk= course_id)
        codes= EnrollmentCode.objects.filter(course =  course )
        usable_codes =[]
        for code in codes:
            if code.expiring_date > date.today():
                usable_codes.append({'code':code.code, 
                                    'ex_date':code.expiring_date})
            else:
                code.delete()

        return JsonResponse({'codes':usable_codes})    

@login_required(login_url='astros:login')
def manage_course_info(request,course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return HttpResponseForbidden('COURSE DOES NOT EXIST')
    
    if not course.professors.filter(pk = request.user.pk).exists():
        return HttpResponseForbidden('YOU ARE NOT AUTHORIZED TO MANAGE THIS COURSE')
    course_info, created = CourseInfo.objects.get_or_create(course=course)
    
    def markdown_convert(field):
        return markdown(getattr(course_info, field))

    course_info_markdown_html= {
        'about_course': markdown_convert('about_course'),
        'course_skills': markdown_convert('course_skills'),
        'course_plan': markdown_convert('course_plan'),
        'course_instructors': markdown_convert('course_instructors'),
    }
    return render(request,'phobos/course_info_management.html',{'markdown':course_info_markdown_html ,\
                                                                 'course': course, 'course_info':course_info})

@login_required(login_url='astros:login')
@csrf_exempt
def save_course_info(request, course_id):
 course = Course.objects.get(pk= course_id) 
 if request.method == "POST":
    data = json.loads(request.body.decode("utf-8"))
    info = data.get('text_info')
    category = data.get('category')
    course_info, created = CourseInfo.objects.get_or_create(course=course)

    if category == 'about_course':
        course_info.about_course = info
    elif category == 'course_skills':
        course_info.course_skills = info
    elif category == 'course_plan':
        course_info.course_plan = info
    elif category == 'course_instructors':
        course_info.course_instructors = info
    else:
        return JsonResponse({'error': 'Invalid category'}, status=400)

    course_info.save(update_fields=[category])
    markdown_content = markdown(info)
    return JsonResponse({'message': f'{category} updated successfully', 'md':markdown_content})
 else:
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def copy_question_images(old_question, new_question):
    question_images = QuestionImage.objects.filter(question=old_question)
    for question_image in question_images:
        qi = QuestionImage.objects.create(question=new_question, image=question_image.image, label=question_image.label)
        qi.save()
def copy_variables(old_question, new_question):
    for variable in Variable.objects.filter(question=old_question):
        new_variable = Variable.objects.create(
            question=new_question,
            symbol=variable.symbol
        )
        new_variable.save()
        for var_interval in VariableInterval.objects.filter(variable=variable):
            vi = VariableInterval.objects.create(
                variable=new_variable,
                lower_bound=var_interval.lower_bound,
                upper_bound=var_interval.upper_bound
            )
            vi.save()
        

def copy_answers(old_question, new_question):
    answer_type_mapping = {
        QuestionChoices.STRUCTURAL_EXPRESSION: ExpressionAnswer,
        QuestionChoices.STRUCTURAL_FLOAT: FloatAnswer,
        QuestionChoices.STRUCTURAL_VARIABLE_FLOAT: VariableFloatAnswer,
        QuestionChoices.STRUCTURAL_LATEX: LatexAnswer,
        QuestionChoices.STRUCTURAL_TEXT: TextAnswer,
        # ... add other mappings for structural questions... if created
    }

    answer_type_class = answer_type_mapping.get(old_question.answer_type)
    if answer_type_class:
        answer = answer_type_class.objects.get(question=old_question)
        a = answer_type_class.objects.create(
            question=new_question,
            content=answer.content,
            preface=answer.preface,
            sufface=answer.sufface,
            answer_unit=answer.answer_unit
        )
        a.save()
    elif old_question.answer_type.startswith('MCQ'):
        # Handle MCQ types separately as they have multiple possible answers
        mcq_answer_type_mapping = {
            QuestionChoices.MCQ_EXPRESSION: MCQExpressionAnswer,
            QuestionChoices.MCQ_FLOAT: MCQFloatAnswer,
            QuestionChoices.MCQ_VARIABLE_FLOAT: MCQVariableFloatAnswer,
            QuestionChoices.MCQ_LATEX: MCQLatexAnswer,
            QuestionChoices.MCQ_TEXT: MCQTextAnswer,
            QuestionChoices.MCQ_IMAGE: MCQImageAnswer,
        }
        for answer_type, AnswerClass in mcq_answer_type_mapping.items():
            for answer in AnswerClass.objects.filter(question=old_question):
                new_answer = AnswerClass(
                    question=new_question,
                    content=answer.content,
                    is_answer=answer.is_answer
                )
                if isinstance(new_answer, MCQImageAnswer):
                    new_answer.image = answer.image
                    new_answer.label = answer.label
                
                new_answer.save()
    elif old_question.answer_type.startswith('MATCHING'):
        for answer in old_question.matching_pairs.all():
            new_answer = MatchingAnswer.objects.create(question=new_question)
            new_answer.part_a, new_answer.part_b = answer.part_a, answer.part_b
            new_answer.save()
    else:
        raise ValueError("No answer type match")

@transaction.atomic
@login_required(login_url='astros:login')
def export_question_to(request, question_id, exp_assignment_id, course_id=None, assignment_id=None):
    assignment = get_object_or_404(Assignment, pk=exp_assignment_id)
    question_0 = Question.objects.get(pk=question_id)
    if question_0.parent_question: # if question has no parent question(the question itself 
        question_0 = question_0.parent_question
    questions = list(Question.objects.filter(parent_question=question_0))
    questions.insert(0, question_0)
    q_count = assignment.questions.filter(parent_question=None).count() + 1
    p_question = None
    for index, question in enumerate(questions):    
        new_question = Question(
            number= str(q_count) + chr(65 + index) if index > 0 else str(q_count),
            text= question.text,
            topic= question.topic,
            sub_topic= question.sub_topic,
            assignment= assignment,
            answer_type= question.answer_type
        )

        if index == 0:
            p_question = new_question
        else:
            new_question.parent_question = p_question
        new_question.save(save_settings=True)
        copy_question_images(question, new_question)
        copy_variables(question, new_question)
        copy_answers(question, new_question)
        # Saving the settings.
        if new_question.answer_type.startswith(('MCQ', 'MATCHING')): # if MCQ or Matching pair
            question_settings = new_question.mcq_settings
            question_settings.num_points = question.mcq_settings.num_points
            question_settings.difficulty_level = question.mcq_settings.difficulty_level
            question_settings.mcq_max_num_attempts = question.mcq_settings.mcq_max_num_attempts
            question_settings.mcq_deduct_per_attempt = question.mcq_settings.mcq_deduct_per_attempt
        else:
            question_settings = new_question.struct_settings
            question_settings.units_num_attempts = question.struct_settings.units_num_attempts
            question_settings.max_num_attempts = question.struct_settings.max_num_attempts
            question_settings.percentage_pts_units = question.struct_settings.percentage_pts_units
            question_settings.deduct_per_attempt = question.struct_settings.deduct_per_attempt
            question_settings.margin_error = question.struct_settings.margin_error
            question_settings.num_points = question.struct_settings.num_points
            question_settings.difficulty_level = question.struct_settings.difficulty_level
        question_settings.save()

    return JsonResponse({'message': 'Export Successful', 'success': True}, status=200)
    
    # except ObjectDoesNotExist:
    #    return JsonResponse({'message': 'Export Failed: Object does not exist','success':False}, status=400)
    # except MultipleObjectsReturned:
    #    return JsonResponse({'message': 'Export Failed: Multiple objects returned', 'success': False}, status=400)
    # except Exception as e:
    #    return JsonResponse({'message': f'Export Failed: {str(e)}', 'success': False}, status=500)

    
def change_due_date(assignment, new_date):
    # Assign the timezone-aware datetime to assignment.due_date and save
    assignment.due_date = parse_date(new_date)
    assignment.save()

def parse_date(date):
    # Decode any URL-encoded characters in the date string
    decoded_date = unquote(date)

    # Adjust the format string to handle the new date format with time
    format_string = "%Y-%m-%dT%H:%M" if 'T' in decoded_date else "%Y-%m-%d"

    # Convert the string to a datetime object
    naive_datetime = datetime.strptime(decoded_date, format_string)

    # Make the datetime object timezone-aware
    aware_datetime = timezone.make_aware(naive_datetime)

    return aware_datetime


@transaction.atomic
def edit_student_assignment_due_date(request, course_id, assignment_id, student_id=None):
    try:
        data = json.loads(request.body)
        new_date = data['new_date']
        if student_id:
            student_pks = [student_id]
        else:
            # Ensure that selected_ids are integers if the primary keys are integers
            student_pks = [int(pk) for pk in data['selected_ids']]
        # Get the assignment and the students
        assignment = Assignment.objects.get(pk=assignment_id)
        students = Student.objects.filter(pk__in=student_pks)
        # Create or get AssignmentStudent instances
        assignment_students = [
            AssignmentStudent.objects.get_or_create(assignment=assignment, student=student)[0]
            for student in students
        ]

        # Change the due date for all assignment_students
        for assignment_student in assignment_students:
            assignment_student.due_date = parse_date(new_date)

        # Bulk update all assignment_students
        AssignmentStudent.objects.bulk_update(assignment_students, ['due_date'])

        return JsonResponse({'message': 'Due date successfully edited', 'success': True})

    except Exception as e:
        # Log the exception here
        return JsonResponse({'message': str(e), 'success': False})

def edit_assignment_due_date(request, course_id, assignment_id, new_date):
        assignment= Assignment.objects.get(pk=assignment_id)
        if not assignment.course.professors.filter(pk=request.user.pk).exists():
            return JsonResponse({'message': 'You are not allowed to change the due date', 'success':False})
        assignment.due_date = parse_date(new_date)
        assignment.save()
        assignment_students = AssignmentStudent.objects.filter(assignment= assignment)
        for assignment_student in assignment_students:
            try:
               assignment_student.due_date = parse_date(new_date)
            except:
                return JsonResponse({'message':'something went wrong','success':False})
        AssignmentStudent.objects.bulk_update(assignment_students, ['due_date'])
        return JsonResponse({'message':'Due date successfully edited','success':True})

def edit_course_cover(request):
    if request.method == 'POST':
        course_id= request.POST['course_id']
        new_course_name = request.POST['new_course_name']
        new_course_description = request.POST['new_course_description']
        image = request.FILES.get('new_course_image')
        course = Course.objects.get(pk=course_id)
        course.name = new_course_name
        course.description = new_course_description
        if image:
            new_course_image = default_storage.save(image.name, image)
            course.image = new_course_image
        course.save()

    return HttpResponseRedirect(reverse("phobos:index"))

def edit_course_cover_page(request,course_id):
    course= Course.objects.get(pk=course_id)
    return render(request, "phobos/course_cover.html",{'course':course})

def edit_grading_scheme(request,course_id,assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)  # Don't save to DB yet
    course = assignment.course
    if request.method == 'POST':
            gs_pk = int(request.POST['grading_scheme_pk'])
            if gs_pk == -1:
                # Creating a new grading scheme
                name= request.POST['new_scheme_name']
                # checking if scheme with same name already exists
                exists = GradingScheme.objects.filter(name=name, course=course).exists()
                if exists:
                    old_gs = GradingScheme.objects.get(name=name, course=course)
                    try:
                        name = name + str(int(old_gs.name[-1]) + 1) # Not expecting the
                                                                    # integer to be more than
                                                                    # two digits.
                    except:
                        name = name + str(1)
                scheme = GradingScheme.objects.create(
                    course = course,
                    name= name,
                    num_points = request.POST['num_points'],
                    mcq_num_attempts = request.POST['max_mcq_num_attempts'],
                    struct_num_attempts = request.POST['max_num_attempts'],
                    deduct_per_attempt = request.POST['deduct_per_attempt'],
                    mcq_deduct_per_attempt = request.POST['mcq_deduct_per_attempt'],
                    margin_error = request.POST['margin_error'],
                    percentage_pts_units = request.POST['percentage_pts_units'],
                    units_num_attempts = request.POST['units_num_attempts'],
                    late_sub_deduct = request.POST['late_sub_deduct'],
                    floor_percentage = request.POST['floor_percentage']    
                    )
                scheme.save()
                
            else:
                scheme, is_created = GradingScheme.objects.get_or_create(pk=gs_pk)
                try:
                    scheme.num_points = request.POST['num_points_' + str(gs_pk)]
                    scheme.mcq_num_attempts = request.POST['max_mcq_num_attempts_' + str(gs_pk)]
                    scheme.struct_num_attempts = request.POST['max_num_attempts_' + str(gs_pk)]
                    scheme.deduct_per_attempt = request.POST['deduct_per_attempt_' + str(gs_pk)]
                    scheme.mcq_deduct_per_attempt = request.POST['mcq_deduct_per_attempt_' + str(gs_pk)]
                    scheme.margin_error = request.POST['margin_error_' + str(gs_pk)]
                    scheme.percentage_pts_units = request.POST['percentage_pts_units_' + str(gs_pk)]
                    scheme.units_num_attempts = request.POST['units_num_attempts_' + str(gs_pk)]
                    scheme.late_sub_deduct = request.POST['late_sub_deduct_' + str(gs_pk)]
                    scheme.floor_percentage = request.POST['floor_percentage_' + str(gs_pk)] 
                    scheme.save()
                except:
                    return JsonResponse("Something went wrong. Can't modify scheme")
            assignment.grading_scheme = scheme
            assignment.save()  # Now save to DB
            return HttpResponseRedirect(reverse('phobos:assignment_management',None,None, {'assignment_id':assignment.id, 'course_id':assignment.course.id}))
    else:
        gs_exists = GradingScheme.objects.filter(course=course).exists()
        if not gs_exists:
            default_gs, created = GradingScheme.objects.get_or_create(course=course, name="Default")
            default_gs.save()
        default_gs = GradingScheme.objects.get(course=course, name="Default")
        grading_schemes = list(course.grading_schemes.all())
        grading_schemes.reverse()
    return render(request, 'phobos/grading_scheme.html', {'course':course,
                         'default_gs':default_gs, 'grading_schemes':grading_schemes, 'assignment':assignment})