import time
import requests
from ..longpoll import Longpoll

class Message():
    def __init__(s,obj):
        s.chat=Chat(obj['chatId'])
        s.text=obj['body']
        s.from_user = User(obj['author'])
class User:
    def __init__(s,id_):
        s.id = id_
class Chat():
    def __init__(s,i):
        s.id = i
class Callback():
    def __init__(self,msg,data):
        self.message=msg
        self.data = data


START_KB_IDX = 1

class WhatsAppBot:
    def __init__(self, token, endpoint):
        self.token = token
        self.ep = endpoint
        self.timestamp = time.time()
        self.keyboard = []
        def params_next(x,u):
            x.update({
                'lastMessageNumber':x.get('lastMessageNumber',0)
            })
            time.sleep(0.9)

        self.poller = Longpoll(
            self.check_updates,
            params_modifier=params_next,
        )
    def filter_updates(self, messages):
        return filter( lambda x:
                      x['time']>self.timestamp and not x['fromMe'],
                      messages)

    def check_updates(self,x):
        last = x.get('lastMessageNumber')
        msg = x.get('messages',[])
        if len(msg)>0:
            messages = list(self.filter_updates(msg))
            if len(messages)>0:
                return True

    def start_polling(self,**args):
        addr = self.ep +'/messages'
        params = {
            'token':self.token,
            'last':True
        }
        for event in self.poller.event_emmitter(addr,params):
            messages = []
            call = None
            recent = event.get('messages')
            for upd in self.filter_updates(recent):
                print('update',upd)
                msg = Message(upd)
                text = msg.text
                try:
                    label = int(text)
                    if label < 30:
                        call_id=label
                        call = self.keyboard[int(call_id)-START_KB_IDX]
                        call = Callback(msg,call)
                        self.callback_handler(call)
                except ValueError as e:
                    self.message_handler([msg])
            self.timestamp = time.time()

    def send_message(self,chat_id,text,**args):
        mk = args.get('reply_markup')
        butnames = []
        if mk:
            kb,i = "",START_KB_IDX
            for b in mk:
                butnames.append("%i: %s"%(i,b[0]))
                self._update_kb(b)
                i+=1
        params = {
                'phone':chat_id.split('@')[0],
                'body':text + '\n-------\n'+ '\n'.join(butnames),
            }

        r = self.make_request(
            'sendMessage',
            params
        )
        return r

    def _update_kb(s,button):
        s.keyboard.append(button[1])

    def set_message_handler(self,clb):
        self.message_handler =  clb
    def set_callback_handler(self,clb):
        self.callback_handler = clb

    def make_request(self,method_name,method_params):
        ep = self.ep
        ep += method_name
        data= method_params
        print(ep,data)
        r = requests.post(ep,params={'token':self.token},data=data)
        # TODO: add error handling
        js = r.json()
        print(r)
        print(r.text)
        return js.get('response')

        
