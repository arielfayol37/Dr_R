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
def index(request):
    pass

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("phobos:index"))
        else:
            return render(request, "astros/login.html", {
                "message": "Invalid username and/or password."
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
                "message": "Passwords must match."
            })

        # Attempt to create new professor
        try:
            professor = Professor.objects.create_user(username, email, password,\
                                                 first_name = first_name, department = department,\
                                                    last_name = last_name)
            professor.save()
        except IntegrityError:
            return render(request, "astros/register.html", {
                "message": "Username already taken."
            })
        login(request, professor)
        return HttpResponseRedirect(reverse("phobos:index"))
    else:
        return render(request, "astros/register.html")
