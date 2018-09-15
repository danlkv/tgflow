# This is needed to import module in this folder
import sys
sys.path.insert(0, '..')
import logging
logging.basicConfig(level=logging.DEBUG)


import tgflow as tgf
from tgflow import handles as h
from enum import Enum
key='539066078:AAHCUsr8ZoP9JtP5KqOMuL7f_UoFyyH6wik'

class States(Enum):
    START=1
    LIST=2
    ITEM=3

# this function will be used to prefetch list
# signature is strict
def database_call(i,s,**d):
    # perform DB fetch
    # format is ('Name','details')
    kb = [
        ('Corn',"""Corn or maize is a large-grained crop 
         native to the Americas"""),
        ('Tomato',"The tomato is the edible, often red, berry"),
        ('Cucumber',"""Cucumber is a software tool used 
         by computer programmers for testing other software""")
    ]
    # modify the data dict
    d.update({'kb':kb})
    return d

def gen_keyboard(s,**d):
    kb_data=d.get('kb')

    def gen_handler(name,desc):
        return lambda: (States.ITEM,
                        {"ItemText":name+"\n"+desc})
    keyboard = {
        # the format is ad in UI - {"NAME":tgf.action}
        name: tgf.action(
            gen_handler(name,desc)
            )
        for name,desc in kb_data
    }
    # forward to THANKS state and update data. Upd_id is used in THANKS
    print (keyboard)
    return keyboard

UI = {
    States.START:
    {
        't':'Hello! Follow the button to display list of items',
        'b': [
            # this button will appear to every user, triggers the add_kb func
            {'Display list':tgf.action(States.LIST)},
        ]
    },
    States.LIST:{
        't':'Here is your items list',
        'b':[
            # return value from gen_keyboard will be put here 
            # in runtime
            tgf.post(gen_keyboard),
            {'back':tgf.action(States.START)}
        ],
        # Before processing state db call will be executed
        'prepare':database_call
    },
    States.ITEM:{
        't':tgf.st('Item: %s','ItemText'),
        'b': [
            {'back to List':tgf.action(States.LIST)},
        ],
    },
}

tgf.configure(
    token=key,
    state=States.START,
             )
tgf.start(UI)

