from django.shortcuts import render

from .models import Contest


def home(request):
    return render(request, 'main/home.html')


def contest_list(request):
    contests = Contest.objects.all()
    return render(request, 'main/contest_list.html', {'contests': contests})


def add_contest(request):
    return render(request, 'main/add_contest.html')
