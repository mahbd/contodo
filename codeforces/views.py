import threading
import time

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.html import format_html

from .cf_api import update_last_online, get_submissions
from .models import CFUsers, TargetSolves, TargetProblems


@receiver(post_save, sender=CFUsers)
def new_user(sender, instance: CFUsers, created, **kwargs):
    if created:
        for problem in TargetProblems.objects.all():
            TargetSolves.objects.create(user=instance, problem=problem)


@receiver(post_save, sender=TargetProblems)
def new_problem(sender, instance: TargetProblems, created, **kwargs):
    if created:
        for user in CFUsers.objects.all():
            TargetSolves.objects.create(user=user, problem=instance)


def statistics(request):
    users = CFUsers.objects.all().order_by('name')
    problems = []
    for problem in TargetProblems.objects.all().order_by('-date'):
        problem_row = [format_html(f'<a href="{problem.link}">{problem.problem_name}</a>')]
        for solve in problem.targetsolves_set.all().order_by('user__name'):
            if solve.submission_link:
                problem_row.append(format_html(f'<a href="{solve.submission_link}">{solve.status}</a>'))
            else:
                problem_row.append(solve.status)
        problems.append(problem_row)
    return render(request, 'codeforces/statistics.html', {
        'users': users,
        'problems': problems,
        'update_url': reverse('codeforces:update_statistics_sync')
    })


def _update_statistics():
    for user in CFUsers.objects.all():
        update_last_online(user.handle)
        time.sleep(.1)
        get_submissions(user.handle, 20)
        time.sleep(.1)


def update_statistics(request):
    threading.Thread(target=_update_statistics).start()
    return HttpResponse('Updating statistics')


def update_statistics_sync(request):
    _update_statistics()
    return HttpResponse('Updating statistics')
