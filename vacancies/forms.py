from django.forms import ModelForm

from .models import Application


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        # fields = '__all__'
        fields = ['written_username', 'written_phone', 'written_cover_letter']

