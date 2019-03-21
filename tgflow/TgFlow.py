#import telebot
import hashlib, traceback
from enum import Enum
from . import handles
from . import render
import pickle,time
from .api.tg import telegramAPI

import pprint
pp = pprint.PrettyPrinter(indent=4)

action = handles.action

VERBOSE=False
def _print(*args):
    if VERBOSE:
        print("tgflow:",*args)

api,key = None,None
def_state = None
def_data= None
States = {}
UI = {}
Data = {}
Actions = {}
Keyboards = {}
Reaction_triggers = {}


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
    try:
        with open('states.p','wb+') as f:
            pickle.dump(states,f)
        with open('data.p','wb+') as f:
            pickle.dump(data,f)
    except Exception as e:
        print('Non-picklable',str(e))

try:
    States,Data = read_sd('states.p','data.p')
except FileNotFoundError:
    print("tgflow: creating data.p and states.p files")

def configure(token=None, state=None,
              apiModel=telegramAPI, data={},
              group_id=None,
              verbose=False,
              **kwargs

             ):
    global def_state,def_data
    global api,key
    if verbose:
        global VERBOSE
        VERBOSE=True
    if not token:
        raise Exception("tgflow needs your bot token")
    if not state:
        raise Exception("tgflow needs a default state for new users")
    key =token
    def_state=state
    def_data =data

    # create bot and assign handlers
    # Group Id is not used in telegram
    api = apiModel(key,group_id=group_id, **kwargs)

    api.set_message_handler(message_handler)
    api.set_callback_handler(callback_handler)


def start(ui):
    global api,UI
    UI = ui
    _print("tgflow: listening")
    try:
        api.start(none_stop=True)
    except Exception as e:
        print("tgflow:polling error",e)
        traceback.print_exc()

def get_file_link(file_id):
    # TODO: implement this in api
    finfo = bot.get_file(file_id)
    l='https://api.telegram.org/file/bot%s/%s'%(
        key,finfo.file_path)
    return l

def message_handler(messages):
    global States,UI
    for msg in messages:
        s = States.get(msg.chat.id,def_state)
        _print('tgflow: got message. State:'+str(s))
        # for security reasons need to hash. user can call every action in this state
        # key format: kb_+ButtonName
        a = Actions.get('kb_'+str(msg.text))
        if not a:
            if Reaction_triggers.get(msg.chat.id):
                for r,a_ in Reaction_triggers[msg.chat.id]:
                    if msg.__dict__.get(r):
                        a = a_
                    if r=='all':
                        a = a_

        d = Data.get(msg.chat.id,def_data)

# following restriction is dictaded by telegram api
        messages = flow(a,s,d,msg,msg.chat.id)
        if messages:
            send(messages,msg.chat.id)
        else:
            _print("Staying silent...")

def callback_handler(call):
    s = States.get(call.message.chat.id,def_state)
    a = Actions.get(call.data)
    d = Data.get(call.message.chat.id,def_data)
    _print("tgflow: got callback. State:",s)
    messages = flow(a,s,d,call,call.message.chat.id)
    if a:
        if not a.update:
            send(messages,call.message.chat.id)
        else:
            update(messages, call.message)
    else:
        _print("tgflow: Warning: no action found but should")
        send(messages,call.message.chat.id)

def gen_state_msg(i,ns,nd,_id,state_upd=True):
    if not ns:
        _print('tgflow: None as new state, sending nothing')
        return []
    new_state_ui = UI.get(ns)
    pre_a = new_state_ui.get('prepare')

    if pre_a:
       # call user-defined data perparations. 
       _print("tgflow: found a prep function, calling...")
       nd.update(pre_a(i,ns,**nd))

    args = {'s':ns,'d':nd}
    ui = render.prep(new_state_ui,args)

    # saving data and state
    Data[_id] = nd
    if state_upd: States[_id] = ns
    save_sd(States,Data)
    # registering callback triggers on buttons
    save_iactions(ui.get('b'))
    save_kactions(ns,ui.get('kb'),ns,_id)
    _print("tgflow: actions registered:\n",Actions)

    # registering reaction triggers
    rc = ui.get('react') or ui.get('react_to')
    if rc:
        trigs = Reaction_triggers.get(_id)
        if trigs:
            Reaction_triggers[_id].append((rc.react_to,rc))
        else:
            Reaction_triggers.update({_id:[(rc.react_to,rc)]})
        _print("tgflow: reaction tgigger for %s registrated %s"%(str(_id),str(rc)))
    # clearing reaction triggers if needed
    rc = ui.get('clear_trig')
    if rc:
        _print("tgflow: reaction trigger clear",rc)
        if Reaction_triggers.get(_id):
            for r,a_ in Reaction_triggers[_id]:
                #TODO: handle arrays of triggers
                if rc == r:
                    Reaction_triggers[_id].remove((r,a_))
        else:
            _print("tgflow:WARN removing unset trigger",rc)

    # rendering message and buttons
    messages = render.render(ui)
    return messages

def send_state(ns,tg_id):
    d = Data.get(tg_id,def_data)
    msg = gen_state_msg(None,ns,d,tg_id)
    send(msg,tg_id)

def send_raw(text,uid):
    # this isn't recommended for users, as will not affect state
    send([(text,None)],uid)

def flow(a,s,d,i,_id):
    messages = []
    while True:
        if a:
            ns,nd = a.call(i,s,**d)
            d.update(nd)
            nd = d

            _print('tgflow: called action:'+str(a))
            if isinstance(s,Enum) and isinstance(ns,Enum):
                _print ('tgflow: states change %s --> %s'%(s.name,ns.name))
            else:
                _print ('tgflow: states change %s --> %s'%(s,ns))
        else:
            _print('tgflow: no action found for message. %s unchanged'%s)
            ns,nd = s,d

        # user can choose what to send if no action found
        # Just should return -1 instead of state
        if ns==-1:
            return message.append(None)

        # This allows to perform an action without waiting for user input
        messages.append(gen_state_msg(i,ns,nd,_id)[0])
        a = UI.get(ns).get('immediate_after')
        if not a:
            break
    return messages

def get_state(id,s):
    pass

def save_iactions(ui):
    if isinstance(ui,action):
        #TODO: assign actions to every user distinctly, as with butons
        key = ui.get_register_key()
        Actions[key]=ui
    if isinstance(ui,dict):
        for k,v in ui.items():
            save_iactions(v)
    elif isinstance(ui,list):
        d = [save_iactions(x) for x in ui ]
# TODO: remove s argument
def save_kactions(k,ui,s,_id):
    if isinstance(ui,action):
        # key format: State+ButtonName
        if ui.react_to:
            trigs = Reaction_triggers.get(_id)
            if trigs:
                Reaction_triggers[_id].append((ui.react_to,ui))
            else:
                Reaction_triggers.update({_id:[(ui.react_to,ui)]})
            _print("tgflow: reaction tgigger for %s registrated %s"%(str(_id),str(ui)))

        else:
            Actions['kb_'+str(k)]=ui
    if isinstance(ui,dict):
        for k,v in ui.items():
            save_kactions(k,v,s,_id)
    elif isinstance(ui,list):
        ui = [save_kactions(k,x,s,_id) for x in ui ]

def send(message,id):
    _print("tgflow: sending message to",id)
    for text,markup in message:
        api.send(id,text=text,markup=markup)

def update(messages,msg):
    for text,markup in messages:
        _print("tgflow: updating message")
        api.update(msg,text=text,markup=markup)
