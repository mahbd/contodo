from django.contrib.auth import get_user_model
from django.db import models

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
    end_time = models.DateTimeField()
    description = models.TextField()
    url = models.URLField()
    unique_id = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class PushedContest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    pushed_time = models.DateTimeField()

    def __str__(self):
        return self.contest.name
