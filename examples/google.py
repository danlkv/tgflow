import tgflow as tgf
import re, urllib
from enum import Enum
key='539066078:AAHCUsr8ZoP9JtP5KqOMuL7f_UoFyyH6wik'

class States(Enum):
    START=1
    RESULT=2

UI = {
    States.START:
    {'t':'Hello! You can send me some text and I will google it',
     'react':tgf.HTTPAction(
         'http://google.com/search?q=%(_text)s',
         States.RESULT,
         react_to = 'text'),
    },
    States.RESULT:{
        't':tgf.st("result is %s",'result'),
        'prepare':lambda i,s,**d: {'result':
                                   re.search(
                                       '"r"><a href=".+?q=(.*?)&amp.+?">(.*?)<\/a></h3>',
                                       d['http_result']
                                   ).group(1)
                                  }


    }
}
tgf.configure(token=key, verbose=True, state=States.START)
tgf.start(UI)
