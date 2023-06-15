from django.urls import path

from . import views

app_name = 'codeforces'

urlpatterns = [
    path('stat/', views.statistics, name='statistics'),
]
