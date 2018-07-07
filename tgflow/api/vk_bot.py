import requests
from .Types import *
from .longpoll import Longpoll

class VKBot:
    ep = 'https://api.vk.com/method'
    version = '5.80'

    def __init__(self,token):
        self.token = token
        group='168613369'
        self.get_longpoll_server(group)
        #self.check_longpoll()
        self.poller = Longpoll(
            lambda x: len(x.get('updates',[]))>0,
            params_modifier=
            lambda x,u: x.update({'ts':x.get('ts',0)+1})\
            if u else x
        )

    def start_polling(self,**args):
        addr = self.longpoll_server
        params = {
            'act':'a_check',
            'key':self.longpoll_key,
            'ts':self.ts,
            'wait':25
        }
        for event in self.poller.event_emmitter(addr,params):
            print("HHAHHL")
            print(event)
            messages = []
            for upd in event.get('updates',[]):
                if upd.get('type')=='message_new':
                    msg = upd.get('object')
                    text = msg.get('text')
                    chat_id = msg.get('peer_id')
                    msg = Message(text)
                    msg.chat = Chat(chat_id)
                    messages.append(msg)
                else:
                    pass
            self.message_handler(messages)

    def send_message(self,chat_id,text,**args):
        r = self.make_request(
            'messages.send',
            {
                'peer_id':chat_id,
                'message':text,
            }
        )
        return r


    def set_message_handler(self,clb):
        self.message_handler =  clb
    def set_callback_handler(self,clb):
        self.callback_handler = clb

    def get_longpoll_server(self,group):
        print("getting longpoll server addr")
        s = self.make_request('groups.getLongPollServer',
                          {
                            'group_id':group
                          }
                         )
        server,key = s.get('server'),s.get('key')
        # Assign the props to self
        if (server and key):
            self.longpoll_server, self.longpoll_key = server,key
            self.ts = s.get('ts')
        else:
            raise Exception("Vk returned no Longpoll servers")

    def check_longpoll(self):
        r = requests.get(
            self.longpoll_server,
            {
                'act':'a_check',
                'key':self.longpoll_key,
                'ts':1,
                'wait':25
            }
        )
        js = r.json()
        print('Checked longpoll',js)
        return js.get('response')

    def make_request(self,method_name,method_params):
        ep = 'https://api.vk.com/method/'
        ep += method_name
        params = {
            'access_token':self.token,
            'v':self.version
        }
        params.update(method_params)
        r = requests.get(ep,params=params)
        # TODO: add error handling
        js = r.json()
        print(js)
        return js.get('response')

