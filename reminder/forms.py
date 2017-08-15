from django import forms
from django.utils.text import slugify
from django.forms import ModelForm

from .models import Team, Roommate, Chore

class TeamForm(ModelForm):
	class Meta:
		model = Team
		fields = ['name']

	def save(self, user):
		instance = super(TeamForm, self).save(commit=False)
		instance.slug = slugify(instance.name)
		instance.user = user
		instance.save()
		return instance

class RoommateForm(ModelForm):
	class Meta:
		model = Roommate
		fields = ['name', 'team', 'phone_number']

	def __init__(self, user, *args, **kwargs):
		super(RoommateForm, self).__init__(*args, **kwargs)
		self.fields['team'].queryset = Team.objects.filter(user=user)

	def save(self):
		instance = super(RoommateForm, self).save(commit=False)
		instance.slug = slugify(instance.name)
		instance.save()
		return instance

class ChoreForm(ModelForm):
	class Meta:
		model = Chore
		fields = ['name', 'description', 'deadline', 'roommate']
		widgets = {
			'description': forms.Textarea(attrs={'rows':5, 'cols':30}),
		}

	def __init__(self, team, *args, **kwargs):
		super(ChoreForm, self).__init__(*args, *kwargs)
		self.fields['roommate'].queryset = Roommate.objects.filter(team=team)

	def save(self, team):
		instance = super(ChoreForm, self).save(commit=False)
		instance.slug = slugify(instance.name)
		instance.team = team
		instance.save()
		return instance

class AlertLaterForm(forms.Form):
	date = forms.DateTimeField(label='When do you want to send the alert?')

class AlertRecurringForm(forms.Form):
	DAY_CHOICES = (
			('Monday', 'Monday'),
			('Tuesday', 'Tuesday'),
			('Wednesday', 'Wednesday'),
			('Thursday', 'Thursday'),
			('Friday', 'Friday'),
			('Saturday', 'Saturday'),
			('Sunday', 'Sunday'),
		)
	day = forms.ChoiceField(choices=DAY_CHOICES)
	time = forms.TimeField()