# This is needed to import this module
import sys
sys.path.insert(0, '..')

import tgflow as tgf
from tgflow import TgFlow as tgf
from tgflow import handles as h
from enum import Enum
key='539066078:AAHCUsr8ZoP9JtP5KqOMuL7f_UoFyyH6wik'


class States(Enum):
    START=1
    INFO=2
    FAV=3
    THANKS=4

UI = {
    States.START:
    {'t':'Hello, User!\n Here\'s what you can do:',
     'b': [
         {'show my info':tgf.action(States.INFO)},
         {'set my favourite':h.action(States.FAV)}
     ]},
    States.FAV:{
        't':'Please send me name of your favourite thing',
        'b':[{'my favourite is star':(lambda input,data: (States.THANKS,{'fav':'star'}))}],
        'react':h.action(
            lambda i: (States.THANKS,{'fav':i.text}),
            react_to = 'text'),
    },
    States.INFO:{
        't':h.st('Your fav is %s','fav'),
        'b': [
            {'back to start':tgf.action(States.START)},
            {'overwrite favourite':h.action(States.FAV)}
        ]
    },
    States.THANKS:{
        't':h.st('Thanks! I will remember your %s','fav'),
         'b': [
             {'show info':h.action(States.INFO,update_msg=True)},
             {'set another favourite':h.action(States.FAV,update_msg=True)}
         ],
        'clear_trig':'text'},
    }

tgf.configure(token=key,
                 state=States.START,
                 data={"foo":'bar'})
tgf.start(UI)

"""
from tgflow import TgFlow
from enum import Enum
key='539066078:AAHCUsr8ZoP9JtP5KqOMuL7f_UoFyyH6wik'

class States(Enum):
    START=1

TgFlow.configure(token=key,
                 state=States.START,
                 data={"foo":'bar'})
TgFlow.start({States.START:{'t':'hello'}})
"""
