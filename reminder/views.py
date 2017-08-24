import os, sched, schedule, time, datetime, pytz
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from reminder.models import Team, Roommate, Chore
from reminder.forms import TeamForm, RoommateForm, ChoreForm, AlertLaterForm, AlertRecurringForm

from twilio.rest import Client

@login_required
def index(request):
	current_user = request.user
	teams = current_user.teams.all()
	return render(request, 'reminder/index.html', {'teams': teams})

def signup(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('index')
	else:
		form = UserCreationForm()
	return render(request, 'registration/signup.html', {'form': form})

def create_team(request):
	current_user = request.user
	if request.method == 'POST':
		form = TeamForm(request.POST)
		if form.is_valid():
			team = form.save(current_user)
			return redirect('index')
	else:
		form = TeamForm()
	return render(request, 'registration/create_team.html', {'form': form})

def create_roommate(request):
	current_user = request.user
	if request.method == "POST":
		form = RoommateForm(current_user, request.POST)
		if form.is_valid():
			roommate = form.save()
			return redirect('view_team')
	else:
		form = RoommateForm(current_user)
	return render(request, 'registration/create_roommate.html', {'form': form})

def create_chore(request, slug):
	team = get_object_or_404(Team, slug=slug)
	if request.method == "POST":
		form = ChoreForm(team, request.POST)
		if form.is_valid():
			chore = form.save(team)
			return redirect('view_team', slug=team.slug)
	else:
		form = ChoreForm(team)
	return render(request, 'registration/create_chore.html', {'form': form})

def view_team(request, slug):
	return render(request, 'reminder/view_team.html', {
			'team': get_object_or_404(Team, slug=slug)
		})

def view_roommate(request, slug):
	return render(request, 'reminder/view_roommate.html', {
			'roommate': get_object_or_404(Roommate, slug=slug),
			'team': get_object_or_404(Roommate, slug=slug).team
		})
 
def view_chore(request, slug):
	alertlater_form = AlertLaterForm()
	alertrecurring_form = AlertRecurringForm()
	return render(request, 'reminder/view_chore.html', {
			'chore': get_object_or_404(Chore, slug=slug),
			'alertlater_form': alertlater_form,
			'alertrecurring_form': alertrecurring_form,
			'team': get_object_or_404(Chore, slug=slug).team,
			'roommate': get_object_or_404(Chore, slug=slug).roommate
		})

#Twilio Views
def alert_now(request, slug):
	#Twilio Setup
	account_sid = "AC28c62e521145b961ad432ec7f6050fce"
	auth_token = "27061d0c4ca70a43f1ffdb8e4572ae66"
	client = Client(account_sid, auth_token)

	#My Stuff
	chore = get_object_or_404(Chore, slug=slug)
	phone_num = chore.roommate.phone_number

	client.messages.create(
		to = str(phone_num),
		from_ = "+16692207006",
		body = str(' '.join([chore.name, chore.description]))
		)

	return render(request, 'reminder/view_chore.html', {
			'chore': chore
		})

def alert_later(request, slug):
	#Set up Twilio function to send text message
	def send_message(slug):
		#Twilio Setup
		account_sid = "AC28c62e521145b961ad432ec7f6050fce"
		auth_token = "27061d0c4ca70a43f1ffdb8e4572ae66"
		client = Client(account_sid, auth_token)

		chore = get_object_or_404(Chore, slug=slug)
		phone_num = chore.roommate.phone_number

		client.messages.create(
		to = str(phone_num),
		from_ = "+16692207006",
		body = str(' '.join([chore.name, chore.description]))
		)

	#Incorporates the sending date/time and uses while loop to pause function until the right time
	raw_datetime = request.POST.get('date')
	print (raw_datetime)
	datetime_format = '%m/%d/%Y %I:%M %p'
	future_datetime = datetime.datetime.strptime(raw_datetime, datetime_format)

	while datetime.datetime.now() < future_datetime:
		time.sleep(1)

	send_message(slug)
	return HttpResponse('Woot')

def alert_recurring(request, slug):
	#Set up Twilio function to send text message
	def send_message(slug):
		#Twilio Setup
		account_sid = "AC28c62e521145b961ad432ec7f6050fce"
		auth_token = "27061d0c4ca70a43f1ffdb8e4572ae66"
		client = Client(account_sid, auth_token)

		chore = get_object_or_404(Chore, slug=slug)
		phone_num = chore.roommate.phone_number

		client.messages.create(
		to = str(phone_num),
		from_ = "+16692207006",
		body = str(' '.join([chore.name, chore.description]))
		)
	#Pulling from the relevant Chore object
	chore = get_object_or_404(Chore, slug=slug)
	raw_datetime = chore.deadline

	#Converting Chore deadline to aware timezone object
	future_datetime = raw_datetime.replace(tzinfo=None)
	#Pulling from the Request object
	day = request.POST.get('day').lower()
	raw_time = str(request.POST.get('time'))
	time_ = str(datetime.datetime.strptime(raw_time, '%I:%M %p').time())[:-3]  

	def schedule_process(day, time_, slug):
		sched1 = schedule.every()
		sched2 = getattr(sched1, day)
		sched3 = sched2.at(time_).do(send_message, slug).tag(slug)
		return sched3
	job = schedule_process(day, time_, slug)

	print (datetime.datetime.now() < future_datetime )

	#Scheduling - While loop keeps function online until deadline
	while datetime.datetime.now() < future_datetime:
		schedule.run_pending()
		time.sleep(1)


	return HttpResponse('Woot')