from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
import datetime
from django.utils import timezone

class Team(models.Model):
	name = models.CharField(max_length=100)
	created = models.DateTimeField(default = timezone.now)
	#timezone (if global support necessary)
	user = models.ForeignKey(User, related_name='teams')
	slug = models.SlugField(max_length=100)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('view_team', kwargs={'slug': self.slug})

class Roommate(models.Model):
	name = models.CharField(max_length=50)
	team = models.ForeignKey('Team', related_name='roommates')
	phone_number = PhoneNumberField()
	slug = models.SlugField(max_length=100)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('view_roommate', kwargs={'slug': self.slug})

class Chore(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField()
	deadline = models.DateTimeField()
	roommate = models.ForeignKey('Roommate', related_name='chores')
	team = models.ForeignKey('Team', related_name='chores')
	slug = models.SlugField(max_length=100)
	STATUS_OPTIONS = (
		('Y', 'Complete'),
		('N', 'Incomplete'),
	)
	status = models.CharField(
		max_length = 1,
		choices = STATUS_OPTIONS,
		default = 'N',
		)

	def is_complete(self):
		self.status = 'Y'
		self.save()

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('view_chore', kwargs={'slug': self.slug})
