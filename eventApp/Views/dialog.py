class Dialogs:
    dialogQuesData = {
        'location' : {
            'ques1' : 'What is location of',
            'ques2' : 'Where is located',
            'ques3' : 'Where is happening',
            'ques4' : 'What is address of ',
            'ques5' : 'location of '
        },
        'date' : {
            'ques1' : 'what is date of',
            'ques2' : 'When is happening',
            'ques3' : 'date of'
        },
        'description' : {
            'ques1' : 'What are details of',
            'ques2' : 'Can you please tell me details of',
            'ques3' : 'Describe',
            'ques4' : 'Provide details',
            'ques5' : 'description of',
            'ques6' : 'details of'
        },
        'type' : {
            'ques1' : 'What type of it is',
            'ques2' : 'category of',
            'ques3' : 'type of'
        },
        'time' : {
            'ques1' : 'What is time of',
            'ques2' : 'At what time is',
            'ques3' : 'time of'
        },
        'city' : {
            'ques1' : 'What is city of',
            'ques2' : 'City of',
            'ques3' : 'in which city will happen'
        }
    }

    dialogResponseData = {
        'location' : {
            'res' : 'Location of the '
        },
        'date' : {
            'res' : 'Date (in format \'MM/DD/YY\') of the '
        },
        'type' : {
            'res' : 'Type of the '
        },
        'time' : {
            'res' : 'Time (in 24 hr format) of the '
        },
        'city' : {
            'res' : 'City of the '
        }
    }
    dialogStatementGeneral = {
        'greeting_1' : {
            'format1' : 'Hi',
            'format2' : 'Hello', 
            'format3' : 'Hey',
            'format4' : 'Hi there',
            'format5' : 'Hey there',
        },
        'greeting_2' : {
            'format1' : 'Thank you',
            'format2' : 'Thanks', 
            'format3' : 'Thanks a bunch',
            'format4' : 'Thanks a ton',
            'format5' : 'Thank you so much',
            'format6' : 'Thanks a lot'
        },
        'greeting_3' : {
            'format1' : 'Nice talking to you',
            'format2' : 'Nice to meet you',
            'format3' : 'Nice meeting you',
            'format4' : 'Nice to talk to you'
        },
        'dialogForHelp' : 
        {
            'format1' : 'Help please',
            'format2' : 'Help needed',
            'format3' : 'Help',
            'format4' : 'I need help',
            'format5' : 'Can you help'
        }
    }

    dialogResponseGeneral = {
        'greetingRes_1' : 'Hi, how can I help you today ? ',
        'greetingRes_2' : 'You are most welcome.',
        'greetingRes_3' : 'Same here.',
        'respForHelp'   : 'This is event specific chatbot. Try formulating questions specific to event such as: location of eventName, details of eventName, date of eventName etc.'
    }

    def get_dialog_data(self, typeRequestedData):
        if (typeRequestedData == 'EventSpecificDialogQues'):
            return self.dialogQuesData
        if (typeRequestedData == 'EventSpecificDialogAns'):
            return self.dialogResponseData
        if (typeRequestedData == 'GeneralDialogQues'):
            return self.dialogStatementGeneral
        if (typeRequestedData == 'GeneralDialogAns'):
            return self.dialogResponseGeneral
