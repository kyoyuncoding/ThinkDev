from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Problems, ProblemVersions
from datetime import datetime
from django import forms
from django.urls import reverse

# Create your views here.
def register_user(request):

    # Conditional logic to determine whether or not a register attempt was valid. For example, if the request method is "POST", and there isn't a
    # value in the "register_username" element, then the function returns an error message, which is "Enter a username."
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

        elif User.objects.filter(username=request.POST.get("register_username")):
            return render(request, "register.html", {
                "message": "Username already taken."
            })

        elif User.objects.filter(email=request.POST.get("register_email")):
            return render(request, "register.html", {
                "message": "Email address already used."
            })

    # If all the checks are passed, then there are a series of variables which are initalized, to store the login details, and a new user
    # variable is initialized, which uses the User model to create a user.
        else:
            username = request.POST.get("register_username")
            email = request.POST.get("register_email")
            password = request.POST.get("register_password")
            new_user = User.objects.create_user(username, email, password)
            return render(request, "register.html",{
                "confirmation_message": "You successfully registered!"
            })

    return render(request, "register.html")

def login_user(request):

    # This function allows users to login. It takes the request method from the HTML element and uses the authenticate function to login 
    # the user.
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

    # This function allows users to logout, via the "logout()" function.
    logout(request)
    return render(request, "index.html", {
        "message": "Successfully Logged Out!"
    })

def index(request):

    # This function takes you back to the homepage if the user is not authenticated.
    if not request.user.is_authenticated:
        return render(request, "index.html")  

    else:
        return HttpResponseRedirect(reverse("problem_log"))

@login_required
def problem_log(request):

    # When the 'save problem' button is clicked on the Problem Log page, and the title of the problem is not empty, then 
    # a new entry is created in the Problems model, which populates all the columns with the text areas.
    if request.method == "POST":

        if request.POST.get("save_problem_button") and request.POST.get("title_of_problem"):
            problem_entry = Problems(username=request.user.username, problem_title = request.POST.get("title_of_problem"), problem_description = request.POST.get("problem_description"), problem_summary = request.POST.get("problem_summary"), pseudo_code = request.POST.get("pseudocode"), source_code = request.POST.get("sourcecode"), solved=request.POST.get("solved_dropdown"), submit_time = datetime.now())
            problem_entry.save()
            save_version = ProblemVersions(problem_id = problem_entry.id, username=request.user.username, problem_title = request.POST.get("title_of_problem"), problem_description = request.POST.get("problem_description"), problem_summary = request.POST.get("problem_summary"), pseudo_code = request.POST.get("pseudocode"), source_code = request.POST.get("sourcecode"), solved=request.POST.get("solved_dropdown"), submit_time = datetime.now())
            save_version.save()

        elif not request.POST.get("title_of_problem"):
            return HttpResponse("Enter a title.")

        return HttpResponseRedirect(reverse("log"))

    return render(request, "problem-log.html")

@login_required
def log(request):

    # This function filters the Problems model, returning a QuerySet of all the problems which match the username of the requestee. 
    # These problems then get passed to the log.html file, and rendered.
    problems = Problems.objects.filter(username=request.user.username)
    return render(request, "log.html", {
        "problems": problems 
    })

@login_required
def problem_log_edit(request, id_entry):

    # If the "delete button" is pressed, a new variable is first initialized with the id of the problem, and then the variable is deleted.
    if request.POST.get("delete_button"):
        entry = Problems.objects.get(id=id_entry, username=request.user.username)
        entry.delete()
        return HttpResponseRedirect(reverse("log"))

    # If the save problem button is pressed, a new variable is initalized with the results of the QuerySet, and it first checks whether or not
    # any edits have been made (if there haven't been any edits, then it returns an error message.) Otherwise, it just updates the problem 
    # in the previously saved problems log, and saves a new version to the ProblemVersions model.
    elif request.POST.get("save_problem_button"):
        update_entry = Problems.objects.get(id=id_entry, username=request.user.username)

        if (update_entry.username == request.user.username and update_entry.problem_title == request.POST.get("title_of_problem") and update_entry.problem_description == request.POST.get("problem_description") and update_entry.problem_summary == request.POST.get("problem_summary") and update_entry.pseudo_code == request.POST.get("pseudocode") and update_entry.source_code == request.POST.get("sourcecode") and update_entry.solved == request.POST.get("solved_dropdown")):
            error = "No edits detected."
            entry = Problems.objects.get(id=id_entry, username=request.user.username)
            return render(request, "problem-log.html",{
                "entry": entry,
                "error": error
            })

        else:
            update_entry.username = request.user.username
            update_entry.problem_title = request.POST.get("title_of_problem")
            update_entry.problem_description = request.POST.get("problem_description")
            update_entry.problem_summary = request.POST.get("problem_summary")
            update_entry.pseudo_code = request.POST.get("pseudocode")
            update_entry.source_code = request.POST.get("sourcecode")
            update_entry.solved = request.POST.get("solved_dropdown")
            update_entry.submit_time = datetime.now()
            update_entry.save()
        
        latestProblemVersion = ProblemVersions.objects.filter(problem_id=id_entry).order_by('-submit_time').values('version_number').first()

        if (latestProblemVersion == None):
            probVersion == 1

        else:
            probVersion = latestProblemVersion["version_number"] + 1

        save_version = ProblemVersions(problem_id = id_entry, username=request.user.username, version_number = probVersion, problem_title = request.POST.get("title_of_problem"), problem_description = request.POST.get("problem_description"), problem_summary = request.POST.get("problem_summary"), pseudo_code = request.POST.get("pseudocode"), source_code = request.POST.get("sourcecode"), solved=request.POST.get("solved_dropdown"), submit_time = datetime.now())
        save_version.save()
        return HttpResponseRedirect(reverse("log"))

    entry = Problems.objects.get(id=id_entry, username=request.user.username)
    return render(request, "problem-log.html",{
        "entry": entry
    })

@login_required
def problem_versions(request, id_entry):

    # This function basically returns all of the versions of the problem. The query is based on the problem id, and the username.
    versions =  ProblemVersions.objects.filter(problem_id = id_entry, username = request.user.username)
    return render(request, "versions.html", {
        "versions": versions
    })

@login_required
def versions_view(request, id_entry):

    # If the view button is pressed, then the currentTitle() variable is initialized, which finds the version of the problem and renders it.
    if request.POST.get("view_button"):
        currentTitle = Problems.objects.get(id=ProblemVersions.objects.filter(id=id_entry).values('problem_id').first()["problem_id"])
        version = ProblemVersions.objects.get(id=id_entry)
        return render(request, "version-view.html", {
            "entry": version,
            "currentTitle": currentTitle
        })