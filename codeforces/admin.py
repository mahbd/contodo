from django.contrib import admin

from .models import CFUsers, TargetProblems, TargetSolves, Submissions


@admin.register(CFUsers)
class CFUsersAdmin(admin.ModelAdmin):
    list_display = ('handle', 'name', 'photo', 'last_submission')
    search_fields = ('handle', 'name')


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
    list_display = ('problem_name', 'problem_link', 'user')
    search_fields = ('problem_name', 'user__name', 'user__handle')
    list_filter = ('user', 'contest_id', 'problem_name')
