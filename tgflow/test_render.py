import handles as h
import copy
from enum import Enum
import render
class States(Enum):
    HI=1
    bu=0
UI={
    States.HI:{
        't':"Hello",
        'b':h.post('foo'),
        'f':['he','llo',h.post('world')]
    },
    States.bu:h.post('bar')
}

def bar(a,s,foo=None,**d):
    return foo

class sobake:
    def __init__(self,a):
       self.a = a

d={
    'foo':"here cFOO",
    'bar':{'t':"BOO",
           'b':h.post('kaka'),
           'r':h.post(bar)
          },
    'kaka':sobake('s'),
    'world':'worlD'

}

a = 'action'
s = 'state'
args = {'a':a,'s':s,'d':d}
ui = render.prep(UI,args)
print('\n before')
render.pp.pprint(UI)
print('\n data')
render.pp.pprint(d)
print('\n rendered')
render.pp.pprint(ui)
