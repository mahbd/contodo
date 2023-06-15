from django.db import models


class CFUsers(models.Model):
    handle = models.CharField(max_length=63, primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    photo = models.URLField(max_length=255, blank=True, null=True)
    last_submission = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return self.handle


class TargetSolves(models.Model):
    STATUS_NOT_READ = 'N'
    STATUS_READ = 'R'
    STATUS_TRIED = 'T'
    STATUS_SOLVED = 'S'
    STATUS_CHOICES = [
        (STATUS_NOT_READ, 'Not Read'),
        (STATUS_READ, 'Read'),
        (STATUS_TRIED, 'Tried'),
        (STATUS_SOLVED, 'Solved'),
    ]

    user = models.ForeignKey(CFUsers, on_delete=models.CASCADE)
    problem = models.ForeignKey('TargetProblems', on_delete=models.CASCADE)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default=STATUS_NOT_READ)
    last_change = models.DateTimeField(blank=True, null=True)


class TargetProblems(models.Model):
    problem_name = models.CharField(max_length=255)
    link = models.URLField(max_length=255, primary_key=True)
    date = models.DateField(auto_now_add=True)
    users = models.ManyToManyField(CFUsers)


class Submissions(models.Model):
    problem_link = models.URLField(max_length=255)
    problem_name = models.CharField(max_length=255)
    contest_id = models.IntegerField()
    problem_id = models.CharField(max_length=7)
    user = models.ForeignKey(CFUsers, on_delete=models.CASCADE)
