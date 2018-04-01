import telebot

from . import TgFlow as Tgflow
from . import handles as h
from enum import Enum

key = "469681737:AAE1JOJ7Ae2tVglDswCXXbrYNR7oyECtiQQ"

data={'foo':'FO','bar':'BA','cnt':0}
class States(Enum):
    HI=1
    Hl=2
    Hh=3
    Hq=4
    bu=0

def func(i,s,**d):
    print(' id %i Pressed!'%i.message.chat.id)
    print('data',d)
    d['cnt'] += 1
    return States.bu,d

UI={
    States.HI:{
        't':h.subst("hello %s",'foo'),
        'b':[
            {'press':h.action(func)}
        ],
        'kb':[
            {'contact':States.bu,
             'kwargs':{'share_contact':True}}
        ],
        'f':['he','llo',h.post('world')]
    },
    States.bu:{
        't':'Thanks for pressing',
        'b':[{'go on':h.action(States.Hl)}]
    },
    States.Hl:{
        't':'look!',
        'b':[{'forward':h.action(States.Hq)},
             {'back':h.action(States.bu)}
            ]
    },
    States.Hh:{
        't':'Not bad',
        'b':[{'forward':h.action(States.Hq)}]
    },
    States.Hq:{
        't':'Not bad',
        'b':[{'forward':States.Hq},
             h.post(lambda s,**d: 
                    dict((str(States(n)),h.action(States(n))) 
                         for n in range(4)))
                   ]
    },
}
Tgflow.__init__(key)
Tgflow.set_default_state_data(States.HI,data)
Tgflow.start(UI)
