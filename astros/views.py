from django.shortcuts import render, redirect
from phobos.models import Course, Professor
from deimos.models import Student, Enrollment
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
# Create your views here.
import stripe
from django.http import JsonResponse


def index(request):
    return render(request, 'astros/index.html')


def login_view(request):
    return render(request, 'astros/login.html')


def register(request):
    return render(request, 'astros/register.html')


def checkout(request):
    stripe.api_key = 'sk_test_51NgacsKivEXkYAiMsbOrP336KU8pVrqhvfVBKLF4xcDlu2DWxR7lc4HSMVIBxfCNeu7finHJbIieOikyTu3AH5Eo00DoRuw0wg'
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Dr.R Subscription',
                        },
                        'unit_amount': 3773,  # 37.73 USD
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url="http://127.0.0.1:8000/register",
            cancel_url="http://127.0.0.1:8000",
        )
    except Exception as e:
        return str(e)
    print(checkout_session.url)
    return JsonResponse({'url': checkout_session.url})


def all_courses(request):
    courses = Course.objects.all().order_by('-timestamp')
    # TODO: you may *need* to user request.user._wrapped instead
    try:
        professor = Professor.objects.get(pk=request.user.pk)
        is_professor_list = [1 if course.professors.filter(pk=request.user.pk).exists()
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
        student = Student.objects.get(pk=request.user.pk)
        is_student_list = [1 if Enrollment.objects.filter(student=request.user, course=course).exists()
                           else 0 for course in courses]
        context = {
            "courses__is_student": zip(courses, is_student_list),
            "is_professor": False,
            "is_student": True
        }
        return render(request, "astros/all_courses.html", context)

    except Student.DoesNotExist:
        pass
    return render(request, 'astros/all_courses.html', {"courses": courses})
