from datetime import timedelta

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .scrapper import get_cf_contest_list, get_at_contest_list, get_lt_contest_list
from .todoist import add_task, edit_task
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
    fetch_cnt = 0
    for contest in all_contest:
        prev = Contest.objects.filter(unique_id=contest[1])
        if prev:
            if prev[0].start_time != contest[2]:
                if prev[0].pushedcontest_set.all():
                    for pushed_contest in prev[0].pushedcontest_set.all():
                        token = pushed_contest.user.todo_token
                        content = f"[{contest[0]}]({contest[1]})"
                        if edit_task(token, content, contest[2], pushed_contest.task_id):
                            prev[0].start_time = contest[2]
                            prev[0].save()
                            print('Contest updated: ', contest[0])
                            fetch_cnt += 1
                        else:
                            print('Failed to update contest: ', contest[0])
        else:
            c_obj = Contest(name=contest[0], judge=contest[3], url=contest[1],
                            start_time=contest[2], unique_id=contest[1])
            c_obj.save()
            print('Contest added: ', contest[0])
            fetch_cnt += 1
    return HttpResponse(f'{fetch_cnt} contests fetched')


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
    return HttpResponse('Contest pushed')
