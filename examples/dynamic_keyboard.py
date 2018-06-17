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

# Lets' assume following usecase: user has some entities that 
# he can modify, and thus button for every thing needs to
# display user-dependent mutatable data

# Here's how you dynamically assign inline keyboard:

def add_kb(i,keyboard={}):
    print("user creates new button")
    # that's the default button name
    but_name=  'rename me'
    # here's the magic! your action can be generated in runtime
    # and with any local to that action parameters you want!
    func = gen_handler(but_name)
    keyboard.update({but_name:h.action(func)})
    # forward to THANKS state and update data. Upd_id is used in THANKS
    return States.THANKS, {'keyboard':keyboard,'upd_id':but_name}

def gen_handler(but_id):
    # the generator saves but_id in locals so each handler func is unique
    # and is created every time generator called
    def handler():
        return States.MODIFY_BUT,{'upd_id':but_id}
    return handler

def upd_kb(i,keyboard={},upd_id='rename me'):
    but_name=  i.text
    print('user changes name to ',but_name)
    # delete old button
    del keyboard[upd_id]
    # create a button with new name
    keyboard.update(
        {
            # the format is ad in UI - {"NAME":tgf.action}
            but_name:h.action(gen_handler(but_name))
        }
    )
    # forward to THANKS state and update data. Upd_id is used in THANKS
    return States.THANKS, {'keyboard':keyboard, 'upd_id':but_name}


UI = {
    States.START:
    {
        't':'Hello! click on a button to create or modify',
        'b': [
            # this button will appear to every user, triggers the add_kb func
            {'create button':tgf.action(add_kb)},

            # this post will return data['keyboard'] or {} if no such key
            ## again, data is dict where all user's variables are stored
            h.post(lambda s,**d: d.get('keyboard',{}))
            # Some fancy magic will be done by tgflow above.
            # Before this state is passed, all h.post will be evaluated.
            # This h.post will return an array of buttons

            # tgflow will automatically add the persistent button to 
            # ones that are returned by h.post!
        ]
    },
    States.MODIFY_BUT:{
        't':'Send me the name of button',
        'b':[
            {'cancel':tgf.action(States.START)}
        ],
        # now every time user sends us some text, upd_kb will be called
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
        # this is to stop triggering the previously defibed actiion for upd_kb
        'clear_trig':'text'
    },
}

tgf.configure(
    token=key,
    state=States.START,
             )
tgf.start(UI)

