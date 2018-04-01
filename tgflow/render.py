import json,pprint,copy,telebot


pp = pprint.PrettyPrinter(indent=5)
from . import handles as h
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

def prep(UI,args):
    print("tgflow: preprocessing ui")
    ## SUBSTITUTION
    ui = rdict(UI,args)
    ## VALIDALIZATIOIN
    b = ui.get('b')
    if b:
        if isinstance(b,list):
            ui['b']=flatten(b)
    print('done. result:',ui)
    return ui

def render(ui):
    t = ui.get('t')
    butns =ui.get('b')
    kbb =ui.get('kb')
    if butns:
        butns = [[
        telebot.types.InlineKeyboardButton(text=bt,
                                           callback_data=str(s))
                    for bt,s in butrow.items()]
                        for butrow in butns]
        imarkup = telebot.types.InlineKeyboardMarkup(row_width=1)
        imarkup.add(*sum(butns,[]))
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

