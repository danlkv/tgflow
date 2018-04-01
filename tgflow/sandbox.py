import inspect
def myfoo(i,s, course=['s'],gg=2,fdf=3,**d):
    """
    return course id
    Keyword arguments,
    course, -- course object (default None)
    """
    print ('data:',d)
    if course:
        print (course)
        return course.get('id')
    else:
        print("No Course!")
        return None

def caller(i,s,foo=None,**d):
    print ('documentation:\n',foo.__doc__)
    print ('name:\n',foo.__name__)
    print ('signature:\n',inspect.signature(foo))
    print ('fuul arg spec:\n',inspect.getfullargspec(foo))
    print ('defaults:\n',foo.__defaults__)
    print ('kw defaults:\n',foo.__kwdefaults__)
    print ('args:\n',inspect.getargspec(foo))
    spec = inspect.signature(foo)
    params = spec.parameters
    print(params)
    for n,p in params.items():
        print( n)
        print('parameter name:',p.name)
        print('parameter def:',p.default)
        if p.default:
            print('has def',p.default)


    d['course'] = None
    d = dict(d)
    out = foo(1,2,**d)
    print ('output,\n',out)
    return s,d


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
if __name__=='__main__':
    i ='message'
    s = 'state'
    d = {'course':
         {'name':'test course','id':123},
         'fsoo':'bar'}
    ns,nd= caller(i,s,myfoo,**d)
    print('new state %s, new data %s'%(ns,nd))
