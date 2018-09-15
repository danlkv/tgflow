import json,pprint,copy,telebot
from . import handles as h
from . import TgFlow as tgf
pp = pprint.PrettyPrinter(indent=5)

def rdict(d,a):
    # leave untouched original ui template and it's parts
    d = copy.copy(d)
    if isinstance(d,h.post):
        # apply post transform, passing out_data
        x = d.apply(**a)
        # process post in output of this post
        if isinstance(x,dict):
            d = rdict(x,a)
        else:
            d=x
    if callable(d):
        # paste action instead of callable
        d = h.action(d)
        print("acion on callable")
    elif isinstance(d,list):
        d = [rdict(x,a) for x in d ]
    elif isinstance(d,dict):
        # recursively process nested dicts. 
        # throws recursive depth error if self referenced
        for k,v in d.items():
            d[k] = rdict(v,a)
    return d

def flatten(lis):
    new_lis = []
    for item in lis:
        if isinstance(item,list):
            new_lis.extend(flatten(item))
        else:
            new_lis.append(item)
    return new_lis

def prep(ui,args):
    print("tgflow: preprocessing ui for state",args.get('s'))
    ## SUBSTITUTION
    # support for full names
    ui['t']=ui.get('t') or ui.get('text')
    ui['b']=ui.get('b') or ui.get('buttons')
    ui['kb']=ui.get('kb') or ui.get('keyboard')

    ui = rdict(ui,args)
    ## VALIDALIZATIOIN
    b = ui.get('b')
    if b:
        if isinstance(b,list):
            ui['b']=flatten(b)
    print('done. result:',ui)
    return ui

def render(ui):
    # get ui contents
    t = ui.get('t')
    butns =ui.get('b')
    kbb =ui.get('kb')
    if butns:
        butns = [[
        tgf.api.KeyboardButton(
            text=bt,
            # TODO: s should be of type handle.action !
            callback_data=act.get_register_key()
        )
                    for bt,act in butrow.items()]
                        for butrow in butns]
        imarkup = tgf.api.KeyboardMarkup(
            row_width=1,
            buttons=sum(butns,[])
        )
    else:
        imarkup = None
    if kbb:
        if kbb=='Remove':
            kmarkup = telebot.types.ReplyKeyboardRemove()
        else:
            kacc=[]
            for but in kbb:
                k = list(but.keys())
                kwargs = but.get('kwargs')
                if kwargs:
                    k.remove('kwargs')
                    kacc.append(
                        telebot.types.KeyboardButton(text=k[0],**kwargs)
                    )
                else:
                    kacc.append(
                        telebot.types.KeyboardButton(text=k[0])
                    )
            kmarkup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            kmarkup.add(*kacc)
    else:
        kmarkup = None
    messages = [(t,imarkup or kmarkup)]

    if (kbb and butns):
        messages.append((ui.get('kb_txt'),kmarkup))
    messages.reverse()
    return messages

