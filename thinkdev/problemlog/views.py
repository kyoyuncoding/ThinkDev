from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Problems
from datetime import datetime
from django import forms
from django.urls import reverse

# Create your views here.
def register_user(request):

    if request.method == "POST":
        if not request.POST.get("register_username"):
            return render(request, "register.html", {
                "message": "Enter a username."
            })
        elif not request.POST.get("register_email"):
            return render(request, "register.html", {
                "message": "Enter an email address."
            })
        elif not request.POST.get("register_password") or not request.POST.get("confirm_password"):
            return render(request, "register.html", {
                "message": "Enter password and confirmation."
            })
        elif request.POST.get("register_password") != request.POST.get("confirm_password"):
            return render(request, "register.html", {
                "message": "Passwords don't match."
            })
        # fix this, don't let someone with the same username create an account, or someone with the same email address. Change all the objects.get() to objects.filter()
        elif User.objects.filter(username=request.POST.get("register_username")).values:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        elif User.objects.filter(email=request.POST.get("register_email")).values:
            return render(request, "register.html", {
                "message": "Email address already has an account associated with it."
            })
        else:
            username = request.POST.get("register_username")
            email = request.POST.get("register_email")
            password = request.POST.get("register_password")
            new_user = User.objects.create_user(username, email, password)

    return render(request, "register.html")

def login_user(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("problem_log"))
        else:
            return render(request, "login.html", {
                "message": "Invalid Log-In Details. Try Again."
            })

    return render(request, "login.html")

def logout_user(request):

    logout(request)
    return render(request, "index.html", {
        "message": "Successfully Logged Out!"
    })

def index(request):

    if not request.user.is_authenticated:
        return render(request, "index.html")    
    else:
        HttpResponseRedirect(reverse("problem_log"))

@login_required
def problem_log(request):

    if request.method == "POST":
        if request.POST.get("save_problem_button") and request.POST.get("title_of_problem"):
            problem_entry = Problems(username=request.user.username, problem_title = request.POST.get("title_of_problem"), problem_description = request.POST.get("problem_description"), problem_summary = request.POST.get("problem_summary"), pseudo_code = request.POST.get("pseudocode"), source_code = request.POST.get("sourcecode"), solved=request.POST.get("solved_dropdown"), submit_time = datetime.now())
            problem_entry.save()
        elif not request.POST.get("title_of_problem"):
            return HttpResponse("Ya Need To Enter a Title My Guy")
        return HttpResponseRedirect(reverse("log"))

    return render(request, "problemlog.html")

@login_required
def log(request):

    problems = Problems.objects.filter(username=request.user.username).values()
    return render(request, "log.html", {
        "problems": problems 
    })

@login_required
def problem_log_edit(request, id_entry):

    if request.POST.get("delete_button"):
        entry = Problems.objects.get(id=id_entry, username=request.user.username)
        entry.delete()
        return HttpResponseRedirect(reverse("log"))

    if request.POST.get("save_problem_button"):
        # ChatGPT taught me how to update pre-existing database entries with Django.
        update_entry = Problems.objects.get(id=id_entry)
        update_entry.username = request.user.username
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

    entry = Problems.objects.get(id=id_entry, username=request.user.username)
    return render(request, "problemlog.html",{
        "entry": entry
    })
