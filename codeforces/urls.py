from django.urls import path

from . import views

app_name = 'codeforces'

urlpatterns = [
    path('stat/', views.statistics, name='statistics'),
    path('update/', views.update_statistics, name='update_statistics'),
    path('update-sync/', views.update_statistics, name='update_statistics_sync'),
]
