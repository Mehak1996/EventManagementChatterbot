from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
import json
import datetime 
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .Models.models import Event
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from django.core.files.storage import FileSystemStorage

chatbot = ChatBot(
    'Mehak',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)
chatbot.train("/Users/manpreetdhillon/Desktop/EventManagementChatterbot/eventApp/custom_corpus/mehak.yml")

# chatbot = ChatBot(
#     'Ron Obvious',
#     trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
# )
# # Train based on the english corpus
# chatbot.train("chatterbot.corpus.english")
# Train based on the english corpus

#Already trained and it's supposed to be persistent
#chatbot.train("chatterbot.corpus.english")
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

def homePage(request):
    return render(request,'login.html')
   
def login_request(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('listAll')
        #list_all_events(request);
        #return render(request, 'listAllEvents.html')

    else:
        messages.error(request, "Invalid username or password.")

def register(request):
    " register"
    return render(request, 'register.html')

def list_all_events(request):
    obj = Event.objects.all()
    context = {"totalEvents": obj}
    return render(request, 'listAllEvents.html',context)

def event_detail(request,eventId):
    obj = Event.objects.get(id=eventId)
    context = {"event": obj}
    return render(request, 'eventDetail.html',context)

def logout_request(request):
    logout(request)
    return redirect('login')

def edit_event(request,eventId):
    obj = Event.objects.get(id=eventId)
    formattedDate = obj.date.strftime("%m/%d/%Y")
    context = {"event": obj, "date": formattedDate}
    return render(request, 'addEvent.html',context)

def saveEvent(request,eventId,name,location, date, description):
    if eventId == '0':
        unformattedDate = request.POST.get('date')
        format_str = '%m/%d/%Y' # The format
        datetime_obj = datetime.datetime.strptime(unformattedDate, format_str)
        e = Event(name=request.POST.get('name'),location=request.POST.get('location'),date=datetime_obj,description=request.POST.get('description'))
        e.save();
    elif eventId:
        obj = Event.objects.get(id=eventId)
        obj.name = request.POST.get('name')
        obj.location = request.POST.get('location')
        date = request.POST.get('date')
        format_str = '%m/%d/%Y' # The format
        datetime_obj = datetime.datetime.strptime(date, format_str)
        obj.date = datetime_obj
        obj.description = request.POST.get('description')
        if request.method == "GET":
            files = request.FILES["image"]
            fs = FileSystemStorage()
            fs.save(files.name,files)
            obj.image.name = files.name
        obj.save()
    return redirect('listAll')


def deleteEvent(request,eventId):
    Event.objects.get(id=eventId).delete()
    return redirect('listAll')

def add_Event(request):
    context = {"event": {"id":0,"name":" ","date":" ","description":" ","location":" "}, "date": " "}
    return render(request, 'addEvent.html',context)

def floating_button(request):
    return render(request, 'floatingButton.html')