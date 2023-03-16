from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('contests/', views.contest_list, name='contest_list')
]
