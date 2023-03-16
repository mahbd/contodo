from django.contrib import admin

from .models import Contest, PushedContest


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ('name', 'judge', 'start_time', 'url', 'unique_id')
    list_filter = ('judge', 'start_time', 'end_time')
    search_fields = ('name', 'url', 'unique_id')


@admin.register(PushedContest)
class PushedContestAdmin(admin.ModelAdmin):
    list_display = ('user', 'contest', 'pushed_time')
    list_filter = ('pushed_time', 'contest__judge', 'user__username')
    search_fields = ('user__username', 'contest__name')
