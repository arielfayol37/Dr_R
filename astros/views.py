from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'astros/index.html')

def login_view(request):
    return render(request, 'astros/login.html')

def register(request):
    return render(request, 'astros/register.html')
