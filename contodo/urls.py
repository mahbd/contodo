from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('cf/', include('codeforces.urls')),
    path('', include('main.urls')),
]
