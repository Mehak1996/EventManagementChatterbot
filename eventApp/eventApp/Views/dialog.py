class Dialogs:
    dialogData = {
        'location' : {
            'ques1' : 'What is the location of event',
            'ques2' : 'Where is the event located',
            'ques3' : 'Where is event happening',
            'ques4' : 'What is the address of event'
        },
        'date' : {
            'ques1' : 'what is the date of event',
            'ques2' : 'When is event happening',
        },
        'description' : {
            'ques1' : 'What are the details of the event',
            'ques2' : 'Can you please tell me details of event',
            'ques3' : 'Describe event',
            'ques4' : 'Please provide event details',
        },
        'type' : {
            'ques1' : 'What type of event it is',
            'ques2' : 'category of event',
        },
        'time' : {
            'ques1' : 'What is the time of the event',
            'ques2' : 'At what time is the event',
        },
        'city' : {
            'ques1' : 'What is the city of the event',
            'ques2' : 'City of the event',
            'ques3' : 'In which city event will happen'
        } 
    }
    def get_dialog_data(self):
        return self.dialogData