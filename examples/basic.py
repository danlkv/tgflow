from tgflow import TgFlow
from enum import Enum
key='539066078:AAHCUsr8ZoP9JtP5KqOMuL7f_UoFyyH6wik'

class States(Enum):
    START=1

TgFlow.__init__(key)
TgFlow.set_default_state_data(States.START,{"foo":'bar'})
TgFlow.start({States.START:{'t':'hello'}})

