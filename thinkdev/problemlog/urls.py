from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("problemlog/", views.problem_log, name="problem_log"),
    path("problemlog/edit/<int:id_entry>", views.problem_log_edit, name="problem_log_edit"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("log/", views.log, name="log")
]