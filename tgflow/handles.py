import inspect
from inspect import signature
from enum import Enum
import pprint
pp = pprint.PrettyPrinter(indent=4)

class post():
    def __init__(self,func,name=None):
        if isinstance(func,str):
            k = func
            func = lambda s,**d: d.get(k)
        else: k = None
        self.__name__ = str(name or func.__name__)
        self.f= func
        self.k = k
    def __repr__(self):
        if self.k:
            return "<post func: key "+self.k.__repr__()+">"
        else: return "<post func: "+self.f.__name__+str(signature(self.f))+">"
    def apply(self,s,d):
        return self.f(s,**d)

class action():
    def __init__(self,func,name=None,react_to=None):
        if isinstance(func,Enum):
            ns = func
            func = lambda i,s,**d: (ns, d)
        else: ns = None
        self.__name__ = str(name or func.__name__)
        self.react_to = react_to
        self.f= func
        self.ns = ns
    def __repr__(self):
        if self.ns:
            return "<+action: state "+self.ns.__repr__()+">"
        else:
            try:
                return "<+action: "+self.f.__name__+str(signature(self.f))+">"
            except TypeError:
                return "<+action: "+self.f.__repr__()+">"
    def call(self,i,s,**d):
        # TODO: check signature
        inp = {'i':i,'s':s,'d':d}
        args,kwargs=get_args_kwargs(self.f)
        if len(args)>3:
            print('No more than 3 arguments withoud def')
        else:
            if inspect.getargspec(self.f)[2]=='d':
                print ('ff',self.__repr__())
                return self.f(i,s,**d)
            to_pass = {name:inp.get(name) for name in args}
            for name in kwargs:
                val = d.get(name)
                if val:
                    to_pass[name]=val
        outp = self.f(**to_pass)
        if outp:
            if isinstance(outp,tuple):
                if len(outp)==2:
                    # User has to return state as first and data as second value
                    ns = outp[0]
                    print("OUTPUT OF %s:"%str(self.f))
                    pp.pprint(outp)
                    d.update(outp[1])
                if len(outp)==1:
                    ns = outp[0]
            else:
                ns = outp
        else:
            ns = s
        return ns,d

def safeget(dct,keylist):
    for key in keylist:
        try:
            dct = dct[key]
        except KeyError:
            return None
    return dct
def st(string,key):
    if isinstance(key,str):
        return post(lambda s,**d: string%d.get(key))
    else:
        return post(lambda s,**d: string%safeget(d,key))
def obj(o):
    return  post(lambda s,**d: o)
def data_key(key):
    return  post(lambda s,**d: d['key'])

def choose(key,options,default = None):
    return post(lambda s,**d: options.get(d.get(key),default))


def get_args_kwargs(foo):
    """
    callable->[],[]
    function that determines which argumnents have a default value
    :return: tuple of lists of names [args],[args_with_def]
    """
    spec = inspect.signature(foo)
    params = spec.parameters
    args,args_with_def=[],[]
    for n,p in params.items():
        if p.default is p.empty:
            args.append(n)
        else:
            args_with_def.append(n)
    return args,args_with_def
