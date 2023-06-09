from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Contest(models.Model):
    JUDGE_CF = 'Codeforces'
    JUDGE_AT = 'AtCoder'
    JUDGE_LC = 'LeetCode'
    JUDGE_TP = 'Toph'

    JUDGE_CHOICES = (
        (JUDGE_CF, 'Codeforces'),
        (JUDGE_AT, 'AtCoder'),
        (JUDGE_LC, 'LeetCode'),
        (JUDGE_TP, 'Toph'),
    )

    name = models.CharField(max_length=200)
    judge = models.CharField(max_length=50, choices=JUDGE_CHOICES)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    url = models.URLField()
    unique_id = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['start_time']


class PushedContest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    task_id = models.CharField(max_length=200)
    pushed_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.contest.name
