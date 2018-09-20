from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic,Entry
from .forms import TopicForm,EntryForm
# Create your views here.

def check_topic_owner(request,topic):
	'''check owner'''
	# request topic belong to current user
	if topic.owner != request.user:
		raise Http404


def index(request):
	'''learning_log's homepage'''
	return render(request,'learning_logs/index.html')


@login_required
def topics(request):
	'''show all topics'''
	topics = Topic.objects.filter(owner=request.user).order_by('date_added')
	context = {'topics':topics}
	return render(request,'learning_logs/topics.html',context)


@login_required
def topic(request, topic_id):
	'''show single topic with its entries'''
	topic = Topic.objects.get(id=topic_id)
	check_topic_owner(request,topic)

	entries = topic.entry_set.order_by('-date_added')
	context = {'topic':topic,'entries':entries}
	return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
	''' add new topic'''
	if request.method != 'POST':
		#have not post stat,build a new form
		form = TopicForm()
	else:
		# POST's stat,solve these stat
		form = TopicForm(request.POST)
		if form.is_valid():
			new_topic = form.save(commit=False)
			new_topic.owner = request.user
			new_topic.save()
			return HttpResponseRedirect(reverse('learning_logs:topics'))

	context = {'form': form}
	return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
	'''add new_entry in specific topic'''
	topic = Topic.objects.get(id=topic_id)
	check_topic_owner(request,topic)

	if request.method != "POST":
		# have not submit stat,build a new form
		form = EntryForm()
	else:
		# POST stats,solve POST's stats
		form = EntryForm(data=request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.topic = topic
			new_entry.save()
			return HttpResponseRedirect(reverse('learning_logs:topic',
				args=[topic_id]))

	context = {'topic': topic, 'form': form}
	return render(request,'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
	'''edit old entry'''
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic

	check_topic_owner(request,topic)

	if request.method != 'POST':
		# first request,use current item to fill form
		form = EntryForm(instance=entry)
	else:
		# solve the stat of POST
		form = EntryForm(instance=entry,data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse("learning_logs:topic",
				args=[topic.id]))

	context = {'form':form,'entry':entry,'topic':topic}
	return render(request,'learning_logs/edit_entry.html', context)











