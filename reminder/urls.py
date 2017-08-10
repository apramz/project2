from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^create-team/$', views.create_team, name='create_team'),
	url(r'^create-roommate/$', views.create_roommate, name='create_roommate'),
	url(r'^create-chore/(?P<slug>[^\.]+)/$', views.create_chore, name='create_chore'),
	url(r'^roommate/(?P<slug>[^\.]+)/$', views.view_roommate, name='view_roommate'),
	url(r'^chore/(?P<slug>[^\.]+)/$', views.view_chore, name='view_chore'),
	url(r'^alert-later/(?P<slug>[^\.]+)/$', views.alert_later, name='alert_later'),
	url(r'^alert-now/(?P<slug>[^\.]+)/$', views.alert_now, name='alert_now'),
	url(r'^alert-recurring/(?P<slug>[^\.]+)/$', views.alert_recurring, name='alert_recurring'),
	url(r'^(?P<slug>[^\.]+)/$', views.view_team, name='view_team'),
]