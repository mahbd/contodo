from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('contests/', views.contest_list, name='contest_list'),
    path('contests/add/', views.add_contest, name='add_contest'),
    path('contests/<int:contest_id>/edit/', views.edit_contest, name='edit_contest'),
    path('contests/fetch/', views.fetch_contest, name='fetch_contest'),
]
