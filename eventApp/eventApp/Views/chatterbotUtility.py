from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
import json
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
from django.views.decorators.csrf import csrf_exempt
from eventApp.Views import dialog
from chatterbot.conversation import Statement
from chatterbot.conversation import Response
import datetime

chatbot = ChatBot(
    'Mehak',
    #trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='mysql://root:mehak1996@localhost/EventApp'
	
)

trainer = ListTrainer(chatbot.storage)
chatbot.read_only = True

dialogObj = dialog.Dialogs()
dialogs = dialogObj.get_dialog_data()

# chatbot.storage.drop()
# chatbot.train('/Users/mehakluthra/Documents/EventManagementChatterbot/eventApp/custom_corpus/mehak.yml')

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

def edit_converstaions(obj,objStatus):
	print('inside Edit conversations')   
	
	if (objStatus['address'] == 'Mod') or (objStatus['city'] == 'Mod'):
		edit_dialog_event_location (obj)
	if (objStatus['eventDate'] == 'Mod') :
		edit_dialog_event_date (obj)
	if (objStatus['eventType'] == 'Mod') :
		edit_dialog_event_type (obj)
	if (objStatus['eventTime'] == 'Mod'):
		edit_dialog_event_time (obj)
	if (objStatus['city'] == 'Mod'):
		edit_dialog_event_city (obj)
	edit_dialog_event_description(obj)

def formulate_conversations(obj):
	print('inside create conversations')
	create_dialog_event_location (obj.name, obj.city, obj.address)
	create_dialog_event_date (obj.name, obj.date)
	create_dialog_event_type (obj.name, obj.eventType)
	create_dialog_event_time (obj.name, obj.time)
	create_dialog_event_city (obj.name, obj.city)
	create_dialog_event_description (obj.name, obj.city, obj.address, obj.date, obj.time, obj.eventType, obj.description)

def create_dialog_event_location(name,city,address):
	ansLocationType = 'Location of the event ' + name + ' is '+ city + ' , ' + address

	for key in dialogs['location']:
		quesLocationType = dialogs['location'].get(key) + ' ' + name + ' ? '
		train_chatbot_with_question_answer( quesLocationType , ansLocationType )

def create_dialog_event_date(name,strDate):
	ansDateType = 'Date of the event ' + name + ' is ' + strDate.strftime('%m/%d/%Y')

	for key in dialogs['date']:
		quesLocationType = dialogs['date'].get(key) + ' ' + name + ' ? '
		train_chatbot_with_question_answer( quesLocationType , ansDateType )

def create_dialog_event_type(name,eventType):
	ansDateType = 'Event type for the event ' + name + ' is ' + eventType

	for key in dialogs['type']:
		quesLocationType = dialogs['type'].get(key) + ' ' + name + ' ? '
		train_chatbot_with_question_answer( quesLocationType , ansDateType )

def create_dialog_event_time(name,eventTime):
	ansEventTime = 'Time of the event ' + name + ' is ' + eventTime

	for key in dialogs['time']:
		quesLocationType = dialogs['time'].get(key) + ' ' + name + ' ? '
		train_chatbot_with_question_answer( quesLocationType , ansEventTime )

def create_dialog_event_city(name,eventCity):
	ansEventCity = 'City of the event ' + name + ' is ' + eventCity

	for key in dialogs['city']:
		quesLocationType = dialogs['city'].get(key) + ' ' + name + ' ? '
		train_chatbot_with_question_answer( quesLocationType , ansEventCity )

def create_dialog_event_description(name, city, address, strDate, time, eventType, description):
	ansEventDescription =  'Event Name : ' + name + '\n' +  'Location: ' + city + ' , ' + address + '\n' + 'Date: ' + strDate.strftime('%m/%d/%Y') + '\n' + 'Time: ' + time + '\n' + 'Event Type: ' + eventType + '\n' + 'Description: ' + description

	for key in dialogs['description']:
		quesLocationType = dialogs['description'].get(key) + ' ' + name + ' ? '
		train_chatbot_with_question_answer( quesLocationType , ansEventDescription )

def edit_dialog_event_location(obj):
	quesLocationType = dialogs['location']['ques1'] + ' ' + obj.name + ' ? '
	oldResponse = chatbot.get_response(quesLocationType)
	remove_statement(oldResponse)
		
	create_dialog_event_location (obj.name, obj.city, obj.address)

def edit_dialog_event_date(obj):
	quesDateType = dialogs['date']['ques1'] + ' ' + obj.name + ' ? '
	oldResponse = chatbot.get_response(quesDateType)
	remove_statement(oldResponse)

	create_dialog_event_date(obj.name, obj.date)

def edit_dialog_event_type(obj):
	quesEventType = dialogs['type']['ques1'] + ' ' + obj.name + ' ? '
	oldResponse = chatbot.get_response(quesEventType)
	remove_statement(oldResponse)
		
	create_dialog_event_type (obj.name, obj.eventType)

def edit_dialog_event_time(obj):
	quesEventTime = dialogs['time']['ques1'] + ' ' + obj.name + ' ? '
	oldResponse = chatbot.get_response(quesEventTime)
	remove_statement(oldResponse)
		
	create_dialog_event_time (obj.name, obj.time)

def edit_dialog_event_city(obj):
	quesEventCity = dialogs['city']['ques1'] + ' ' + obj.name + ' ? '
	oldResponse = chatbot.get_response(quesEventCity)
	remove_statement(oldResponse)
		
	create_dialog_event_city (obj.name, obj.city)

def edit_dialog_event_description(obj):
	quesEventDesc = dialogs['description']['ques1'] + ' ' + obj.name + ' ? '
	oldResponse = chatbot.get_response(quesEventDesc)
	remove_statement(oldResponse)
		
	create_dialog_event_description (obj.name, obj.city, obj.address, obj.date, obj.time, obj.eventType, obj.description)
	
def train_chatbot_with_question_answer(question, answer):
	chatbot.read_only = False
	trainer.train([question,answer])
	chatbot.read_only = True

def remove_statement(strStatement):
	chatbot.storage.remove(strStatement)




