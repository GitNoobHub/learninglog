'''define learning_logs's URL'''

from django.urls import path,re_path

from . import views

app_name = 'learning_logs'
urlpatterns = [
	#homepage
	path('',views.index,name='index'),
	#show all topics
	path('topics/',views.topics,name='topics'),
	#show specific topic's page
	re_path(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
	#page for adding new topic
	path('new_topic/', views.new_topic, name='new_topic'),
	# page for adding new entry
	re_path(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry,
	 name='new_entry'),
	# page for editing entry
	re_path(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry,
		name='edit_entry'),
	]

