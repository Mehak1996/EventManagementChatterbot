from abc import ABCMeta, abstractstaticmethod


class Message(metaclass=ABCMeta):  

    @abstractstaticmethod
    def get_messageText():
        pass

class SuccessMessage(Message):  

    def __init__(self):
        self._message = "Succesfully done"

    def get_messageText(self):
        return {"message":self._message}

class FailureMessage(Message):  

    def __init__(self):
         self._message = "Error ocurred in your request"

    def get_messageText(self):
        return {"message":self._message}


class InfoMessage(Message): 

    def __init__(self):
         self._message = "Info message"

    def get_messageText(self):
        return {"message":self._message}


class MessageFactory:  

    @staticmethod
    def get_message(message):
        try:
            if message == "Success":
                return SuccessMessage()
            if message == "Failure":
                return FailureMessage()
            if message == "Info":
                return InfoMessage()
            raise AssertionError("Message Not Found")
        except AssertionError as _e:
            print(_e)
        return None
        

#if __name__ == "__main__":
#    messageFactory = MessageFactory().get_message("Failure")
#    print(messageFactory.get_messageText())