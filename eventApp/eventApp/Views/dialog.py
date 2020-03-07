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
    def get_dialog_data(self, typeRequestedData):
        if (typeRequestedData == 'ques'):
            return self.dialogQuesData
        else:
            return self.dialogResponseData