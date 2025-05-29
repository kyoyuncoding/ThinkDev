from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("problemlog/", views.problem_log, name="problem_log")
]