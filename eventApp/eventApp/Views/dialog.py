class Dialogs:
    dialogData = {
        'location' : {
            'ques1' : 'What is location of event',
            'ques2' : 'Where is event located',
            'ques3' : 'Where is event happening',
            'ques4' : 'What is address of event'
        },
        'date' : {
            'ques1' : 'what is date of event',
            'ques2' : 'When is event happening',
        },
        'description' : {
            'ques1' : 'What are details of event',
            'ques2' : 'Can you please tell me details of event',
            'ques3' : 'Describe event',
            'ques4' : 'Provide event details',
        },
        'type' : {
            'ques1' : 'What type of event it is',
            'ques2' : 'category of event',
        },
        'time' : {
            'ques1' : 'What is time of event',
            'ques2' : 'At what time is event',
        },
        'city' : {
            'ques1' : 'What is city of event',
            'ques2' : 'City of event',
            'ques3' : 'In which city event will happen'
        } 
    }
    def get_dialog_data(self):
        return self.dialogData