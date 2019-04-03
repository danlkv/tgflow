# This is needed to import this module
import sys
sys.path.insert(0, '..')

import tgflow as tgf
from tgflow import TgFlow as tgf
from tgflow import handles as h
from enum import Enum
import time
key='539066078:AAHCUsr8ZoP9JtP5KqOMuL7f_UoFyyH6wik'


def handle_delay(i, s, **d):
    delay = int(i.text)
    tgf.send_state(States.SET, i.from_user.id, data = {'delay':delay})
    print("sleeping for",delay)
    time.sleep(delay)
    print("done",delay)
    return States.NOTIF, {'delay':delay}

class States(Enum):
    START=1
    REMIND=2
    NOTIF=3
    SET=4

UI = {
    States.START:
    {'t':'Hi! You can set up a reminder here.',
     'kb': [
         {'Set up a reminder':tgf.action(States.REMIND)},
     ]},
    States.REMIND:{
        't':'Please send me a delay in seconds:',
        'b':[{'Back':tgf.action(States.START)}],
        'react':h.action(
            handle_delay,
            react_to = 'text'),
    },
    States.SET:{
        't':h.st('Delay is %s','delay'),
        'b': [
            {'back to start':tgf.action(States.START)},
        ],
        'clear_trig':'text',
    },
    States.NOTIF:{
        't':h.st('Hey! time\'s up! delay was: %s','delay'),
         'b': [
            {'back to start':tgf.action(States.START)},
         ],
        'clear_trig':'text'},
    }

tgf.configure(token=key,
              verbose=True,
                 state=States.START,
                 data={"delay":'unin'})
tgf.start(UI)
