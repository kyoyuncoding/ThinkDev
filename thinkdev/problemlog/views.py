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
        return HttpResponseRedirect(reverse("problem_log"))

@login_required
def problem_log(request):
    if request.method == "POST":
        if request.POST.get("save_problem_button") and request.POST.get("title_of_problem"):
            problem_entry = Problems(username=request.user.username, problem_title = request.POST.get("title_of_problem"), problem_description = request.POST.get("problem_description"), problem_summary = request.POST.get("problem_summary"), pseudo_code = request.POST.get("pseudocode"), source_code = request.POST.get("sourcecode"), solved=request.POST.get("solved_dropdown"), submit_time = datetime.now())
            problem_entry.save()
            save_version = ProblemVersions(problem_id = Problems.objects.get(id=problem_entry.id), username=request.user.username, problem_title = request.POST.get("title_of_problem"), problem_description = request.POST.get("problem_description"), problem_summary = request.POST.get("problem_summary"), pseudo_code = request.POST.get("pseudocode"), source_code = request.POST.get("sourcecode"), solved=request.POST.get("solved_dropdown"), submit_time = datetime.now())
            save_version.save()
        elif not request.POST.get("title_of_problem"):
            return HttpResponse("Ya Need To Enter a Title My Guy")
        return HttpResponseRedirect(reverse("log"))
    return render(request, "problemlog.html")

@login_required
def log(request):
    problems = Problems.objects.filter(username=request.user.username)
    return render(request, "log.html", {
        "problems": problems 
    })

@login_required
def problem_log_edit(request, id_entry):
    if request.POST.get("delete_button"):
        entry = Problems.objects.get(id=id_entry, username=request.user.username)
        entry.delete()
        return HttpResponseRedirect(reverse("log"))
    elif request.POST.get("save_problem_button"):

        # ChatGPT taught me how to update pre-existing database entries with Django.
        update_entry = Problems.objects.get(id=id_entry, username=request.user.username)
        update_entry.username = request.user.username
        update_entry.problem_title = request.POST.get("title_of_problem")
        update_entry.problem_description = request.POST.get("problem_description")
        update_entry.problem_summary = request.POST.get("problem_summary")
        update_entry.pseudo_code = request.POST.get("pseudocode")
        update_entry.source_code = request.POST.get("sourcecode")
        update_entry.solved = request.POST.get("solved_dropdown")
        update_entry.submit_time = datetime.now()
        update_entry.save()
        problems = Problems.objects.filter(id=id_entry, username=request.user.username)
        
        # Do a query to see if a past row exists with the foriegn key. If not, then automatically give the version_number as 1(or I can just make the default value 1 tbf). If a row exists already, take the largest version number and add 1 to it.
        save_version = ProblemVersions(problem_id = Problems.objects.get(id=id_entry), username=request.user.username, version_number = , problem_title = request.POST.get("title_of_problem"), problem_description = request.POST.get("problem_description"), problem_summary = request.POST.get("problem_summary"), pseudo_code = request.POST.get("pseudocode"), source_code = request.POST.get("sourcecode"), solved=request.POST.get("solved_dropdown"), submit_time = datetime.now())
        save_version.save()
        return HttpResponseRedirect(reverse("log"))
    entry = Problems.objects.get(id=id_entry, username=request.user.username)
    return render(request, "problemlog.html",{
        "entry": entry
    })

@login_required
def problem_versions(request, id_entry):
    versions =  ProblemVersions.objects.filter(problem_id = id_entry, username = request.user.username)
    return render(request, "versions.html", {
        "versions": versions
    })

@login_required
def versions_view(request, id_entry):
    if request.POST.get("view_button"):
        currentTitle = Problems.objects.get(id=ProblemVersions.objects.filter(id=id_entry).values('problem_id_id').first()["problem_id_id"])
        version = ProblemVersions.objects.get(id=id_entry)
        return render(request, "versionview.html", {
            "entry": version,
            "currentTitle": currentTitle,
            # "versionNumber": versionNumber
        })















        # TO-DO LIST
        # Edit the ProblemVersions model to include the version number of the problem, so that it can be used in the versionview.html file, and the versions_view view.
        # You shouldn't be able to save a problem if it is unchanged from the most previous version.
        # The most recent version of the problem should be the most recent problem in the problemversions table, rather than the unique copy of the problem in the problems table.
        # When you click "view" on one of the problem versions, the problem title should be clickable, so that it takes you back to the versions of the problem you clicked on.

        #DONE
        # Get rid of the delete functionality on the versions. You can't delete a previous version. You can only view the previous version.
        # When you first create a problem, it should also be the first version that is created.
        # When you register an account, it should say that you have successfully registered an account! and take you to the login page, or have a link to take you to the login page.
        # Fixed the issue where problems from different users were coming up when saving an edit to a pre - existing problem.
        # Added the ability to view and delete different versions, where the text-areas are greyed out, and there is some metadata about the version of the problem as well.
        # Version history should have the title of the most recent version of the problem somewhere.

        # IN PROGRESS
        # The current version should be highlighted, so you know that it is the first version.