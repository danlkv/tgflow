import json
class Message():
    def __init__(self,text=None):
        self.text=text
        self.chat = Chat()
        self.object = {}
        self.attachments = []

    def load_object(self,obj):
        self.object = obj
        self.attachments = obj.get('attachments',[])

class Chat():
    def __init__(self,id=None):
        self.id=id

class Callback():
    def __init__(self):
        self.message= Message()

class VkKeyboard():
    def __init__(self,row_width=1,buttons=None):
        self.row_width = row_width
        self.buttons = buttons
    def get_json( self):
        d = {
            'one_time':False,
            'buttons':[[
                but.get_dict() for but in self.buttons
            ]],
        }
        return json.dumps(d)

class VkKeyboardButton():
    def __init__(self,text=None,
                 callback_data=None,
                 color=None):

        self.text = text
        self.color = color
        self.callback_data =  callback_data


    def get_dict(self):
        d = {
            'action':{
                'type':"text",
                'payload':json.dumps(self.callback_data),
                'label':self.text
            },
            'color':self.color or 'default'
        }
        return d
    def get_json(self):
        d = self.get_dict()
        return json.dumps(d)

class VkCallback():
    def __init__(self,data=None,
                 message=Message()):
        self.data = data
        self.message = message

