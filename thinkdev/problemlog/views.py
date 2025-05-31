from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, "index.html")

def problem_log(request):
    return render(request, "problemlog.html")

def log(request):
    return render(request, "log.html")

def register(request):
    return render(request, "register.html")

def login(request):
    return render(request, "login.html")
