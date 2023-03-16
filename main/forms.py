from django.forms import ModelForm

from .models import Contest


class ContestForm(ModelForm):
    class Meta:
        model = Contest
        fields = ['name', 'start_time', 'end_time', 'description', 'unique_id']
