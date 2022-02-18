
### TESTING ###

from django import forms
from .models import Talk

class NewTalkForm(forms.ModelForm):
	class Meta:
		model = Talk
		fields = ['body', 'pic', 'tags']

""" class NewCommentForm(forms.ModelForm):
	class Meta:
		model = Comments
		fields = ['comment'] """