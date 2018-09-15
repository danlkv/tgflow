# This is needed to import module in this folder
import sys
sys.path.insert(0, '..')

import logging
logging.basicConfig(level=logging.DEBUG)

from tgflow import TgFlow as tgf
from tgflow import handles as h
from tgflow.api.cli import cliAPI
from enum import Enum

class States(Enum):
    START=1
    INFO=2
    BALOON = 3


ui = {
    States.START:{
        't':'Hello there!',
        'b':[
         {'show my info':tgf.action(States.INFO)},
        ]
    },
    States.INFO:{
        't':'INFOOOOOO',
        'b': [
            {'back to start':tgf.action(States.START)},
            {'make a baloon':tgf.action(States.BALOON)},
        ]
    },
    States.BALOON:{
        't':"""     ,-*****-.

           ,'      _ `.

          /       )_)  \\

         :              :

         \              /

          \            /

           `.        ,'

             `.    ,'

               `.,'

                /\`.   ,-._

                    `-'         hjw


        """,
        'b':[
            {'to start':tgf.action(States.START)}
        ]
    },
}
tgf.configure(token='0',
              state=States.START,
              apiModel=cliAPI,
             )
tgf.start(ui)

