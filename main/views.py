from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404

from .scrapper import get_cf_contest_list, get_at_contest_list, get_lt_contest_list
from .forms import ContestForm
from .models import Contest


def home(request):
    return render(request, 'main/home.html')


def contest_list(request):
    contests = Contest.objects.all()
    return render(request, 'main/contest_list.html', {'contests': contests})


def add_contest(request):
    if request.method != 'POST':
        form = ContestForm()
    else:
        form = ContestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:contest_list')
    return render(request, 'main/contest_form.html', {'form': form})


def edit_contest(request, contest_id):
    contest = get_object_or_404(Contest, id=contest_id)
    if request.method != 'POST':
        form = ContestForm(instance=contest)
    else:
        form = ContestForm(instance=contest, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:contest_list')
    return render(request, 'main/contest_form.html', {'form': form, 'contest': contest})


def fetch_contest(request):
    cf_list = get_cf_contest_list()
    at_list = get_at_contest_list()
    lc_list = get_lt_contest_list()
    bdt = timedelta(hours=6)
    for contest in cf_list:
        if not Contest.objects.filter(unique_id=contest[1]).exists():
            c_obj = Contest(name=contest[0], judge=Contest.JUDGE_CF, url=contest[1],
                            start_time=contest[2] + bdt, unique_id=contest[1])
            c_obj.save()
            print('Contest added: ', contest[0])
    for contest in at_list:
        if not Contest.objects.filter(unique_id=contest[1]).exists():
            c_obj = Contest(name=contest[0], judge=Contest.JUDGE_AT, url=contest[1],
                            start_time=contest[2] + bdt, unique_id=contest[1])
            c_obj.save()
            print('Contest added: ', contest[0])
    for contest in lc_list:
        if not Contest.objects.filter(unique_id=contest[1]).exists():
            c_obj = Contest(name=contest[0], judge=Contest.JUDGE_LC, url=contest[1],
                            start_time=contest[2] + bdt, unique_id=contest[1])
            c_obj.save()
            print('Contest added: ', contest[0])
    return redirect('main:contest_list')
