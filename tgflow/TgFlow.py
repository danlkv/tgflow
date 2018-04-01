import telebot
import hashlib
from . import handles
from . import render
import pickle

import pprint
pp = pprint.PrettyPrinter(indent=4)

action = handles.action

bot,key = None,None
def_state = None
def_data= None
States = {}
UI = {}
Data = {}
Actions = {}
Keyboards = {}
Reaction_triggers = []


def read_sd(sf,df):
    with open(sf,'rb') as f:
        try:
            s= pickle.load(f)
        except:
            s={}
    with open(df,'rb') as f:
        try:
            d = pickle.load(f)
        except:
            d={}
    return s,d

def save_sd(states,data):
    with open('states.p','wb+') as f:
        pickle.dump(states,f)
    with open('data.p','wb+') as f:
        pickle.dump(data,f)

States,Data = read_sd('states.p','data.p')

def __init__(apikey):
    global bot,key
    print ('init')
    key = apikey
    bot = telebot.TeleBot(key)
    bot.set_update_listener(message_handler)
    blah()

def set_default_state_data(ds,dd):
    global def_state,def_data
    def_state=ds
    def_data = dd
def start(ui):
    global bot,UI
    UI = ui
    bot.polling(none_stop=True)

def get_file_link(file_id):
    finfo = bot.get_file(file_id)
    l='https://api.telegram.org/file/bot%s/%s'%(
        key,finfo.file_path)
    return l

def message_handler(messages):
    global States,UI
    for msg in messages:
        s = States.get(msg.chat.id,def_state)
        print('gor message state'+str(s))
        # for security reasons need to hash. user can call every action in this state
        # key format: kb_+ButtonName
        a = Actions.get('kb_'+str(msg.text))
        print (Reaction_triggers)
        if not a:
            for r,a_ in Reaction_triggers:
                if msg.__dict__.get(r):
                    a = a_
        d = Data.get(msg.chat.id,def_data)

        messages = flow(a,s,d,msg,msg.chat.id)
        send(messages,msg.chat.id)
def blah():
    @bot.callback_query_handler(func=lambda call: True)
    def callback_handler(call):
        s = States.get(call.message.chat.id,def_state)
        a = Actions.get(call.data)
        d = Data.get(call.message.chat.id,def_data)
        messages = flow(a,s,d,call,call.message.chat.id)
        send(messages,call.message.chat.id)

def flow(a,s,d,i,_id):
    print ("Starting to flow< data:")
    if a:
        ns,nd = a.call(i,s,**d)
        print(' called action:'+str(a))
    else:
        ns,nd = s,d

    print ('New state',ns)

    pre_a = UI.get(ns).get('prepare') # call generic perparation action
    if pre_a:
       nd = pre_a(i,ns,**nd)
       print('data prep ended')

    args = {'s':ns,'d':nd}
    ui = render.prep(UI.get(ns),args)

    Data[_id] = nd
    States[_id] = ns
    save_sd(States,Data)
    save_iactions(ui.get('b'))
    save_kactions(ns,ui.get('kb'),ns)
    print("registration ended",Actions)
    rc = ui.get('react')
    if rc:
        Reaction_triggers.append((rc.react_to,rc))
    messages = render.render(ui)
    return messages

def get_state(id,s):
    pass

def save_iactions(ui):
    if isinstance(ui,action):
        Actions[str(ui)]=ui
    if isinstance(ui,dict):
        for k,v in ui.items():
            save_iactions(v)
    elif isinstance(ui,list):
        d = [save_iactions(x) for x in ui ]
def save_kactions(k,ui,s):
    if isinstance(ui,action):
        # key format: State+ButtonName
        if ui.react_to:
            print('react to'+ui.react_to)
            Reaction_triggers.append((ui.react_to,ui))
        else:
            Actions['kb_'+str(k)]=ui
    if isinstance(ui,dict):
        for k,v in ui.items():
            save_kactions(k,v,s)
    elif isinstance(ui,list):
        ui = [save_kactions(k,x,s) for x in ui ]

def send(messages,id):
    for text,markup in messages:
        bot.send_message(
            text=text,
            chat_id=id,
            parse_mode='Markdown',
            reply_markup =markup)

