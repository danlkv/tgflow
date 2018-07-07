class Message():
    def __init__(self,text=None):
        self.text=text
        self.chat = Chat()

class Chat():
    def __init__(self,id=None):
        self.id=id

class Callback():
    def __init__(self):
        self.message= Message()

class VkKeyboard():
    def __init__(self):
        pass
