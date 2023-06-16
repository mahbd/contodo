from datetime import datetime, timedelta
from typing import Union

import pytz
import requests

from .models import Submissions, CFUsers, TargetSolves, TargetProblems


DHAKA_TZ = pytz.timezone('Asia/Dhaka')


def get_submissions(handle: str, count=10000) -> Union[bool, int]:
    user = CFUsers.objects.filter(handle=handle).first()
    if not user:
        return False
    res = requests.get(f'https://codeforces.com/api/user.status?handle={handle}&from=1&count={count}')
    if res.status_code != 200:
        return False
    new_added = 0
    for submission in res.json()['result']:
        contest_id = submission['problem']['contestId']
        problem_id = submission['problem']['index']
        problem_name = submission['problem']['name'].strip()
        submitted_at = datetime.fromtimestamp(submission['creationTimeSeconds'], tz=DHAKA_TZ) + timedelta(hours=3)
        submission_status = Submissions.STATUS_SOLVED if submission['verdict'] == 'OK' else Submissions.STATUS_TRIED
        problem_link = f'https://codeforces.com/contest/{contest_id}/problem/{problem_id}'
        if not Submissions.objects.filter(problem_name=problem_name, user__handle=handle).exists():
            new_submission = Submissions()
            new_submission.problem_name = problem_name
            new_submission.problem_link = problem_link
            new_submission.contest_id = contest_id
            new_submission.problem_id = problem_id
            new_submission.user_id = user.handle
            new_submission.status = submission_status
            new_submission.submitted_at = submitted_at
            new_submission.save()
            new_added += 1
            if TargetProblems.objects.filter(problem_name=problem_name).exists():
                target_solve = TargetSolves.objects.filter(user=user, problem__problem_name=problem_name).first()
                if not target_solve:
                    target_solve = TargetSolves()
                    target_solve.user = user
                    target_solve.problem = TargetProblems.objects.filter(problem_name=problem_name).first()
                    target_solve.status = TargetSolves.STATUS_SOLVED if submission_status == Submissions.STATUS_SOLVED \
                        else TargetSolves.STATUS_TRIED
                target_solve.save()

    return new_added


def update_last_online(handle: str) -> bool:
    res = requests.get(f'https://codeforces.com/api/user.info?handles={handle}')
    if res.status_code != 200:
        return False
    last_online = res.json()['result'][0]['lastOnlineTimeSeconds']
    last_online = datetime.fromtimestamp(last_online,
                                         tz=pytz.timezone('Asia/Dhaka')) + timedelta(hours=3)
    user = CFUsers.objects.filter(handle=handle).first()
    if not user:
        return False
    user.last_online = last_online
    user.save()
    if last_online.date() == datetime.today().date() and last_online.hour >= 6:
        target_solve = TargetSolves.objects.filter(user=user, problem__date=datetime.today().date()).first()
        if target_solve:
            target_solve.status = TargetSolves.STATUS_READ
            target_solve.save()
    return True
