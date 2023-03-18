import json
from datetime import datetime, timedelta
import requests


def add_task(token, content, time: datetime):
    data = {
        'due_string': str(time),
        'content': content
    }
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    url = "https://api.todoist.com/rest/v2/tasks"
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200 or response.status_code == 201:
        json_obj = response.json()
        return json_obj['id']
    return False


def edit_task(token, content, time: datetime, task_id):
    url = f"https://api.todoist.com/rest/v2/tasks/{task_id}"
    data = {
        'due_string': str(time),
        'content': content
    }
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200 or response.status_code == 201:
        json_obj = response.json()
        return json_obj['id']
    return False
