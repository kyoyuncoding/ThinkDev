from django.shortcuts import render
from django.http import HttpResponse
from .models import Problems
from datetime import datetime

# Create your views here.

def index(request):
    return render(request, "index.html")

def problem_log(request):

    if request.method == "POST":
        if request.POST.get("edit_button"):
            return render(request, "problemlog.html")

    return render(request, "problemlog.html")

def log(request):

    if request.method == "POST":
        if request.POST.get("save_problem_button") and request.POST.get("title_of_problem"):
            problem_entry = Problems(problem_title = request.POST.get("title_of_problem"), problem_description = request.POST.get("problem_description"), problem_summary = request.POST.get("problem_summary"), pseudo_code = request.POST.get("pseudocode"), source_code = request.POST.get("sourcecode"), submit_time = datetime.now())
            problem_entry.save()
        else:
            return HttpResponse("Ya Need To Enter a Title My Guy")

    problems = Problems.objects.all()

    return render(request, "log.html", {
        "problems": problems 
    })

def register(request):
    return render(request, "register.html")

def login(request):
    return render(request, "login.html")
