from django import forms

from .models import TalkerProfile


class TalkerProfileForm(forms.ModelForm):
    class Meta:
        model = TalkerProfile
        fields = ('avatar',)
