import logging
logging.basicConfig(level=logging.DEBUG)

from tgflow import TgFlow as tgf
from tgflow import handles as h
from tgflow.api.whatsapp import WhatsAppAPI
from enum import Enum

key='%Your Chat API key'
ep='%Your endpoint from Chat API service'

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
              apiModel=WhatsAppAPI,
              data={"foo":'bar'},
              endpoint=ep,
              verbose=True,
             )
tgf.start(ui)

