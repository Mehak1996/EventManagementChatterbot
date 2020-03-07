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
dialogsQues = dialogObj.get_dialog_data('ques')
dialogResp = dialogObj.get_dialog_data('ans')

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

def edit_converstaions(oldObj, obj,objStatus):
	print('inside Edit conversations')   
	
	if (objStatus['address'] == 'Mod') or (objStatus['city'] == 'Mod'):
		edit_dialog_event_location (oldObj , obj)
	if (objStatus['eventDate'] == 'Mod') :
		edit_dialog_event_date (oldObj, obj)
	if (objStatus['eventType'] == 'Mod') :
		edit_dialog_event_type (oldObj, obj)
	if (objStatus['eventTime'] == 'Mod'):
		edit_dialog_event_time (oldObj, obj)
	if (objStatus['city'] == 'Mod'):
		edit_dialog_event_city (oldObj, obj)
	edit_dialog_event_description(oldObj, obj)

def formulate_conversations(obj):
	print('inside create conversations')
	create_dialog_event_location (obj.name, obj.city, obj.address)
	create_dialog_event_date (obj.name, obj.date)
	create_dialog_event_type (obj.name, obj.eventType)
	create_dialog_event_time (obj.name, obj.time)
	create_dialog_event_city (obj.name, obj.city)
	create_dialog_event_description (obj.name, obj.city, obj.address, obj.date, obj.time, obj.eventType, obj.description)

def create_dialog_event_location(name,city,address):
	ansLocationType = dialogResp['location'].get('res') + name + ' is '+ city + ' , ' + address

	for key in dialogsQues['location']:
		quesLocationType = dialogsQues['location'].get(key) + ' ' + name + ' ? '
		train_chatbot_with_question_answer( quesLocationType , ansLocationType )

def create_dialog_event_date(name,strDate):
	ansDateType = dialogResp['date'].get('res') + name + ' is ' + strDate.strftime('%m/%d/%Y')

	for key in dialogsQues['date']:
		quesLocationType = dialogsQues['date'].get(key) + ' ' + name + ' ? '
		train_chatbot_with_question_answer( quesLocationType , ansDateType )

def create_dialog_event_type(name,eventType):
	ansDateType = dialogResp['type'].get('res') + name + ' is ' + eventType

	for key in dialogsQues['type']:
		quesLocationType = dialogsQues['type'].get(key) + ' ' + name + ' ? '
		train_chatbot_with_question_answer( quesLocationType , ansDateType )

def create_dialog_event_time(name,eventTime):
	ansEventTime = dialogResp['time'].get('res') + name + ' is ' + eventTime

	for key in dialogsQues['time']:
		quesLocationType = dialogsQues['time'].get(key) + ' ' + name + ' ? '
		train_chatbot_with_question_answer( quesLocationType , ansEventTime )

def create_dialog_event_city(name,eventCity):
	ansEventCity = dialogResp['city'].get('res') + name + ' is ' + eventCity

	for key in dialogsQues['city']:
		quesLocationType = dialogsQues['city'].get(key) + ' ' + name + ' ? '
		train_chatbot_with_question_answer( quesLocationType , ansEventCity )

def create_dialog_event_description(name, city, address, strDate, eventTime, eventType, description):
	ansEventDescription = 'Event Name : ' + name + '\n' +  'Location: ' + city + ' , ' + address + '\n' + 'Date: ' + strDate.strftime('%m/%d/%Y') + '\n' + 'Time: ' + eventTime + '\n' + 'Event Type: ' + eventType + '\n' + 'Description: ' + description
	
	for key in dialogsQues['description']:
		quesLocationType = dialogsQues['description'].get(key) + ' ' + name + ' ? '
		train_chatbot_with_question_answer( quesLocationType , ansEventDescription )

def edit_dialog_event_location(oldObj, obj):
	textOldResponse = dialogResp['location'].get('res') + oldObj.name + ' is '+ oldObj.city + ' , ' + oldObj.address
	remove_old_response (textOldResponse)
	
	create_dialog_event_location (obj.name, obj.city, obj.address)

def edit_dialog_event_date(oldObj, obj):
	textOldResponse = dialogResp['date'].get('res') + oldObj.name + ' is ' + oldObj.date.strftime('%m/%d/%Y')
	remove_old_response (textOldResponse)

	create_dialog_event_date(obj.name, obj.date)

def edit_dialog_event_type(oldObj, obj):
	textOldResponse = dialogResp['type'].get('res') + oldObj.name + ' is ' + oldObj.type
	remove_old_response (textOldResponse)
		
	create_dialog_event_type (obj.name, obj.eventType)

def edit_dialog_event_time(oldObj, obj):
	textOldResponse = dialogResp['time'].get('res') + oldObj.name + ' is ' + convertTimeToStr (oldObj.time)
	remove_old_response (textOldResponse)
		
	create_dialog_event_time (obj.name, obj.time)

def edit_dialog_event_city(oldObj, obj):
	textOldResponse = dialogResp['city'].get('res') + oldObj.name + ' is ' + oldObj.city
	remove_old_response (textOldResponse)
		
	create_dialog_event_city (obj.name, obj.city)

def edit_dialog_event_description(oldObj, obj):
	textOldResponse = 'Event Name : ' + oldObj.name + '\n' +  'Location: ' + oldObj.city + ' , ' + oldObj.address + '\n' + 'Date: ' + oldObj.date.strftime('%m/%d/%Y') + '\n' + 'Time: ' + convertTimeToStr(oldObj.time) + '\n' + 'Event Type: ' + oldObj.eventType + '\n' + 'Description: ' + oldObj.description
	remove_old_response (textOldResponse)
		
	create_dialog_event_description (obj.name, obj.city, obj.address, obj.date, obj.time, obj.eventType, obj.description)
	
def train_chatbot_with_question_answer(question, answer):
	chatbot.read_only = False
	trainer.train([question,answer])
	chatbot.read_only = True

def remove_old_response(strStatement):
	oldResponse = Statement (text = strStatement)
	chatbot.storage.remove(oldResponse)

def convertTimeToStr(timeObj):
	minutes= str(timeObj.minute).zfill(2)
	formattedTime = str(timeObj.hour)+":"+ str(minutes)+ " "
	return formattedTime



