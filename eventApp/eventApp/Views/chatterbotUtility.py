from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
import json
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from django.views.decorators.csrf import csrf_exempt

chatbot = ChatBot(
    'Mehak',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='mysql://root:mehak1996@localhost/EventApp'

)
chatbot.train("/Users/mehakluthra/Documents/EventManagementChatterbot/eventApp/custom_corpus/mehak.yml")

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


