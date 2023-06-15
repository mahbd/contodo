from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render

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
    problems = [[problem.problem_name].extend(
        [solve.status for solve in problem.targetsolves_set.all().order_by('user__name')])
        for problem in TargetProblems.objects.all().order_by('-date')]
    return render(request, 'codeforces/statistics.html', {
        'users': users,
        'problems': problems,
    })
