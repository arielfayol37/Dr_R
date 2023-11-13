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
from .forms import *
from .models import *
from django.shortcuts import get_object_or_404
from django.middleware import csrf
from django.utils.timesince import timesince
from phobos.models import QuestionChoices
import random
import numpy as np
import torch
from sklearn.metrics.pairwise import cosine_similarity
from Dr_R.settings import BERT_TOKENIZER, BERT_MODEL
import heapq
from django.db import transaction
from markdown2 import markdown
from phobos.models import Topic, SubTopic
import qrcode
from phobos.views import export_question_to
from scipy.stats import norm
from .utils import *
from datetime import date

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

    assignments = Assignment.objects.filter(course=course, assignmentstudent__student=student, \
                                            is_assigned=True)
    context = {
        "student":student,
        "assignments": assignments,
        "course": course,
    }
    return render(request, "deimos/course_management.html", context)

@login_required(login_url='astros:login')
def gradebook(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    # Check if there is any Enrollment entry that matches the given student and course
    student = get_object_or_404(Student, pk = request.user.pk)
    is_enrolled = Enrollment.objects.filter(student=student, course=course).exists()
    if not is_enrolled:
        return HttpResponseForbidden('You are not enrolled in this course.')
    # needed student's gradebook
    course_score=0
    assignment_student_grade=[]
    assignment_student = AssignmentStudent.objects.filter(student=student, assignment__course=course)
    a_sums = 0
    for assignment_s in assignment_student:
        grade = assignment_s.get_grade()
        assignment_student_grade.append({'id':assignment_s.id,'assignment_student':assignment_s,'grade':grade})
        course_score += assignment_s.assignment.num_points * grade
        a_sums += assignment_s.assignment.num_points
    if a_sums == 0:
        course_score = 0
    else:
        course_score /= a_sums

    return render(request, 'deimos/gradebook.html', {
        'student': student, 'course':course,
                "assignment_student_grade": assignment_student_grade,
        "course_score": round(course_score, 2),
    })

@login_required(login_url='astros:login') 
def assignment_management(request, assignment_id, course_id=None):
    # Making sure the request is done by a Student.
    student = get_object_or_404(Student, pk = request.user.pk)
    assignment = get_object_or_404(Assignment, pk = assignment_id)
    questions = Question.objects.filter(assignment = assignment, parent_question=None)
    question_students = []
    if assignment.course != 'Question Bank':
        for question in questions:
            qs, created = QuestionStudent.objects.get_or_create(question=question, student=student)
            question_students.append(qs)
            question.text = qs.evaluate_var_expressions_in_text(question.text, add_html_style=True)
    else:
        question_students = [i for i in range(questions.count())] # here for templating purposes.
    context = {
        "questions": zip(questions, question_students),
        "assignment": assignment,
    }
    return render(request, "deimos/assignment_management.html", context)

# List of all answer types
all_mcq_answer_types = {
    'ea': ('mcq_expression_answers', 0),
    'ta': ('mcq_text_answers',3),
    'fa':('mcq_float_answers',1),
    'fva': ('mcq_variable_float_answers',8),
    'ia': ('mcq_image_answers',7),
    'la': ('mcq_latex_answers',2),
}
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
        questtype = ''
        answers = []
        answers_c = None

        if question.answer_type.startswith('MCQ'):
            questtype='mcq'
            # List of answer types that require content evaluation
            answer_types_to_evaluate = ['mcq_expression_answers', 'mcq_variable_float_answers']
            # Loop through each answer type
            for key, answer_type in all_mcq_answer_types.items():
                # Get the related manager for the answer type
                answer_queryset = getattr(question, answer_type[0]).all()
                # If the answer type requires content evaluation, process each answer
                if answer_type[0] in answer_types_to_evaluate:
                    for answer in answer_queryset:
                        answer.content = question_student.evaluate_var_expressions_in_text(answer.content, add_html_style=True)
                
                # Extend the answers list with the processed or unprocessed answers
                answers.extend(answer_queryset)
            if not question_student.success: # Do not need to randomize the order if student has already passed.
                random.shuffle(answers)  
        elif question.answer_type.startswith('STRUCT'):
            questtype = 'struct'
            # TODO: Subclass all structural answers to a more general class 
            # so that you may use only one if.
            # Define a mapping from answer_type to the corresponding attribute and question type value
            answer_type_mapping = {
                QuestionChoices.STRUCTURAL_LATEX: 'latex_answer',
                QuestionChoices.STRUCTURAL_EXPRESSION: 'expression_answer',
                QuestionChoices.STRUCTURAL_VARIABLE_FLOAT: 'variable_float_answer',
                QuestionChoices.STRUCTURAL_FLOAT: 'float_answer',
                QuestionChoices.STRUCTURAL_TEXT: 'text_answer',
            }

            # Get the attribute name based on the answer_type
            attribute_name = answer_type_mapping.get(question.answer_type, None)

            # If the attribute name is valid, get the attribute value and extend the lists
            if attribute_name:
                answers.extend([getattr(question, attribute_name)])
            else:
                raise ValueError('Unexpected answer type. Expected a type of Structural')
            answers[0].preface = '' if answers[0].preface is None else answers[0].preface
        elif question.answer_type.startswith('MATCHING'):
            questtype = 'mp'
            answers = question.matching_pairs.all()
            attempts = question_student.attempts.all()
            pk_of_success = []
            for at in attempts:
                pk_of_success.extend(at.success_pairs.pairs.split('&'))
            # separating the parts a and b, then shuffling b
            answers_a, answers_b, answers_c = [], [], []
            for a in answers:
                if str(a.pk) not in pk_of_success:
                    answers_a.append({'content': a.part_a, 'key': a.pk})
                    answers_b.append({'content': a.part_b, 'key': encrypt_integer(a.pk)})
                else:
                    answers_c.append({'contenta':a.part_a, 'contentb':a.part_b})
            random.shuffle(answers_a) 
            random.shuffle(answers_b)
            answers = list(zip(answers_a, answers_b))
        else:
            return HttpResponse('Something went wrong')
        last_attempt = question_student.attempts.last()
        context = {
            'question':question,
            'questtype':questtype,
            'answers': answers,
            'answer': answers[0] if answers else None,
            'question_student':question_student,
            'too_many_attempts':question_student.get_too_many_attempts(),
            'last_attempt_content':last_attempt.submitted_answer if last_attempt else '',
            'last_attempt':last_attempt,
            'units_too_many_attempts':question_student.get_units_too_many_atempts(),
            'passed_pairs':answers_c,
            'potential':round(question_student.get_potential() * 100, 1),
            'num_points':round(question_student.get_num_points(), 2)
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
        
        units_correct = False
        previously_submitted = False
        data = json.loads(request.body)
        simplified_answer = data["answer"]
        submitted_answer = data["submitted_answer"]
        question = Question.objects.get(pk=question_id)
        feedback_data = ''
        return_sp = None

        question_student, created = QuestionStudent.objects.get_or_create(student=student, question=question)
        current_potential = question_student.get_potential()
        num_attempts = question_student.get_num_attempts()

        if data["questionType"].startswith('structural'):
            too_many_attempts =  num_attempts == question.struct_settings.max_num_attempts

            units_too_many_attempts = question_student.num_units_attempts == question.struct_settings.units_num_attempts

        elif data["questionType"].startswith('mcq')  or data["questionType"] == 'mp':
            too_many_attempts = num_attempts >= question.mcq_settings.mcq_max_num_attempts
            units_too_many_attempts = True # Yes, the True here is intentional. If a question type 
                                           # does not permit units any attempt, we technically interpret it
                                           # as there have already been too many units attempt for that question.
        correct = question_student.success
        if not question_student.success: 
            last_attempt = QuestionAttempt.objects.filter(question_student=question_student).last()
            prev_success = last_attempt.success if last_attempt else False
            correct = prev_success # checking if succeeded sheer answer (and failed units)
            prev_units_success = last_attempt.units_success if last_attempt else False # checking if succeeded units (and failed sheer answer)
            units_correct = prev_units_success
            units_too_many_attempts = False if prev_units_success else units_too_many_attempts

            if not (too_many_attempts or prev_success):
                if data["questionType"].startswith('structural'):
                    if question.answer_type == QuestionChoices.STRUCTURAL_EXPRESSION:
                        # checking previous attempts
                        for previous_attempt in question_student.attempts.all():
                            if compare_expressions(previous_attempt.content, simplified_answer):
                                previously_submitted = True
                                return JsonResponse({'previously_submitted': previously_submitted})
                        # Recording attempt
                        attempt = QuestionAttempt.objects.create(question_student=question_student,\
                                                                 content=simplified_answer,\
                                                                    submitted_answer=submitted_answer)
                        # Getting correct answer
                        answer_content, units = question.expression_answer.content, question.expression_answer.answer_unit
                        # Comparing correct answer with simplified submitted answer
                        correct = compare_expressions(answer_content, simplified_answer)
                    elif question.answer_type in [QuestionChoices.STRUCTURAL_FLOAT, QuestionChoices.STRUCTURAL_VARIABLE_FLOAT]:
                        if question.answer_type == QuestionChoices.STRUCTURAL_FLOAT:
                            # Structural float with no variable.
                            answer_content, units = question.float_answer.content, question.float_answer.answer_unit
                        else:
                            # Variable structural float
                            answer_content, units = question_student.compute_structural_answer(), question.variable_float_answer.answer_unit
                        try:
                            # Will sometimes return a value error if answers do not match
                            correct, feedback_data = compare_floats(answer_content, simplified_answer, question.struct_settings.margin_error)
                        except ValueError:
                            correct = False

                        # Checking previous submissions before recording attempt
                        if not correct:
                            for prev_attempt in question_student.attempts.all():
                                answers_are_the_same, _ = compare_floats(prev_attempt.content, simplified_answer, margin_error=0.02, get_feedback=False)
                                if answers_are_the_same:
                                    return JsonResponse({'previously_submitted': True})
                        
                        attempt = QuestionAttempt.objects.create(question_student=question_student,\
                                                                 content=simplified_answer,
                                                                 submitted_answer=submitted_answer)
                    else:
                        raise ValueError(f'Expected either STRUCT FLOAT OR VAR STRUCT FLOAT, but got {question.answer_type}')
                    
                    # Recording status (whether attempt was succesful or not)
                    # then calculating the number of points
                    if correct: # Handling correct case for structural questions.
                        attempt.success = True
                        attempt_potential = current_potential
                        if units: # if the answer has units.                      
                            if prev_units_success:
                                # Carrying over the units submission from previous attempt.
                                attempt.units_success = True
                                attempt.submitted_units = last_attempt.submitted_units
                                attempt_potential -= question.struct_settings.percentage_pts_units
                                question_student.success, question_student.is_complete = (True, True)  
                            # We do not need to check whether there have been too many units
                            # attempt because the function returning current_potential already considers that. 
                            else:                       
                                submitted_units = data["submitted_units"]
                                units_correct = compare_units(units, submitted_units)
                                attempt.units_success = units_correct
                                attempt.submitted_units = submitted_units
                                question_student.num_units_attempts += 1
                                # Updating question status
                                if units_correct:
                                    question_student.success, question_student.is_complete = (True, True)    
                                else: # if the person gets the question wrong
                                    attempt_potential -= question.struct_settings.percentage_pts_units     
                        else:
                            question_student.success, question_student.is_complete = (True, True)
                        attempt_potential = max(0, attempt_potential)
                        attempt.num_points = round(attempt_potential * question.struct_settings.num_points, 2)
                        question_student.save()
                    else:
                        if prev_units_success:
                            # Checking whether units have been previously succeeded and
                            # carrying the submission over
                            attempt.units_success = True
                            attempt.submitted_units = last_attempt.submitted_units
                        elif not units_too_many_attempts:
                            # Checking whether submitted units are correct. 
                            submitted_units = data["submitted_units"]
                            units_correct = compare_units(units, submitted_units)
                            attempt.units_success = units_correct
                            attempt.submitted_units = submitted_units
                            question_student.num_units_attempts += 1
                            # Update the number of points for this attempt
                            if units_correct:
                                attempt.num_points = max(0, round(question.struct_settings.percentage_pts_units * \
                                                           question.struct_settings.num_points, 2))
                        

                elif data["questionType"] == 'mcq':
                    # retrieve list of 'true' mcq options
                    # !important: mcq answers of different type may have the same primary key.
                    # That is the reason why the type is taken into consideration when doing comparisons.
                    # checking previous attempts
                    for previous_attempt in question_student.attempts.all():
                        # previous_attempt.content is a string, so we use eval() to convert 
                        # to list, before converting to set and doing the comparison.
                        if set(simplified_answer) == set(eval(previous_attempt.content)):
                            previously_submitted = True
                            return JsonResponse({'previously_submitted': previously_submitted})
                    attempt = QuestionAttempt.objects.create(question_student=question_student, \
                                                             content=str(simplified_answer))
                    answers = []

                    # Loop through each answer type and process accordingly
                    for answer_type_code, answer_field in all_mcq_answer_types.items():
                        # Use getattr to dynamically get the related manager for the answer type
                        answer_queryset = getattr(question, answer_field[0])
                        # Filter for is_answer=True and get a list of primary keys
                        answer_pks = list(answer_queryset.filter(is_answer=True).values_list('pk', flat=True))
                        # Convert primary keys to the desired string format and extend the answers list
                        answers.extend([str(pk) + str(answer_field[1]) for pk in answer_pks])

                    # Validating mcq submission
                    if len(simplified_answer) == len(answers):
                        s1, s2 = set(simplified_answer), set(answers)
                        if s1 == s2:
                            correct = True
                            attempt.num_points = max(0, round(current_potential * question.mcq_settings.num_points, 2))
                            question_student.success, question_student.is_complete = (True, True)
                            attempt.success = True

                elif data["questionType"] == 'mp':
                    success_pairs_strings = []
                    attempt_pairs = []
                    # Expecting to receive a dictionary(JS object) from the front end
                    # with keys being the primary keys, and values being the encrypted primary keys
                    # So we decrypt the values and see if they are the same with the key.
                    for part_A_pk, encrypted_B_pk in submitted_answer.items():
                        decrypted_b = decrypt_integer(int(encrypted_B_pk))
                        attempt_pairs.append(f'{part_A_pk}-{decrypted_b}')
                        if int(part_A_pk) == decrypted_b:
                            success_pairs_strings.append(part_A_pk)

                    # Calculating the number of points gain and saving submission
                    num_of_correct = len(success_pairs_strings)
                    total_num_of_pairs = question.matching_pairs.count()
                    # Checking whether current attempt has some primary keys of already
                    # successful attempt. That scenario should not happen unless someone is trying an inject
                    # but we need to take care of it.
                    for previous_a in QuestionAttempt.objects.filter(question_student=question_student):
                        sp = previous_a.success_pairs.pairs.split('&')
                        success_pairs_strings = list(set(success_pairs_strings) - set(sp))
                    frac = (num_of_correct/total_num_of_pairs)
                    if frac == 1 or num_of_correct == len(attempt_pairs): # we technically do not need frac in this condition.
                        question_student.success, question_student.is_complete = (True, True)                        
                        correct = True
                    attempt_pairs = "&".join(attempt_pairs)
                    attempt = QuestionAttempt.objects.create(question_student=question_student)
                    attempt.content = attempt_pairs
                    attempt.submitted_answer = attempt_pairs # useless. Using twice the size of memory.
                    attempt.num_points = max(0, round(frac * current_potential * question.mcq_settings.num_points, 2))                      
                    return_sp = success_pairs_strings # will return the successful pairs so the front end can be updated.
                    success_pairs_strings = "&".join(success_pairs_strings)   
                    # attempt.save() # probably not needed here?
                    success_pairs = QASuccessPairs.objects.create(question_attempt=attempt,pairs=success_pairs_strings)
                    success_pairs.save()
                question_student.save()
                attempt.save()

            else:                                                                       
                if prev_units_success: # and no attempt has been created
                    assert prev_success == False # because question_student.success must be True in this case.

                elif not units_too_many_attempts:# here is why units_too_many_attempts must be true for non-struct questions.
                    submitted_units = data["submitted_units"]
                    answer_types_with_units = {QuestionChoices.STRUCTURAL_FLOAT: 'float_answer',\
                                            QuestionChoices.STRUCTURAL_EXPRESSION:'expression_answer',\
                                                QuestionChoices.STRUCTURAL_VARIABLE_FLOAT:'variable_float_answer'}
                    if question.answer_type in answer_types_with_units:
                        units = getattr(question, answer_types_with_units[question.answer_type]).answer_unit
                        units_correct = compare_units(units, submitted_units)
                        last_attempt.units_success = units_correct
                        last_attempt.submitted_units = submitted_units
                        question_student.num_units_attempts += 1
                        last_attempt.num_points += max(0, round(question.struct_settings.percentage_pts_units * \
                                                         question.struct_settings.num_points * int(units_correct), 2))
                        last_attempt.save()
                        # Updating question status
                        if units_correct and prev_success:
                            question_student.success, question_student.is_complete = (True, True)
                        question_student.save()    

        # Some info that will be used to update the front end.
        if (not correct and (data["questionType"].startswith('structural'))):
            too_many_attempts =  num_attempts + 1 == question.struct_settings.max_num_attempts
            if not units_correct:
                units_too_many_attempts = question_student.num_units_attempts >= question.struct_settings.units_num_attempts

        # Updating completion status
        if not question_student.is_complete and (units_too_many_attempts or units_correct) and (too_many_attempts or prev_success):
            question_student.is_complete = True
            question_student.save()
        # Return a JsonResponse
        return JsonResponse({
            'correct': correct,
            'too_many_attempts': too_many_attempts,
            'previously_submitted':previously_submitted,
            'feedback_data': feedback_data,
            'units_correct': units_correct,
            'units_too_many_attempts':units_too_many_attempts,
            'success_pairs': return_sp if return_sp else None,
            'potential':round(question_student.get_potential() * 100),
            'grade':round(question_student.get_num_points(), 2),
            'numAttempts':question_student.get_num_attempts(),
            'unitsNumAttempts': question_student.num_units_attempts,
            'complete':question_student.is_complete
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
            stud = Student.objects.get(username=username)
            username = str(username) + str(random.randint(1, 1000000))
        except:
            pass
        try:
            s = Student.objects.get(username=username)
            username = str(username) + str(random.randint(1, 10000000))
        except Student.DoesNotExist:
            pass
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
            title = request.POST.get('title', '')
            note.title = title
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
                             'last_edited':note.last_edited, 'title':title})
    else:
        return JsonResponse({'message': f'Error: Expected POST method, not {request.method}', 'success':False})
@csrf_exempt    
def generate_note_qr(request, question_id, course_id, assignment_id, student_id=None, upload_note_img=None):
    data = json.loads(request.body)
    question = get_object_or_404(Question,pk=question_id)
    student = get_object_or_404(Student,pk=request.user.id)
    question_student = QuestionStudent.objects.get(question=question, student=student)
    data_temp_note = data['temp_note']
    data_temp_title = data['temp_title']
    base_link = data['base_link']
    if data['same_url']:
        custom_link = base_link
    else:
        custom_link = f"{base_link}/{request.user.pk}/1"
    note = Note.objects.get(question_student=question_student)
    temp_note, created = NoteTemporary.objects.get_or_create(note=note)
    temp_note.content = data_temp_note
    temp_note.title = data_temp_title
    temp_note.save()
    img = qrcode.make(custom_link)  # replace with your custom link
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response

@login_required(login_url='astros:login')
def assignment_gradebook_student(request,student_id, assignment_id):

    assignment_student, created = AssignmentStudent.objects.get_or_create(pk=assignment_id)
    course= assignment_student.assignment.course.id

    questions= Question.objects.filter(assignment= assignment_student.assignment ) 
    student= Student.objects.get(pk=student_id)
    assignments= AssignmentStudent.objects.filter(student=student, assignment__course=course)

    assignment_details={'name':assignment_student.assignment.name,'assignment_id':assignment_id,\
                        'Due_date':str(assignment_student.due_date).split(' ')[0],'grade':assignment_student.get_grade() }
    
    question_heading = ['Question_number','score','num_attempts']
    question_details = []
    for question in questions:
        if question.answer_type.startswith(('MCQ', 'MATCHING')):
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
    assignments_dict = {}
    # this is needed to display notes
    Notes = Note.objects.filter(question_student__student=student)
    for note in Notes:
        assignment = note.question_student.question.assignment
        if note.content:
            a_list = assignments_dict.get(assignment, None)
            n_dict = {'Note':note, "note_md":markdown(note.content)}
            if a_list:
                a_list.append(n_dict)
            else:
                assignments_dict[assignment] = [n_dict]
    context = {
        "student":student,
        "course": course,
        "assignments_dict":assignments_dict
    }
    return render(request, "deimos/note_management.html", context)


def generate_practice_test(request):
    course_id = request.POST['course_id']
    topic_name = request.POST['topic_name']
    num_Questions = request.POST['num_Question']
    practice_test_name = request.POST['practice_test_name']
    student = get_object_or_404(Student, pk = request.user.pk)
    course = Course.objects.get(pk=course_id)
    practice_course,is_created= Course.objects.get_or_create(name='Practice Course')

    # try:
    #     is_enrolled= Enrollment.objects.get(course=course, student=student)
    # except Enrollment.DoesNotExist:
    #     return HttpResponse('Illegal Access')
    
    topic = Topic.objects.get(name=topic_name)
    question_student_topic=[]
    question_student_topic_attempts=[]

    # Check if there are any questions under this topic
    if not Question.objects.filter(topic=topic).exists():
        error = "There are currently no questions under this topic. Please select another."
        return HttpResponseRedirect(reverse("deimos:practice_test_settings", args=(course.id,), kwargs={'error_message': error}))

    # Get all QuestionStudent objects for the student and topic with the number of attempts
    question_student_topic = QuestionStudent.objects.filter(
        student=student,
        question__topic=topic
    ).annotate(num_attempts=Count('attempts'))

    # Extract the number of attempts for statistics
    question_student_topic_attempts = [qs.num_attempts for qs in question_student_topic]

    # computing the number of question to be selected
    if int(num_Questions)>len(question_student_topic):
        k=len(question_student_topic)
    else:
        k=int(num_Questions)
    # selecting the questions based on the probability distribution
    distribution=answered_question_statistics(question_student_topic_attempts)
    Selected_questions= random.choices(question_student_topic,weights=distribution, k=k)

    # creating a new practice test assignment
    practice_test= Assignment.objects.create(course=practice_course, name=practice_test_name, is_assigned=True)
    practice_test.save()

    # adding selected and similar questions to the new practice test assignment and saving assignmentstudent
    practice_questions=[]
    for question in Selected_questions:
        similar = similar_question(question.question)
        if not similar:  # If the list is empty, continue to the next iteration
            continue
        select = random.choice(similar)
        # Let's ensure a question doesnot repeat twice
        while select in practice_questions and similar != []:
            similar.remove(select) 
            if similar != []:
                select = random.choice(similar)
        # copying te selected question into te practce test course   
        if similar !=[]:
            result = export_question_to(request,select['question'].id,practice_test.id)
            practice_questions.append(select)

    practice_test_student = AssignmentStudent.objects.create(assignment= practice_test, student= student)
    practice_test_student.save()
    practice_test_enroll = Enrollment.objects.create(student=student, course=practice_course)
    practice_test_enroll.save()

    return HttpResponseRedirect(reverse("deimos:course_management",None,None,{'course_id':practice_course.id}))

def practice_test_settings(request,course_id=None,error_message=None):
    topics= Topic.objects.all()
    course= Course.objects.get(pk=course_id)
    return render(request,"deimos/practice_test_setting.html",{'topics':topics, 'course':course, 'error_message':error_message})

def normal_prob(x, mu, sigma):
    p = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
  # return the normal probability
    return p

def answered_question_statistics(input_list):
    # Check if the input list is empty
    if not input_list:
        # Return a default distribution or handle the empty case appropriately
        return [1]  # or any other default you deem appropriate

    array = np.array(input_list)
    mean = np.mean(array)
    std = np.std(array)
    
    # Handle the case where standard deviation is zero (all values are the same)
    if std == 0:
        std = 1

    # Calculate the probabilities
    probabilities = [normal_prob(x, mean, std) for x in array]

    # Handle the case where all probabilities are zero
    if all(prob == 0 for prob in probabilities):
        return [1] * len(probabilities)

    mode = np.max(probabilities)
    # Calculate the distribution as the maximum probability divided by each probability
    distribution = [mode / i if i != 0 else 1 for i in probabilities]
    return distribution

def similar_question(input_question):
        all_questions = Question.objects.all()
        encoded_output_pooled= torch.tensor(input_question.embedding)
        # Calculate cosine similarity with stored question encodings
        similar_questions = []
        for question in all_questions:
            question_encoded_output_pooled = torch.tensor(question.embedding)  # Load pre-computed encoding
            similarity_score = cosine_similarity(encoded_output_pooled, question_encoded_output_pooled).item()
            similar_questions.append({'question': question, 'similarity': similarity_score})
        # Sort by similarity score and get top 10
        top_n = 3
        return heapq.nlargest(top_n, similar_questions, key=lambda x: x['similarity'])