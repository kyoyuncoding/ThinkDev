from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("problemlog/", views.problem_log, name="problem_log"),
    path("problemlog/edit/<int:id_entry>", views.problem_log_edit, name="problem_log_edit"),
    path("register/", views.register_user, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("log/", views.log, name="log"),
    path("problemlog/versions/<int:id_entry>", views.problem_versions, name="problem_versions"),
    path("problemlog/versions/view/<int:id_entry>", views.versions_view, name="versions_view")
]