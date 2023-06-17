from django.contrib import admin

from .cf_api import get_submissions, update_last_online
from .models import CFUsers, TargetProblems, TargetSolves, Submissions, Logs


@admin.register(CFUsers)
class CFUsersAdmin(admin.ModelAdmin):
    actions = ['fetch_submissions', 'fetch_all_submissions', 'update_last_online']
    list_display = ('handle', 'name', 'last_online', 'last_submission')
    search_fields = ('handle', 'name')

    def fetch_submissions(self, request, queryset):
        count = 0
        for user in queryset:
            count += get_submissions(user.handle, 20)
        self.message_user(request, f'{count} new submissions added')

    fetch_submissions.short_description = 'Fetch submissions'

    def fetch_all_submissions(self, request, queryset):
        count = 0
        for user in queryset:
            count += get_submissions(user.handle, 10000)
        self.message_user(request, f'{count} new submissions added')

    fetch_all_submissions.short_description = 'Fetch all submissions'

    def update_last_online(self, request, queryset):
        count = 0
        for user in queryset:
            count += update_last_online(user.handle)
        self.message_user(request, f'{count} users updated')

    update_last_online.short_description = 'Update last online'


@admin.register(TargetProblems)
class TargetProblemsAdmin(admin.ModelAdmin):
    list_display = ('problem_name', 'link', 'date')
    search_fields = ('problem_name',)


@admin.register(TargetSolves)
class TargetSolvesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'problem', 'status', 'last_change')
    search_fields = ('user__name', 'user__handle', 'problem')
    list_filter = ('status', 'user', 'problem', 'last_change')


@admin.register(Submissions)
class SubmissionsAdmin(admin.ModelAdmin):
    list_display = ('problem_name', 'user', 'problem_link', 'status', 'created_at')
    search_fields = ('problem_name', 'user__name', 'user__handle')
    list_filter = ('created_at', 'user', 'contest_id', 'problem_name')


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('message', 'created_at')
    search_fields = ('message',)
    list_filter = ('created_at',)
