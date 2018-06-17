# This is needed to import module in this folder
import sys
sys.path.insert(0, '..')
import logging
logging.basicConfig(level=logging.DEBUG)


import tgflow as tgf
from tgflow import TgFlow as tgf
from tgflow import handles as h
from enum import Enum
key='539066078:AAHCUsr8ZoP9JtP5KqOMuL7f_UoFyyH6wik'


class States(Enum):
    START=1
    ADD_BUT=2
    MODIFY_BUT=3
    THANKS=4

def upd_kb(i,keyboard={},upd_id='rename me'):
    but_name=  i.text
    print('user changes name to ',but_name)
    keyboard.update(
        {
            but_name:h.action(gen_handler(but_name))
        }
    )
    del keyboard[upd_id]
    return States.THANKS, {'keyboard':keyboard, 'upd_id':but_name}

def gen_handler(but_id):
    def handler():
        return States.MODIFY_BUT,{'upd_id':but_id}
    return handler

def add_kb(i,keyboard={}):
    print("user creates new button")
    but_name=  'rename me'
    func = gen_handler(but_name)
    keyboard.update({but_name:h.action(func)})
    return States.THANKS, {'keyboard':keyboard,'upd_id':but_name}

UI = {
    States.START:
    {
        't':'Hello! click on a button to create or modify',
        'b': [
            {'create button':tgf.action(add_kb)},
            h.post(lambda s,**d: d.get('keyboard',{}))
        ]
    },
    States.MODIFY_BUT:{
        't':'Send me the name of button',
        'b':[
            {'cancel':tgf.action(States.START)}
        ],
        'react':h.action(
            upd_kb,
            react_to='text'),
    },
    States.THANKS:{
        't':h.st('Youve modified, new name is %s',
                 'upd_id'),
        'b': [
            {'back to start':tgf.action(States.START)},
        ],
        'clear_trig':'text'
    },
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
