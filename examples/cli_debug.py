# This is needed to import module in this folder
import sys
sys.path.insert(0, '..')

import logging
logging.basicConfig(level=logging.DEBUG)

import tgflow as tgf
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
        ],
        'prepare':lambda i,s,**d: {'info':"Custom start info"},
    },
    States.INFO:{
        't':tgf.post(lambda s,**d: d['info']),
        'b': [
            {'back to start':tgf.action(States.START)},
            {'make a baloon':tgf.action(States.BALOON)},
        ]
    },
    States.BALOON:{
        't':"""
       _-.:.-_
    .'-/_:-;_\- .
   /_'/__ |__'._'\\
  '__(__tgflow )_ '
  (__(___ )___ )__)   
  .__(___.(__  )_ .
   \__\__ )__ /__/
    -__\ _(_ -_.
     \ _\_)./_/
       \_.|_./
        |_|_|
         _
         [_] 
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

