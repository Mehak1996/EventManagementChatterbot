from abc import ABCMeta, abstractstaticmethod

######################################################################################################################
#           Title        : Factory Method in Python
#           Author       : Unknown
#           Source Url   : https://sourcemaking.com/design_patterns/factory_method/python/1           
######################################################################################################################

class Message(metaclass=ABCMeta):  

    @abstractstaticmethod
    def get_messageText():
        pass

class SuccessMessage(Message):  

    def __init__(self):
        self._message = "Operation Succesfully done"

    def get_messageText(self):
        return self._message

class FailureMessage(Message):  

    def __init__(self):
         self._message = "Operation Failure: Error ocurred in your request"

    def get_messageText(self):
        return self._message

class FailureMessageInline(Message):  

    def __init__(self):
         self._message = ""

    def get_messageText(self):
        return self._message

class InfoMessage(Message): 

    def __init__(self):
         self._message = "You succesfully registered yourself for "

    def get_messageText(self):
        return self._message


class MessageFactory:  

    @staticmethod
    def get_message(message):
        try:
            # Create object of SuccessMessage class if message type is "Success"
            if message == "Success":
                return SuccessMessage()
            # Create object of FailureMessage class if message type is "Failure"
            if message == "Failure":
                return FailureMessage()
            # Create object of InfoMessage class if message type is "Info"
            if message == "Info":
                return InfoMessage()
            # Create object of FailureMessageInline class if message type is "InlineFailure"
            if message == "InlineFailure":
                return FailureMessageInline()
            # Raise Exception of Message Not Found
            raise AssertionError("Message Not Found")
        except AssertionError as _e:
            print(_e)
        return None
        

#if __name__ == "__main__":
#    messageFactory = MessageFactory().get_message("Failure")
#    print(messageFactory.get_messageText())