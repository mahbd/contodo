from django.shortcuts import render, redirect, get_object_or_404

from .models import Contest
from .forms import ContestForm


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
