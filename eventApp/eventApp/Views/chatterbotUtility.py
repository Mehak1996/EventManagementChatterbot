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

class ChatbotUtility():

	chatbot = ChatBot(
		'Event_App_Chatbot',
		#trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
		storage_adapter='chatterbot.storage.SQLStorageAdapter',
		database_uri='mysql://root:mehak1996@localhost/EventApp',
		logic_adapters=[
				{
					"import_path": "chatterbot.logic.BestMatch",
					"statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
				},

				{
					'import_path': 'chatterbot.logic.LowConfidenceAdapter',
					'threshold': 0.85,
					'default_response': 'I am sorry, I did not find answer for you request.\n This is an automated chatbot, please try with different question.'
				},
			],
	)

	trainer = ListTrainer(chatbot.storage)
	chatbot.read_only = True

	dialogObj = dialog.Dialogs()
	dialogsQues = dialogObj.get_dialog_data('ques')
	dialogResp = dialogObj.get_dialog_data('ans')

	# chatbot.storage.drop()
	# chatbot.train('/Users/mehakluthra/Documents/EventManagementChatterbot/eventApp/custom_corpus/mehak.yml')

	@csrf_exempt
	def get_response(self,request):
		response = {'status': None}

		if request.method == 'POST':
			data = json.loads(request.body.decode('utf-8'))
			message = data['message']

			chat_response = self.chatbot.get_response(message).text
			response['message'] = {'text': chat_response, 'user': False, 'chat_bot': True}
			response['status'] = 'ok'

		else:
			response['error'] = 'no post data found'

		return HttpResponse(
			json.dumps(response),
				content_type="application/json"
			)

	def edit_converstaions(self, oldObj, obj,objStatus):
		print('inside Edit conversations')   
		
		if (objStatus['address'] == 'Mod') or (objStatus['city'] == 'Mod'):
			self.edit_dialog_event_location (oldObj , obj)
		if (objStatus['eventDate'] == 'Mod') :
			self.edit_dialog_event_date (oldObj, obj)
		if (objStatus['eventType'] == 'Mod') :
			self.edit_dialog_event_type (oldObj, obj)
		if (objStatus['eventTime'] == 'Mod'):
			self.edit_dialog_event_time (oldObj, obj)
		if (objStatus['city'] == 'Mod'):
			self.edit_dialog_event_city (oldObj, obj)
		self.edit_dialog_event_description(oldObj, obj)

	def formulate_conversations(self, obj):
		print('inside create conversations')
		self.create_dialog_event_location (obj.name, obj.city, obj.address)
		self.create_dialog_event_date (obj.name, obj.date)
		self.create_dialog_event_type (obj.name, obj.eventType)
		self.create_dialog_event_time (obj.name, obj.time)
		self.create_dialog_event_city (obj.name, obj.city)
		self.create_dialog_event_description (obj.name, obj.city, obj.address, obj.date, obj.time, obj.eventType, obj.description)

	def create_dialog_event_location(self, name,city,address):
		ansLocationType = self.dialogResp['location'].get('res') + name + ' is '+ city + ' , ' + address

		for key in self.dialogsQues['location']:
			quesLocationType = self.dialogsQues['location'].get(key) + ' ' + name + ' ? '
			self.train_chatbot_with_question_answer( quesLocationType , ansLocationType )

	def create_dialog_event_date(self, name,strDate):
		ansDateType = self.dialogResp['date'].get('res') + name + ' is ' + strDate.strftime('%m/%d/%Y')

		for key in self.dialogsQues['date']:
			quesLocationType = self.dialogsQues['date'].get(key) + ' ' + name + ' ? '
			self.train_chatbot_with_question_answer( quesLocationType , ansDateType )

	def create_dialog_event_type(self, name,eventType):
		ansDateType = self.dialogResp['type'].get('res') + name + ' is ' + eventType

		for key in self.dialogsQues['type']:
			quesLocationType = self.dialogsQues['type'].get(key) + ' ' + name + ' ? '
			self.train_chatbot_with_question_answer( quesLocationType , ansDateType )

	def create_dialog_event_time(self, name,eventTime):
		ansEventTime = self.dialogResp['time'].get('res') + name + ' is ' + eventTime

		for key in self.dialogsQues['time']:
			quesLocationType = self.dialogsQues['time'].get(key) + ' ' + name + ' ? '
			self.train_chatbot_with_question_answer( quesLocationType , ansEventTime )

	def create_dialog_event_city(self, name,eventCity):
		ansEventCity = self.dialogResp['city'].get('res') + name + ' is ' + eventCity

		for key in self.dialogsQues['city']:
			quesLocationType = self.dialogsQues['city'].get(key) + ' ' + name + ' ? '
			self.train_chatbot_with_question_answer( quesLocationType , ansEventCity )

	def create_dialog_event_description(self, name, city, address, strDate, eventTime, eventType, description):
		ansEventDescription = 'Event Name : ' + name + '\n' +  'Location: ' + city + ' , ' + address + '\n' + 'Date: ' + strDate.strftime('%m/%d/%Y') + '\n' + 'Time: ' + eventTime + '\n' + 'Event Type: ' + eventType + '\n' + 'Description: ' + description
		
		for key in self.dialogsQues['description']:
			quesLocationType = self.dialogsQues['description'].get(key) + ' ' + name + ' ? '
			self.train_chatbot_with_question_answer( quesLocationType , ansEventDescription )

	def edit_dialog_event_location(self, oldObj, obj):
		textOldResponse = self.dialogResp['location'].get('res') + oldObj.name + ' is '+ oldObj.city + ' , ' + oldObj.address
		self.remove_old_response (textOldResponse)
		
		self.create_dialog_event_location (obj.name, obj.city, obj.address)

	def edit_dialog_event_date(self, oldObj, obj):
		textOldResponse = self.dialogResp['date'].get('res') + oldObj.name + ' is ' + oldObj.date.strftime('%m/%d/%Y')
		self.remove_old_response (textOldResponse)

		self.create_dialog_event_date(obj.name, obj.date)

	def edit_dialog_event_type(self, oldObj, obj):
		textOldResponse = self.dialogResp['type'].get('res') + oldObj.name + ' is ' + oldObj.eventType
		self.remove_old_response (textOldResponse)
			
		self.create_dialog_event_type (obj.name, obj.eventType)

	def edit_dialog_event_time(self, oldObj, obj):
		textOldResponse = self.dialogResp['time'].get('res') + oldObj.name + ' is ' + self.convertTimeToStr (oldObj.time)
		self.remove_old_response (textOldResponse)
			
		self.create_dialog_event_time (obj.name, obj.time)

	def edit_dialog_event_city(self, oldObj, obj):
		textOldResponse = self.dialogResp['city'].get('res') + oldObj.name + ' is ' + oldObj.city
		self.remove_old_response (textOldResponse)
			
		self.create_dialog_event_city (obj.name, obj.city)

	def edit_dialog_event_description(self, oldObj, obj):
		textOldResponse = 'Event Name : ' + oldObj.name + '\n' +  'Location: ' + oldObj.city + ' , ' + oldObj.address + '\n' + 'Date: ' + oldObj.date.strftime('%m/%d/%Y') + '\n' + 'Time: ' + self.convertTimeToStr(oldObj.time) + '\n' + 'Event Type: ' + oldObj.eventType + '\n' + 'Description: ' + oldObj.description
		self.remove_old_response (textOldResponse)
			
		self.create_dialog_event_description (obj.name, obj.city, obj.address, obj.date, obj.time, obj.eventType, obj.description)
		
	def train_chatbot_with_question_answer(self, question, answer):
		self.chatbot.read_only = False
		self.trainer.train([question,answer])
		self.chatbot.read_only = True

	def remove_old_response(self, strStatement):
		oldResponse = Statement (text = strStatement)
		self.chatbot.storage.remove(oldResponse)

	def convertTimeToStr(self, timeObj):
		minutes= str(timeObj.minute).zfill(2)
		formattedTime = str(timeObj.hour)+":"+ str(minutes)+ " "
		return formattedTime



