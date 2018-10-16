import requests
from .Types import *
from .longpoll import Longpoll

class VKBot:
    ep = 'https://api.vk.com/method'
    version = '5.80'

    def __init__(self,token,group,
            lp_ep='groups.getLongPollServer'):
        self.token = token
        self.group = group
        self.get_longpoll_ep = lp_ep

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
            messages = []
            call = None
            for upd in event.get('updates',[]):
                print(upd)
                if upd.get('type')=='message_new':
                    msg_object = upd.get('object')
                    text = msg_object.get('text')
                    data = msg_object.get('payload')
                    chat_id = msg_object.get('peer_id')

                    msg = Message(text)
                    msg.load_object( msg_object)
                    msg.chat = Chat(chat_id)
                    if data:
                        call = VkCallback(
                            # FUCK U VK
                            data = json.loads(data),
                            message = msg
                        )
                    messages.append(msg)
                else:
                    pass
            if call:
                self.callback_handler(call)
            else:
                self.message_handler(messages)

    def send_message(self,chat_id,text,**args):
        params = {
                'peer_id':chat_id,
                'message':text,
            }
        mk = args.get('reply_markup')
        if mk:
            print(mk.get_json())
            k =  mk.get_json()
            params.update({
               # 'keyboard':mk.get_json()
                'keyboard':k
            })

        r = self.make_request(
            'messages.send',
            params
        )
        return r


    def set_message_handler(self,clb):
        self.message_handler =  clb
    def set_callback_handler(self,clb):
        self.callback_handler = clb

    def get_longpoll_server(self,group):
        print("getting longpoll server addr")
        s = self.make_request(self.get_longpoll_ep,
                          {
                            'group_id':group
                          }
                         )
        server,key = s.get('server'),s.get('key')
        if server[:4]!='http':
            server='https://'+server
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
        print(ep,params)
        r = requests.get(ep,params=params)
        # TODO: add error handling
        js = r.json()
        print(r)
        print(r.text)
        return js.get('response')

