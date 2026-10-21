
from django.urls import path
from django.shortcuts import render
from . import views


def login_original(request):
    return render(request, "login.html")


def dashboard_original(request):
    return render(request, "dashboard.html")


def painel_aluno_original(request):
    return render(request, "painel_aluno.html")


urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login-original/", login_original, name="login_original"),
    path("dashboard-original/", dashboard_original, name="dashboard_original"),
    path("painel-aluno/", painel_aluno_original, name="painel_aluno_original"),

    path("api/demo/alunos", views.demo_alunos, name="demo_alunos"),
    path("api/demo/disciplinas", views.demo_disciplinas, name="demo_disciplinas"),
    path("api/demo/matriculas", views.demo_matriculas, name="demo_matriculas"),
    path("api/demo/kpis", views.demo_kpis, name="demo_kpis"),
    path("api/demo/risco/<int:aluno_id>", views.demo_risco, name="demo_risco"),
]
