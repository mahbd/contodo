from datetime import timedelta

from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .scrapper import get_cf_contest_list, get_at_contest_list, get_lt_contest_list
from .todoist import add_task
from .forms import ContestForm
from .models import Contest, PushedContest

User = get_user_model()


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
    cf_list = [(contest[0], contest[1], contest[2], Contest.JUDGE_CF) for contest in cf_list]
    at_list = get_at_contest_list()
    at_list = [(contest[0], contest[1], contest[2], Contest.JUDGE_AT) for contest in at_list]
    lc_list = get_lt_contest_list()
    lc_list = [(contest[0], contest[1], contest[2], Contest.JUDGE_LC) for contest in lc_list]
    all_contest = cf_list + at_list + lc_list
    for contest in all_contest:
        if not Contest.objects.filter(unique_id=contest[1]).exists():
            c_obj = Contest(name=contest[0], judge=contest[3], url=contest[1],
                            start_time=contest[2], unique_id=contest[1])
            c_obj.save()
            print('Contest added: ', contest[0])
    return redirect('main:contest_list')


def push_contest(request):
    user_list = User.objects.all()
    contest_list = Contest.objects.all()
    for user in user_list:
        if not user.todo_token:
            continue
        for contest in contest_list:
            if contest.start_time < timezone.now():
                continue
            if contest.start_time > timezone.now() + timedelta(days=5):
                continue
            if PushedContest.objects.filter(user=user, contest=contest):
                continue
            content = f"[{contest.name}]({contest.url})"
            task_id = add_task(user.todo_token, content, contest.start_time)
            if task_id:
                PushedContest(user=user, contest=contest, task_id=task_id).save()
                print('Task added: ', contest.name)
            else:
                print("Failed to add task: ", contest.name)
    return redirect('main:contest_list')
