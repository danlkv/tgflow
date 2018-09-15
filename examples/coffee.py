
from tgflow import TgFlow as tgf
from tgflow import handles as h
from tgflow.coffee_ui import CoffeeUI
from enum import Enum
key='539066078:AAHCUsr8ZoP9JtP5KqOMuL7f_UoFyyH6wik'


class States(Enum):
    START=1
    INFO=2
    FAV=3
    THANKS=4

cof = """
START:
    t:'hello'
    b:[
        'show info':a 'INFO'
    ]
INFO:
    t: 'info'
    b:[
        start: a 'START'
    ,
        'set fav': a 'FAV'
    ]
FAV:
    t: 'send me fav'
    react: a 'set_fav'
    b:[
        start: a 'START',
        info: a 'INFO'
    ]
THANKS:
    t: ps 'fav'
    b: [ start: a 'START' ]
"""

tgf.configure(token=key,
                 state=States.START,
                 data={"foo":'bar'})

cofui = CoffeeUI( cof, States)
cofui.add_action('set_fav',
                 lambda i: (States.THANKS,{'fav':i.text}),
                 react_to = 'text')
cofui.add_subst('fav',
                 lambda i,**d: "Thank you for %s "%d['fav']
               )
print('alkdfj',cofui.actions)
UI = cofui.get_ui()
print (UI)
tgf.start(UI)

"""

UI = {
    States.START:
    {'t':'hello',
     'b': [
         {'show info':h.action(States.INFO)},
          {'set my favourite':h.action(States.FAV)}
     ]},
    States.FAV:{
        't':'Please send me name of your favourite thing',
        'react_to':h.action(
            lambda i: (States.THANKS,{'fav':i.text})),
    },
    States.INFO:{
        't':h.st('Your fav is %s','fav'),
        'react':h.action(
            lambda i: (States.THANKS,{'fav':i.text}),
            react_to = 'text'),
    },
    States.THANKS:{
        't':'Thanks! I will remember it',
         'b': [
             {'show info':h.action(States.INFO)},
          {'set another favourite':h.action(States.FAV)}
         ]},
    }
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
