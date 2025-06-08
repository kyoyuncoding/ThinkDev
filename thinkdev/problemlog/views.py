from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Problems
from datetime import datetime
from django import forms
from django.urls import reverse

# Create your views here.

def index(request):
    return render(request, "index.html")

def problem_log(request):
    if request.method == "POST":
        if request.POST.get("save_problem_button") and request.POST.get("title_of_problem"):
            problem_entry = Problems(problem_title = request.POST.get("title_of_problem"), problem_description = request.POST.get("problem_description"), problem_summary = request.POST.get("problem_summary"), pseudo_code = request.POST.get("pseudocode"), source_code = request.POST.get("sourcecode"), solved=request.POST.get("solved_dropdown"), submit_time = datetime.now())
            problem_entry.save()
        elif request.POST.get("title_of_problem") == False:
            return HttpResponse("Ya Need To Enter a Title My Guy")
        return HttpResponseRedirect(reverse("log"))

    return render(request, "problemlog.html")

def log(request):
    problems = Problems.objects.all()

    return render(request, "log.html", {
    "problems": problems 
    })

def register(request):
    return render(request, "register.html")

def login(request):
    return render(request, "login.html")

def problem_log_edit(request, id_entry):

    if request.POST.get("delete_button"):
        entry = Problems.objects.get(id=id_entry)
        entry.delete()
        return HttpResponseRedirect(reverse("log"))

    if request.POST.get("save_problem_button"):

        # ChatGPT taught me how to update pre-existing database entries with Django.
        update_entry = Problems.objects.get(id=id_entry)
        update_entry.problem_title = request.POST.get("title_of_problem")
        update_entry.problem_description = request.POST.get("problem_description")
        update_entry.problem_summary = request.POST.get("problem_summary")
        update_entry.pseudo_code = request.POST.get("pseudocode")
        update_entry.source_code = request.POST.get("sourcecode")
        update_entry.solved = request.POST.get("solved_dropdown")
        update_entry.submit_time = datetime.now()
        update_entry.save()
        problems = Problems.objects.all()
        return render(request, "log.html",{
        "problems": problems
        })

    entry = Problems.objects.get(id=id_entry)
    return render(request, "problemlog.html",{
    "entry": entry
    })


