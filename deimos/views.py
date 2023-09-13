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
from phobos.models import QuestionChoices
import random
from sympy import symbols, simplify
import numpy as np
import torch
from sklearn.metrics.pairwise import cosine_similarity
from Dr_R.settings import BERT_TOKENIZER, BERT_MODEL
import heapq

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
    assignment_student, created = AssignmentStudent.objects.get_or_create(student = student, assignment=assignment)
    assignment_student.save()
    # TODO: Do delete the following code in comment.
    """
    is_assigned = AssignmentStudent.objects.filter(student=student, assignment=assignment).exists()
    if not is_assigned:
        return HttpResponseForbidden('You have not be assigned this assignment.')
    
    """

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
    too_many_attempts = question_student.get_num_attempts() >= question.max_num_attempts
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
    question_type_dict = {'ea': 0, 'fa':1, 'la':2, 'ta':3, 'ia':7}
    question_type_count = {'ea': 0, 'fa': 0, 'la': 0, 'ta': 0, 'ia': 0}
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
        ia = question.mcq_image_answers.all()
        answers.extend(ia)
        la = question.mcq_latex_answers.all()
        answers.extend(la)
        
        question_type_count['ea'] = ea.count()
        question_type_count['fa'] = fa.count()
        question_type_count['la'] = la.count()
        question_type_count['ta'] = ta.count()
        question_type_count['ia'] = ia.count()
        # !Important: order matters here. Latex has to be last!
        is_latex = [0 for _ in range(ea.count()+ta.count()+fa.count()+ia.count())]
        is_latex.extend([1 for _ in range(la.count())])
        for q_type in question_type_dict:
            question_type.extend([question_type_dict[q_type] for _ in range(question_type_count[q_type])])
        assert len(is_latex) == len(answers)
        shuffler = [counter for counter in range(len(answers))]
        random.shuffle(shuffler)  
        is_latex = [is_latex[i] for i in shuffler]
        answers = [answers[i] for i in shuffler]

    # TODO: Subclass all structural answers to a more general class 
    # so that you may use only one if.
    elif question.answer_type == QuestionChoices.STRUCTURAL_LATEX:# Probably never used (because disabled on frontend)
        answers.extend(question.latex_answers.all())
        is_latex.extend([1 for _ in range(question.latex_answers.all().count())]) 
        question_type = [2]  
    elif question.answer_type == QuestionChoices.STRUCTURAL_EXPRESSION:
        answers.extend(question.expression_answers.all())
        question_type = [0]
    elif question.answer_type == QuestionChoices.STRUCTURAL_VARIABLE_FLOAT:
        answers.extend(question.variable_float_answers.all())
        question_type = [5]
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
        'answer': answers[0],
        'success':question_student.success,
        'too_many_attempts':too_many_attempts,
        'sq_type':question_type[0], # structural question type used in js.
    }
    return render(request, 'deimos/answer_question.html',
                  context)
@login_required(login_url='astros:login')
def validate_answer(request, question_id, assignment_id=None, course_id=None):
    student = get_object_or_404(Student, pk=request.user.pk)
    
    if request.method == 'POST':
        correct = False
        previously_submitted = False
        data = json.loads(request.body)
        submitted_answer = data["answer"]
        question = Question.objects.get(pk=question_id)
        
        # Use get_or_create() to avoid duplicating QuestionStudent instances
        # Normally, we should just use get() because QuestionStudent object is already created
        # whenever the user opens a question for the first time, but just to be safe.
        question_student, created = QuestionStudent.objects.get_or_create(student=student, question=question)
        
        too_many_attempts = question_student.get_num_attempts() >= question.max_num_attempts
        if ( not (too_many_attempts or question_student.success)):
            if data["questionType"].startswith('structural'):

                if question.answer_type == QuestionChoices.STRUCTURAL_EXPRESSION:
                    # checking previous attempts
                    for previous_attempt in question_student.attempts.all():
                        if compare_expressions(previous_attempt.content, submitted_answer):
                            previously_submitted = True
                            return JsonResponse({'previously_submitted': previously_submitted})
                    assert question.expression_answers.count() == 1
                    attempt = QuestionAttempt.objects.create(question_student=question_student)
                    attempt.content = submitted_answer
                    answer = question.expression_answers.first()
                    correct = compare_expressions(answer.content, submitted_answer)
                elif question.answer_type == QuestionChoices.STRUCTURAL_FLOAT:
                    # Checking previous attempts
                    for previous_attempt in question_student.attempts.all():
                        if compare_floats(previous_attempt.content,submitted_answer):
                            previously_submitted = True
                            return JsonResponse({'previously_submitted': previously_submitted})
                    attempt = QuestionAttempt.objects.create(question_student=question_student)
                    attempt.content = submitted_answer
                    assert question.float_answers.count() == 1
                    answer = question.float_answers.first()
                    try:
                        # answer.content must come first in the compare_floats()
                        correct = compare_floats(answer.content, submitted_answer, question.margin_error) 
                    except ValueError:
                        # TODO: Maybe return a value to the user side that will ask them to enter a float.
                        # TODO: Actually, ensure this on the front-end.
                        correct = False
                elif question.answer_type == QuestionChoices.STRUCTURAL_VARIABLE_FLOAT:
                    # Checking previous attempts
                    for previous_attempt in question_student.attempts.all():
                        if compare_floats(previous_attempt.content,submitted_answer):
                            previously_submitted = True
                            return JsonResponse({'previously_submitted': previously_submitted})
                    attempt = QuestionAttempt.objects.create(question_student=question_student)
                    attempt.content = submitted_answer
                    try:
                        answer_temp = question_student.compute_structural_answer()
                        correct = compare_floats(answer_temp, submitted_answer,
                                                    question.margin_error)
                    except ValueError:
                        correct = False
                if correct:
                    # Deduct points based on attempts, but ensure it doesn't go negative
                    attempt.num_points = max(0, question.num_points - (question.deduct_per_attempt * question_student.get_num_attempts()))
                    question_student.success = True
                    attempt.success = True
                    
                question_student.save()  # Save the changes to the QuestionStudent instance
                attempt.save()
            elif data["questionType"] == 'mcq':
                # retrieve list of 'true' mcq options
                # !important: mcq answers of different type may have the same primary key.
                
                # checking previous attempts
                for previous_attempt in question_student.attempts.all():
                    if set(submitted_answer) == set(previous_attempt.content):
                        previously_submitted = True
                        return JsonResponse({'previously_submitted': previously_submitted})
                attempt = QuestionAttempt.objects.create(question_student=question_student)
                attempt.content = str(submitted_answer)
                question_type_dict = {'ea': 0, 'fa':1, 'la':2, 'ta':3, 'ia':7}
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
                la = list(question.mcq_latex_answers.filter(is_answer=True).values_list('pk', flat=True))
                la = [str(pk)+ str(question_type_dict['la']) for pk in la]
                answers.extend(la)
                ia = list(question.mcq_image_answers.filter(is_answer=True).values_list('pk', flat=True))
                ia = [str(pk) + str(question_type_dict['ia']) for pk in ia]
                answers.extend(ia)
                if len(submitted_answer) == len(answers):
                    if set(submitted_answer) == set(answers):
                        correct = True
                        attempt.num_points = max(0, question.num_points * (1 - (question.deduct_per_attempt * question_student.get_num_attempts())))
                        question_student.success = True
                        attempt.success = True
                question_student.save()
                attempt.save()
        # Return a JsonResponse
        return JsonResponse({
            'correct': correct,
            'too_many_attempts': too_many_attempts,
            'previously_submitted':previously_submitted
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
                "message": "Username/email already taken."
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

def compare_expressions(expression1, expression2):
    """
    Given two strings e1 and e2,
    returns True if they are algebraically equivalent,
    returns False otherwise.
    """
    e1 = transform_expression(expression1)
    e2 = transform_expression(expression2)
    if not (isinstance(e1, str) and isinstance(e2, str)):
        raise ValueError("Both inputs should be strings")

    symbols_union = set(e1) | set(e2)  # Combined set of symbols from both expressions
    symbols_union.update(extract_numbers(e1 + e2))  # Update with extracted numbers
    symbls = symbols(' '.join(symbols_union), real=True, positive=True)
    sym_e1 = simplify(e1, symbols=symbls)
    sym_e2 = simplify(e2, symbols=symbls)
    difference = (simplify(sym_e1 - sym_e2, symbols=symbls))
    return True if difference == 0 else False

def compare_floats(correct_answer, submitted_answer, margin_error=0.0):
    """
    Given two floats f1 and f2,
    returns True if they are equal or close,
    returns False otherwise
    """
    f1 = eval(str(correct_answer))
    f2 = eval(str(submitted_answer))
    if f1 == 0:
        return f1-f2 <= margin_error
    else:
        return abs(f1-f2)/f1 <= margin_error

    
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
