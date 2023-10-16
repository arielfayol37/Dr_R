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
from .forms import *
from .models import *
from django.shortcuts import get_object_or_404
from django.middleware import csrf
from django.utils.timesince import timesince
from phobos.models import QuestionChoices
import random, string
from sympy import symbols, simplify
import numpy as np
import torch
from sklearn.metrics.pairwise import cosine_similarity
from Dr_R.settings import BERT_TOKENIZER, BERT_MODEL
import heapq
from django.db import transaction
from markdown2 import markdown
import qrcode
import math

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
def course_management(request, course_id, show_gradebook=None):
    course = get_object_or_404(Course, pk=course_id)

    # Check if there is any Enrollment entry that matches the given student and course
    student = get_object_or_404(Student, pk = request.user.pk)
    is_enrolled = Enrollment.objects.filter(student=student, course=course).exists()
    
    # needed student's gradebook
    course_score=0
    assignment_student_grade=[]
    assignment_student = AssignmentStudent.objects.filter(student=student)
    for assignment in assignment_student:
        assignment_student_grade.append({'id':assignment.id,'assignment_student':assignment,'grade':assignment.get_grade()})
        course_score= course_score+ assignment.get_grade()

    if not is_enrolled:
        return HttpResponseForbidden('You are not enrolled in this course.')
    assignments = Assignment.objects.filter(course=course, assignmentstudent__student=student, \
                                            is_assigned=True)
    context = {
        "student":student,
        "assignments": assignments,
        "course": course,
        "assignment_student_grade": assignment_student_grade,
        "course_score": course_score,
        "show_gradebook": show_gradebook
    }
    return render(request, "deimos/course_management.html", context)

@login_required(login_url='astros:login') 
def assignment_management(request, assignment_id, course_id=None):
    # Making sure the request is done by a Student.
    student = get_object_or_404(Student, pk = request.user.pk)
    assignment = get_object_or_404(Assignment, pk = assignment_id)
    questions = Question.objects.filter(assignment = assignment, parent_question=None)
    context = {
        "questions": questions,
        "assignment": assignment
    }
    return render(request, "deimos/assignment_management.html", context)

# TODO: Add the action link in answer_question.html
# TODO: Implement question_view as well.
@login_required(login_url='astros:login')
def answer_question(request, question_id, assignment_id, course_id, student_id=None, upload_note_img=None):
    # Making sure the request is done by a Student.
    if student_id:
        student = get_object_or_404(Student, pk=student_id)
    else:
        student = get_object_or_404(Student, pk=request.user.pk)
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    if assignment.course.name != 'Question Bank':
        is_questionbank = False
        question_ids = assignment.questions.filter(parent_question=None).values_list('id', flat=True)
        question_nums = assignment.questions.filter(parent_question=None).values_list('number', flat=True)
    else:
        is_questionbank = True
        question_ids, question_nums = [], []
    question_0 = Question.objects.get(pk=question_id)
    if not question_0.parent_question: # if question has no parent question(the question itself 
        #is the parent question)
        questions = list(Question.objects.filter(parent_question=question_0))
        questions.insert(0, question_0)
    else:
        question_0 = question_0.parent_question
        questions = list(Question.objects.filter(parent_question=question_0))
        questions.insert(0, question_0)

    questions_dictionary = {}
    for index, question in enumerate(questions):
        question_student, created = QuestionStudent.objects.get_or_create(question=question, student=student)
        if index==0:
            note, note_created = Note.objects.get_or_create(question_student=question_student)
            note_md = markdown(note.content)
        if question.answer_type.startswith('MCQ'):
            too_many_attempts = question_student.get_num_attempts() >= question.mcq_settings.mcq_max_num_attempts
        else:
            too_many_attempts = question_student.get_num_attempts() >= question.struct_settings.max_num_attempts    
        if created:
            question_student.create_instances()
        else:
            if not question_student.instances_created:
                question_student.create_instances()
        question_student.save() 
        # Detect links and replace with html a-tags
        question.text = replace_links_with_html(question.text)
        labels_urls_list = [(question_image.label, question_image.image.url) for question_image in \
                        question.images.all()]
        question.text = replace_image_labels_with_links(question.text,labels_urls_list)
        # Replace vars with values in colored tags.
        question.text = question_student.evaluate_var_expressions_in_text(question.text, add_html_style=True)
        is_mcq = False #nis mcq
        is_fr = False # is free response
        answers = []
        is_latex = []
        question_type = []
        # The dictionary question_type_dict is used for answer validation.
        # So validate_answer() takes the input from the user and kind of compares to this dictionary.
        question_type_dict = {'ea': 0, 'fa':1, 'fva':8,'la':2, 'ta':3, 'ia':7}
        question_type_count = {'ea': 0, 'fa': 0, 'fva':0, 'la': 0, 'ta': 0, 'ia': 0}
        if question.answer_type.startswith('MCQ'):
            is_mcq = True
            ea = question.mcq_expression_answers.all()
            answers.extend(ea)
            ta = question.mcq_text_answers.all()
            answers.extend(ta)
            # Putting before floats because they are not a django character field.
            for answer in answers:
                answer.content = question_student.evaluate_var_expressions_in_text(answer.content, add_html_style=True)
            fa = question.mcq_float_answers.all()
            answers.extend(fa)
            fva = question.mcq_variable_float_answers.all()
            #evaluated_fva = [question_student.evaluate_var_expressions_in_text(mcq_fva.content, add_html_style=True)\
                #for mcq_fva in fva]
            for mcq_fva in fva:
                mcq_fva.content = question_student.evaluate_var_expressions_in_text(mcq_fva.content, add_html_style=True)
            answers.extend(fva)
            ia = question.mcq_image_answers.all()
            answers.extend(ia)
            la = question.mcq_latex_answers.all()
            answers.extend(la)
            
            question_type_keys = ['ea', 'fa', 'fva', 'ta', 'ia', 'la']

            for key in question_type_keys:
                question_type_count[key] = getattr(locals()[key], 'count')()

            # !Important: order matters here. Latex has to be last!
            is_latex = [0 for _ in range(ea.count()+ta.count()+fa.count()+fva.count()+ia.count())]
            is_latex.extend([1 for _ in range(la.count())])
            for q_type in question_type_dict:
                question_type.extend([question_type_dict[q_type] for _ in range(question_type_count[q_type])])
            assert len(is_latex) == len(answers)
            if not question_student.success: # Do not need to randomize the order if student has already passed.
                shuffler = [counter for counter in range(len(answers))]
                random.shuffle(shuffler)  
                is_latex = [is_latex[i] for i in shuffler]
                answers = [answers[i] for i in shuffler]
        else:
            # TODO: Subclass all structural answers to a more general class 
            # so that you may use only one if.
            if question.answer_type == QuestionChoices.STRUCTURAL_LATEX:# Probably never used (because disabled on frontend)
                answers.extend([question.latex_answer])
                is_latex.extend([1]) 
                question_type = [2]  
            elif question.answer_type == QuestionChoices.STRUCTURAL_EXPRESSION:
                answers.extend([question.expression_answer])
                question_type = [0]
            elif question.answer_type == QuestionChoices.STRUCTURAL_VARIABLE_FLOAT:
                answers.extend([question.variable_float_answer])
                question_type = [5]
            elif question.answer_type == QuestionChoices.STRUCTURAL_FLOAT:
                answers.extend([question.float_answer])
                question_type = [1]
            elif question.answer_type == QuestionChoices.STRUCTURAL_TEXT:
                is_fr = True 
                answers.extend([question.text_answer])
                question_type = [4]    
            answers[0].preface = '' if answers[0].preface is None else answers[0].preface
        last_attempt = question_student.attempts.last()
        context = {
            'question':question,
            "is_mcq": is_mcq,
            "is_fr": is_fr, 
            "answers_is_latex_question_type": zip(answers, is_latex, question_type),
            'question_type': question_type, # For structural
            'answer': answers[0],
            'success':question_student.success,
            'too_many_attempts':too_many_attempts,
            'sq_type':question_type[0], # structural question type used in js.
            'last_attempt':last_attempt.submitted_answer if last_attempt else ''

        }
        questions_dictionary[index] = context
    return render(request, 'deimos/answer_question.html',
                  {'questions_dict':questions_dictionary, 'course_id': course_id,
                   'assignment': assignment,'main_question':question_0,
                    'note':note, 'question_ids_nums':zip(question_ids, question_nums),
                    'note_md':note_md,
                    'note_comment': 'Edit Notes' if note.content else 'Add Notes',
                    'upload_note_img':upload_note_img,
                    'temp_note': note.temp_note if upload_note_img==1 else None,
                    'is_questionbank': is_questionbank})


def validate_answer(request, question_id, landed_question_id=None,assignment_id=None, course_id=None, student_id=None, upload_note_img=None):
    # landed_question_id is just the id of the question used to get to the page
    # to answer questions. Could have been the id of the main question or other sub questions.
    if not student_id:
        student = get_object_or_404(Student, pk=request.user.pk)
    else:
        student = get_object_or_404(Student, pk=student_id)
    
    if request.method == 'POST':
        correct = False
        previously_submitted = False
        data = json.loads(request.body)
        simplified_answer = data["answer"]
        submitted_answer = data["submitted_answer"]
        question = Question.objects.get(pk=question_id)
        feedback_data = ''
        
        # Use get_or_create() to avoid duplicating QuestionStudent instances
        # Normally, we should just use get() because QuestionStudent object is already created
        # whenever the user opens a question for the first time, but just to be safe.
        question_student, created = QuestionStudent.objects.get_or_create(student=student, question=question)
        if data["questionType"].startswith('structural'):
            too_many_attempts = question_student.get_num_attempts() >= question.struct_settings.max_num_attempts
        else:
            too_many_attempts = question_student.get_num_attempts() >= question.mcq_settings.mcq_max_num_attempts
        if ( not (too_many_attempts or question_student.success)):
            if data["questionType"].startswith('structural'):

                if question.answer_type == QuestionChoices.STRUCTURAL_EXPRESSION:
                    # checking previous attempts
                    for previous_attempt in question_student.attempts.all():
                        if compare_expressions(previous_attempt.content, simplified_answer):
                            previously_submitted = True
                            return JsonResponse({'previously_submitted': previously_submitted})
                    attempt = QuestionAttempt.objects.create(question_student=question_student)
                    attempt.content = simplified_answer
                    attempt.submitted_answer = submitted_answer
                    answer = question.expression_answer
                    correct = compare_expressions(answer.content, simplified_answer)
                elif question.answer_type in [QuestionChoices.STRUCTURAL_FLOAT, QuestionChoices.STRUCTURAL_VARIABLE_FLOAT]:
                    if question.answer_type == QuestionChoices.STRUCTURAL_FLOAT:
                        answer_content, units = question.float_answer.content, question.float_answer.answer_unit
                    else:
                        answer_content, units = question_student.compute_structural_answer(), question.variable_float_answer.answer_unit
                        
                    try:
                        correct, feedback_data = compare_floats(answer_content, simplified_answer, question.struct_settings.margin_error)
                    except ValueError:
                        correct = False
                        
                    if not correct:
                        for prev_attempt in question_student.attempts.all():
                            are_the_same, _ = compare_floats(prev_attempt.content, simplified_answer, margin_error=0.02, get_feedback=False)
                            if are_the_same:
                                return JsonResponse({'previously_submitted': True})
                    
                    attempt = QuestionAttempt.objects.create(question_student=question_student)
                    attempt.content = simplified_answer
                    attempt.submitted_answer = submitted_answer

                if correct:
                    attempt.num_points = max(0, question.struct_settings.num_points * \
                                                 (1 - question.struct_settings.deduct_per_attempt *
                                                   max(0, question_student.get_num_attempts() - 1)))
                    question_student.success = True
                    attempt.success = True
                question_student.save()  # Save the changes to the QuestionStudent instance
                attempt.save()
            elif data["questionType"] == 'mcq':
                # retrieve list of 'true' mcq options
                # !important: mcq answers of different type may have the same primary key.
                
                # checking previous attempts
                for previous_attempt in question_student.attempts.all():
                    if set(simplified_answer) == set(eval(previous_attempt.content)):
                        previously_submitted = True
                        return JsonResponse({'previously_submitted': previously_submitted})
                attempt = QuestionAttempt.objects.create(question_student=question_student)
                attempt.content = str(simplified_answer)
                question_type_dict = {'ea': 0, 'fa':1, 'fva':8,'la':2, 'ta':3, 'ia':7}
                answers = []
                ea = list(question.mcq_expression_answers.filter(is_answer=True).values_list('pk', flat=True))
                ea = [str(pk) + str(question_type_dict['ea']) for pk in ea]
                answers.extend(ea)
                ta = list(question.mcq_text_answers.filter(is_answer=True).values_list('pk', flat=True))
                ta = [str(pk) + str(question_type_dict['ta']) for pk in ta]
                answers.extend(ta)
                fa = list(question.mcq_float_answers.filter(is_answer=True).values_list('pk', flat=True))
                fa = [str(pk) + str(question_type_dict['fa']) for pk in fa]
                answers.extend(fa)
                fva = list(question.mcq_variable_float_answers.filter(is_answer=True).values_list('pk', flat=True))
                fva = [str(pk) + str(question_type_dict['fva']) for pk in fva]
                answers.extend(fva)
                la = list(question.mcq_latex_answers.filter(is_answer=True).values_list('pk', flat=True))
                la = [str(pk)+ str(question_type_dict['la']) for pk in la]
                answers.extend(la)
                ia = list(question.mcq_image_answers.filter(is_answer=True).values_list('pk', flat=True))
                ia = [str(pk) + str(question_type_dict['ia']) for pk in ia]
                answers.extend(ia)
                if len(simplified_answer) == len(answers):
                    s1, s2 = set(simplified_answer), set(answers)
                    if s1 == s2:
                        correct = True
                        attempt.num_points = max(0, question.mcq_settings.num_points * \
                                                 (1 - question.mcq_settings.mcq_deduct_per_attempt *
                                                   max(0, question_student.get_num_attempts() - 1)))
                        question_student.success = True
                        attempt.success = True
                question_student.save()
                attempt.save()
        # Return a JsonResponse
        return JsonResponse({
            'correct': correct,
            'too_many_attempts': too_many_attempts,
            'previously_submitted':previously_submitted,
            'feedback_data': feedback_data
        })
    


           
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"].strip()
        password = request.POST["password"].strip()
        try:
            user = Student.objects.get(email=email)
        except Student.DoesNotExist:
            user = None

        # Authenticate the user based on the provided email and password
        if user is not None and user.check_password(password):
            # If authentication successful, log in the user
            login(request, user)
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)
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

def forgot_password(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data["email"]
            password= data['new_password']
            confirmPwd= data['confirm_new_password']

            try:
                user = Student.objects.get(email=email)
            except Student.DoesNotExist:
               return JsonResponse({'success':False,
                         'message':"Hacker don't hack in here. Email does not exist"})
            if password == confirmPwd:
                user.set_password(password)
                user.save()
                return JsonResponse({'success':True,
                    'message':'Password Succesfully changed'})
        except:
            pass
    return JsonResponse({'success':False,
                         'message':'Something went wrong'})


def register(request):
    if request.method == "POST":
        username = request.POST["username"].strip()
        email = request.POST["email"].strip()
        password = request.POST["password"].strip()
        first_name = request.POST["first_name"].strip()
        last_name = request.POST["last_name"].strip()
        try:
            checking_student = Student.objects.get(email=email)
            if checking_student:
                return render(request, "astros/register.html", {
                "message": "Student profile with this email already exists."
            })
        except Student.DoesNotExist:
            pass
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


#---------HELPER FUNCTIONS--------------------------------------------------------
def expression_compare_test(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        e1 = data['expression_1']
        e2 = data['expression_2']
        mode = data['mode']
        if mode == 'units':
            return JsonResponse({'correct': compare_units(e1,e2)})
        else:
            return JsonResponse({'correct': compare_expressions(e1,e2)})
    return render(request, 'deimos/expression_compare_test.html')
def is_student_enrolled(student_id, course_id):
    # Retrieve the Student and Course instances based on their IDs
    student = get_object_or_404(Student, pk=student_id)
    course = get_object_or_404(Course, pk=course_id)

    # Check if there is any Enrollment entry that matches the given student and course
    is_enrolled = Enrollment.objects.filter(student=student, course=course).exists()

    return is_enrolled


def  extract_numbers(text):
    """
    Returns a list of numbers and subscrippted characters in a string.
    # E.g of a subscriptted char: 'e_1'
    """
    # Regular expression pattern to match numbers and subscriptted chars.
    
    pattern = r'[-+]?\d*\.\d+|\d+|\w+_\w+'
    
    # Find all matches using the pattern
    matches = re.findall(pattern, text)
    
    return matches

def compare_expressions(expression1, expression2, for_units=False):
    """
    Given two strings e1 and e2,
    returns True if they are algebraically equivalent,
    returns False otherwise.
    """
    if not for_units:
        e1 = transform_expression(expression1)
        e2 = transform_expression(expression2)
        if not (isinstance(e1, str) and isinstance(e2, str)):
            raise ValueError("Both inputs should be strings")
    else:
        e1, e2 = expression1, expression2
    symbols_union = set(e1) | set(e2)  # Combined set of symbols from both expressions
    symbols_union.update(extract_numbers(e1 + e2))  # Update with extracted numbers
    symbls = symbols(' '.join(symbols_union), real=True, positive=True)
    sym_e1 = simplify(e1, symbols=symbls)
    sym_e2 = simplify(e2, symbols=symbls)
    difference = (simplify(sym_e1 - sym_e2, symbols=symbls))
    return True if difference == 0 else False

def compare_floats(correct_answer, simplified_answer, margin_error=0.0, get_feedback=True):
    """
    Takes two floats f1 and f2,
    returns True if they are equal or close,
    returns False otherwise
    """
    f1 = eval(str(correct_answer))
    f2 = eval(str(simplified_answer))
    feedback_message = ""
    correct = (abs(f1-f2) <= margin_error * abs(f1)) and f1*f2 >= 0
    if not correct and get_feedback:
        feedback_message = feedback_floats(f1, f2, margin_error) 
    return (correct, feedback_message)

def feedback_floats(base_float, inputed_float, margin_error):
    """
    Helper function that returns a feedback message when two floats
    differ but may be integer multiples (within n=2) of each other.
    Margin error is a percentage.
    """
    assert 0 <= margin_error <= 1
    abs_quotient = abs(inputed_float)/abs(base_float) if base_float != 0 and inputed_float!= 0 else 0
    if abs_quotient == 0:
        return ""
    def check_int_interval(a, b):
        # Checking whether there is an integer between a and b
        if not a < b:
            a, b = b, a
        f_a = math.floor(a)
        f_b = math.floor(b)
        diff = abs(f_b - f_a)
        if a == b and (f_a - a) == 0:
            return int(a)
        if type(diff) == int and diff != 0:
            return f_a + diff
        else:
            return None
    sign = "-" if base_float * inputed_float < 0 else ""    
    a_0 = abs_quotient * (1 - margin_error)
    b_0 = abs_quotient * (1 + margin_error)
    n_0 = check_int_interval(a_0, b_0)
    if n_0 and n_0 < 3:
        return f"Your answer is {sign}{n_0}x the correct answer"
    a_1 = (abs_quotient)**-1 * (1 - margin_error)
    b_1 = (abs_quotient)**-1 * (1 + margin_error)
    n_1 = check_int_interval(a_1, b_1)
    if n_1 and n_1 < 3:
        return f"Your answer is {sign}{n_1 ** -1}x the correct answer"
    # Checking for 10^n submission mistake
    a = math.log10(abs_quotient * (1 - margin_error))
    b = math.log10(abs_quotient * (1 + margin_error))
    n = check_int_interval(a, b)
    if n:
        return f"Your answer is {sign}10^{n} x the correct answer"
    return ""
    
def compare_units(units_1, units_2):
    """
    Takes two units units_1 and units_2
    returns True if they are equivalent
    returns False otherwise
    """
    
    # custom_base_units = ['m', 's', 'cd', 'K', 'mol', 'g', 'A']
    scales = {'k':'10^3', 'u':'10^-6', 'm_':'10^-3', 'p':'10^-12', 'M':'10^6', 'n':'10^-9','µ':'10^-6'}
    # Important! Hz must come before H, as well as Sv before S, Wb before W etc
    correspondances = {
        'C': 'A*s', 'V': 'k*g*m^2*s^-3*A^-1','Ω': 'k*g m^2*s^-3*A^-2',
        'T': 'k*g*s^-2*A^-1','Hz': 's^-1','Pa': 'k*g*m^-1*s^-2','N': 'k*g*m*s^-2','J': 'k*g*m^2*s^-2',
        'Wb':'k*g*m^2*A*s^-2','W': 'k*g*m^2*s^-3', 'F':'k*g*A^2*s^4*m^-2', 'H':'k*g*m^2*A^2*s^-2',
        'Sv':'m^2*s^-2','S':'k*g*s^3*A^2*m^-2', 'lx':'cd*m^-2', 'Bq':'s^-1', 'Gy':'m^2*s^-2', 'kat':'mol*s^-1',
        'atm':'101325*k*g*m^-1*s^-2'
    }
    # transform_units_expression() must be done before to replacing the correspondances
    # and scales to reduce runtime.
    units_1 = transform_units_expression(units_1)
    units_2 = transform_units_expression(units_2)

    for key, value in correspondances.items():
        units_1 = units_1.replace(key, value)
        units_2 = units_2.replace(key, value)
    for key, value in scales.items():
        units_1 = units_1.replace(key, value)
        units_2 = units_2.replace(key, value)
    return compare_expressions(units_1, units_2, for_units=True)

def transform_units_expression(expr):
    """Insert multiplication signs between combined characters, except within trig functions."""
    expression = remove_extra_spaces_around_operators(expr)
    expression = expression.replace(', ', '')
    expression = expression.replace(' ', '*')
    expression = re.sub(r'1e\+?(-?\d+)', r'10^\1', expression)
    # replacements are units that are more than 1 character. e.g Hz, Pa, cd, mol
    replacements = {
        'cd': 'ò', 'mol': 'ë', 'Hz': 'à', 'Pa': 'ê','Wb': 'ä',
        'lx': 'Bq', 'Gy': 'ù', 'Sv': 'ô', 'kat': 'ü', 'atm':'у́'
    }

    expression = encode(expression, replacements)
    transformed_expression = ''.join(
        char if index == 0 or not needs_multiplication(expression, index, replacements)
        else '*' + char for index, char in enumerate(expression)
    )
    transformed_expression = transformed_expression.replace('^', '**')
    return decode(transformed_expression, replacements)
    
def replace_links_with_html(text):
    """
    Find linkes in text and return text with those links
    within html a-tags.
    """
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

def replace_vars_with_values(text, variable_dict):
    # Deprecated
    """
    Find variables in text, and replace with highlited/colored values of instances.
    """
    for var_symbol in variable_dict:
        # TODO: !Important Make the replacements only when the text has something 
        # to indicate that a certain sequence of string will contain
        # variables. Perhaps  {}
        text = text.replace(var_symbol,f"<em class=\"variable\">{variable_dict[var_symbol]}</em>")
    return text

def replace_image_labels_with_links(text, labels_url_pairs):
    """
    Returns the text with labels within html link tags.
    labels_url_pairs = ("john_image", "astros/images/jjs.png")
    """
    for label, url in labels_url_pairs:
        replacement = f"<a href=\"#{url}\">{label}</a>"
        text = text.replace(label, replacement)
    return text
#--------------------Depecrated functions used in development--------------------
def question_nav(request):
    return render(request, 'deimos/question_nav.html', {})

def action_menu(request):
    return render(request, 'deimos/action_menu.html', {})

def attention_pooling(hidden_states, attention_mask):
    # Apply attention mask to hidden states
    attention_mask_expanded = attention_mask.unsqueeze(-1).expand(hidden_states.size())
    masked_hidden_states = hidden_states * attention_mask_expanded
    
    # Calculate attention scores and apply softmax
    attention_scores = torch.nn.functional.softmax(masked_hidden_states, dim=1)
    
    # Weighted sum using attention scores
    pooled_output = (masked_hidden_states * attention_scores).sum(dim=1)
    return pooled_output

def search_question(request):
    if request.method == 'POST':
        input_text = request.POST.get('search_question', '')

        # Tokenize and encode the input text
        input_tokens = BERT_TOKENIZER.encode(input_text, add_special_tokens=True)
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
        return render(request, 'deimos/search_question.html', {'similar_questions': top_similar_questions,\
                                                               'search_text': input_text}) 
                                       

    return render(request,'deimos/search_question.html')


@csrf_exempt
def save_note(request, question_id, course_id=None, assignment_id=None, student_id=None, upload_note_img=None):
    if request.method == "POST":
        requester_id = request.user.pk
        if not student_id: 
            student = get_object_or_404(Student, pk = requester_id)
        else:
            student = get_object_or_404(Student, pk=student_id)
        question = get_object_or_404(Question, pk = question_id)
        if question.parent_question is None: # Notes should be related only to the parent question.
            main_question = question
        else:
            main_question = question.parent_question
        question_student = get_object_or_404(QuestionStudent, student=student, question=main_question)
        if question_student.student.pk != requester_id and student_id is None:
            return JsonResponse({'message': "You are not allowed to manage these notes", "success":False})
        with transaction.atomic():
            note, created = Note.objects.get_or_create(question_student=question_student)
            content = request.POST.get('content')
            note.content = content
            note.save()
            
            # DELETING UNKEPT IMAGES

            # Get a list of kept image primary keys from the request.
            kept_images_pk_list = request.POST.get('kept_images_pk').split(',')
            if kept_images_pk_list[0] == '':
                kept_images_pk_list = []
            kept_images_pk_list = [int(pk) for pk in kept_images_pk_list]
            # Get a list of all current NoteImage primary keys.
            note_images_pk_list = list(NoteImage.objects.filter(note=note).values_list('pk', flat=True))

            # Compute the difference.
            difference = set(note_images_pk_list) - set(kept_images_pk_list)
            # If there are any primary keys in the difference, delete the corresponding NoteImage objects.
            if difference:
                NoteImage.objects.filter(pk__in=difference).delete()


            # SAVING NEW IMAGES

            for key, value in request.FILES.items():
                if key.startswith('question_image'):
                    note_image = NoteImage.objects.create(image=value, note=note)
                    note_image.save()
            md = markdown(content)
                
        return JsonResponse({'message': 'Notes successfully saved', 'success': True, 'md':md,\
                             'last_edited':note.last_edited})
    else:
        return JsonResponse({'message': f'Error: Expected POST method, not {request.method}', 'success':False})
@csrf_exempt    
def generate_note_qr(request, question_id, course_id, assignment_id, student_id=None, upload_note_img=None):
    data = json.loads(request.body)
    question = get_object_or_404(Question,pk=question_id)
    student = get_object_or_404(Student,pk=request.user.id)
    question_student = QuestionStudent.objects.get(question=question, student=student)
    data_temp_note = data['temp_note']
    base_link = data['base_link']
    if data['same_url']:
        custom_link = base_link
    else:
        custom_link = f"{base_link}/{request.user.pk}/1"
    note = Note.objects.get(question_student=question_student)
    temp_note, created = NoteTemporary.objects.get_or_create(note=note)
    temp_note.content = data_temp_note
    temp_note.save()
    img = qrcode.make(custom_link)  # replace with your custom link
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response

@login_required(login_url='astros:login')
def assignemt_gradebook_student(request,student_id, assignment_id):

    assignment_student, created = AssignmentStudent.objects.get_or_create(pk=assignment_id)
    course= assignment_student.assignment.course.id

    questions= Question.objects.filter(assignment= assignment_student.assignment ) 
    student= Student.objects.get(pk=student_id)
    assignments= AssignmentStudent.objects.filter(student=student)

    assignment_details={'name':assignment_student.assignment.name,'assignment_id':assignment_id,\
                        'Due_date':str(assignment_student.due_date).split(' ')[0],'grade':assignment_student.get_grade() }
    
    question_heading=['Question_number','score','num_attempts']
    question_details=[]
    for question in questions:
        if question.answer_type.startswith('MCQ'):
            nm_pts = question.mcq_settings.num_points
        else:
            nm_pts = question.struct_settings.num_points
        try:
            question_student = QuestionStudent.objects.get(student= student, question=question)
            question_modified_score, is_created= QuestionModifiedScore.objects.get_or_create(question_student=question_student)

            if question_modified_score.is_modified:
                question_details.append({'Question_number':'Question ' + question.number,\
                                    'score':f"{round(question_modified_score.score, 2)} / {nm_pts}", \
                                        'num_attempts': question_student.get_num_attempts()})
            else:
                        question_details.append({'Question_number':'Question ' + question.number,\
                                    'score':f"{round(question_student.get_num_points(), 2)} / {nm_pts}", \
                                        'num_attempts': question_student.get_num_attempts()})
        except QuestionStudent.DoesNotExist:
            question_details.append({'Question_number':'Question ' + question.number,\
                                     'score':f"0 / {nm_pts}",'num_attempts': "0"})    

    context={
        'question_details':question_details,
        'question_heading':question_heading,
        'assignment': assignment_details,
        'assignments':assignments,
        'student': student,
        'course_id':course
        }
                  
    return render(request,'deimos/assignment_gradebook.html',context)


@login_required(login_url='astros:login') 
def note_management(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    # Check if there is any Enrollment entry that matches the given student and course
    student = get_object_or_404(Student, pk = request.user.pk)
    is_enrolled = Enrollment.objects.filter(student=student, course=course).exists()
    
    if not is_enrolled:
        return HttpResponseForbidden('You are not enrolled in this course.')
    assignments = Assignment.objects.filter(course=course, assignmentstudent__student=student, \
                                            is_assigned=True)
    # this is needed to display notes
    Notes = Note.objects.all()
    notes=[]
    for note in Notes:
        if note.question_student.student == student:
             notes.append({'Note':note,"note_md":markdown(note.content)})
    
    context = {
        "student":student,
        "assignments": assignments,
        "course": course,
        "notes": notes,
    }
    return render(request, "deimos/note_management.html", context)
