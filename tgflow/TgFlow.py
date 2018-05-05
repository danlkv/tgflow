import telebot
import hashlib
from . import handles
from . import render
import pickle,time

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

def configure(token=None, state=None, data={}):
    global def_state,def_data
    global bot,key
    if not token:
        raise Exception("tgflow needs your bot token")
    if not state:
        raise Exception("tgflow needs a default state for new users")
    key =token
    def_state=state
    def_data =data

    # create bot and assign handlers
    bot = telebot.TeleBot(key)
    bot.set_update_listener(message_handler)
    set_callback_handler()

def start(ui):
    global bot,UI
    UI = ui
    print("tgflow: listening")
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print("tgflow:polling error",e)
            time.sleep(10)

def get_file_link(file_id):
    finfo = bot.get_file(file_id)
    l='https://api.telegram.org/file/bot%s/%s'%(
        key,finfo.file_path)
    return l

def message_handler(messages):
    global States,UI
    for msg in messages:
        s = States.get(msg.chat.id,def_state)
        print('tgflow: got message. State:'+str(s))
        # for security reasons need to hash. user can call every action in this state
        # key format: kb_+ButtonName
        a = Actions.get('kb_'+str(msg.text))
        if not a:
            for r,a_ in Reaction_triggers[msg.chat.id]:
                if msg.__dict__.get(r):
                    a = a_
        d = Data.get(msg.chat.id,def_data)

        messages = flow(a,s,d,msg,msg.chat.id)
        send(messages,msg.chat.id)



def set_callback_handler():
    @bot.callback_query_handler(func=lambda call: True)
    def callback_handler(call):
        s = States.get(call.message.chat.id,def_state)
        a = Actions.get(call.data)
        d = Data.get(call.message.chat.id,def_data)
        messages = flow(a,s,d,call,call.message.chat.id)
        if a:
            if not a.update:
                send(messages,call.message.chat.id)
            else:
                update(messages, call.message)
        else:
            print("tgflow: Warning: no action found but should")
            send(messages,call.message.chat.id)

def gen_state_msg(i,ns,nd,_id,state_upd=True):
    pre_a = UI.get(ns).get('prepare')
    if pre_a:
       # call user-defined data perparations. 
       nd = pre_a(i,ns,**nd)

    args = {'s':ns,'d':nd}
    ui = render.prep(UI.get(ns),args)

    # saving data and state
    Data[_id] = nd
    if state_upd: States[_id] = ns
    save_sd(States,Data)
    # registering callback triggers on buttons
    save_iactions(ui.get('b'))
    save_kactions(ns,ui.get('kb'),ns)
    print("tgflow: actions registration ended",Actions)

    # registering reaction triggers
    rc = ui.get('react')
    if rc:
        print("tgflow: reaction tgigger for %i registrated %s"%(i,str(rc)))
        Reaction_triggers[_id].append((rc.react_to,rc))
    # clearing reaction triggers if needed
    rc = ui.get('clear_trig')
    if rc:
        print("tgflow: reaction trigger clear",rc)
        for r,a_ in Reaction_triggers[_id]:
            #TODO: handle arrays of triggers
            if rc == r:
                Reaction_triggers[_id].remove((r,a_))

    # rendering message and buttons
    messages = render.render(ui)
    return messages

def send_state(ns,tg_id):
    d = Data.get(tg_id,def_data)
    msg = gen_state_msg(None,ns,d,tg_id)
    send(msg,tg_id)

def flow(a,s,d,i,_id):
    if a:
        ns,nd = a.call(i,s,**d)
        print('tgflow: called action:'+str(a))
    else:
        print('tgflow: no action found for message. State unchanged')
        ns,nd = s,d

    print ('tgflow: new state',ns)
    return gen_state_msg(i,ns,nd,_id)

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
# TODO: remove s argument
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

def send(message,id):
    print("tgflow: sending message")
    for text,markup in message:
        bot.send_message(
            text=text,
            chat_id=id,
            parse_mode='Markdown',
            reply_markup =markup)

def update(messages,msg):
    print("tgflow: updating message")
    for text,markup in messages:
        if text:
            bot.edit_message_text(
                text=text,
                chat_id=msg.chat.id,
                parse_mode='Markdown',
                message_id=msg.message_id
            )
        if markup:
            bot.edit_message_reply_markup(
                chat_id=msg.chat.id,
                message_id=msg.message_id,
                reply_markup=markup)
