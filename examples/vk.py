# This is needed to import module in this folder
import sys
sys.path.insert(0, '..')

import logging
logging.basicConfig(level=logging.DEBUG)

from tgflow import TgFlow as tgf
from tgflow import handles as h
from tgflow.api.vk import vkAPI
from enum import Enum

key='API_KEY'
group='GROUP_ID'

class States(Enum):
    START=1
    INFO=2
    VOICE=10
    LINK=8
    FAV=3
    THANKS=4
def get_voice_link(i):
    link = i.attachments[0]\
        .get('doc',{})\
        .get('preview',{})\
        .get('audio_msg',{})\
        .get('link_mp3',{})\

    return States.LINK, {'link':link}


ui = {
    States.START:{
        't':'Hello there!',
        'b':[
         {'show my info':tgf.action(States.INFO)},
         {'Voice message link':tgf.action(States.VOICE)},
        ]
    },
    States.INFO:{
        't':'Your fav is s',
        'b': [
            {'back to start':tgf.action(States.START)},
        ]

    },
    States.VOICE:{
        't':'Record a message and i will send a link',
        'b': [
            {'back to start':tgf.action(States.START)},
        ],
        'react':tgf.action(get_voice_link,
                           react_to='all')
    },
    States.LINK:{
        't':h.st('here\'s your link: %s','link'),
        'b': [
            {'back to start':tgf.action(States.START)},
        ]
    },
}
tgf.configure(token=key,
              state=States.START,
              apiModel=vkAPI,
              data={"foo":'bar'},
              group_id=group
             )
tgf.start(ui)


"""
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

"""
