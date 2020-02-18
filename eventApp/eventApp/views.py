from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .Models.models import Testt

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot(
    'Mehak',
)
trainer = ChatterBotCorpusTrainer(chatbot.storage)
trainer.train("/Users/mehakluthra/Documents/Event_Management_Chatterbot/eventApp/custom_corpus/mehak.yml")
# Train based on the english corpus

#Already trained and it's supposed to be persistent
#chatbot.train("chatterbot.corpus.english")

@csrf_exempt
def get_response(request):
	response = {'status': None}

	if request.method == 'POST':
		data = json.loads(request.body.decode('utf-8'))
		message = data['message']

		chat_response = chatbot.get_response(message).text
		response['message'] = {'text': chat_response, 'user': False, 'chat_bot': True}
		response['status'] = 'ok'

	else:
		response['error'] = 'no post data found'

	return HttpResponse(
		json.dumps(response),
			content_type="application/json"
		)


def home(request, template_name="home.html"):
	context = {'title': 'Chatbot Version 1.0'}
	return render_to_response(template_name, context)

def homee(request):
    obj = Testt.objects.get(id=1)
    context = {"object": obj}
    return render(request,'login.html',context)
   
def login_request(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return render(request, 'listAllEvents.html')
    else:
        messages.error(request, "Invalid username or password.")

def register(request):
    " register"
    return render(request, 'register.html')

def list_all_events(request):
    " list"
    context = {"totalEvents": 6}
    return render(request, 'listAllEvents.html',context)

def event_detail(request):
    "detial"
    return render(request, 'eventDetail.html')

def logout_request(request):
    "detial"
    logout(request)
    return render(request, 'login.html')
