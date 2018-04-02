# Here is an idea of how to combine coffeescript dict generation with python functions
from . import handles as h
import js2py, coffeescript, json, re,copy,pprint
a = h.action

pp = pprint.PrettyPrinter(indent=4)
def coffee_encode(d):
    # 'action' encodes action names in a way python can receive it 
    coffee = """
action = (s)->'+action|'+s+'|o+'
subst = (s)->'+post|'+s+'|o+'
a = action
ps = subst
u=%s
return u"""%d
    #print('>COFEEE>\n',coffee)
    js = coffeescript.compile(coffee)
    #print('>JS>\n',js)
    obj =js2py.eval_js(js)
    d = obj.to_dict()
    s = str(obj)
    #print(s)
    #d = json.loads(s.replace('\'','\"'))
    return d

def map_dict(d,func):
    if isinstance(d,dict):
        for k,v in d.items():
            d[k] = map_dict(v,func)
    elif isinstance(d,list):
        d = [map_dict(v,func) for v in d]
    else:
        try:
            d = func(d)
        except Exception as e:
            print('failed to map on element \'%s\', Exception:'%str(d),e)
            d = d
    return d

class CoffeeUI:
    def __init__(self,ui_coffee={},states=None,actions={}):
        self.funcs = {}
        self.ui_coffee = ui_coffee
        self.states={}
        if states:
            self.states ={st.name:st for st in states}
        self.actions = actions
        # generate python dict from coffee code
        self.ui=coffee_encode(ui_coffee)
        # TODO: add support for one-time processing of actions list

    def set_ui(self,ui):
        self.ui = ui_coffee

    def add_action(self,name,act,react_to=None):
        # a wrapper on top of handles.action,
        # fills a lookup dict to substitute by user defied name
        if isinstance(act,h.action):
            self.actions[name]=act
        elif callable(act):
            self.actions[name] = h.action(act,react_to=react_to)

    def add_subst(self,name,act):
        # a wrapper on top of handles.post
        # fills a lookup dict to substitute by user defied name
        if isinstance(act,h.post):
            self.actions[name]=act
        else:
            self.actions[name] = h.post(act)

    def a(self,name,react_to=None):
        return self.add_action(name,react_to)

    def paste_actions(self,u):
        # get the name from matched re object and paste action
        print(type(u))
        if callable(u):
            return h.action(u)
        r=re.search(r'\+(action|post)\|(.+?)\|o\+',u)
        if r:
            if r.group(1)=='action':
                # this is an action
                t = r.group(2)
                if t in self.states.keys():
                    # paste a state instead of it's name
                    a = h.action(self.states.get(t))
                else:
                    a = self.actions.get(r.group(2))
            if r.group(1)=='post':
                # this is a post
                a = self.actions.get(r.group(2))
            if not a:
                print("Couldn't find action with name %s"%r.group(2))
            return a
        else:
            return u

    def get_ui(self):
        # replace every string corresponding to action with action
        # 'action' in coffee code defines endoding of function name
        #print("actions registered")##
        #print(self.actions)
        #print('before\n',self.ui_coffee)
        ui = map_dict(self.ui,self.paste_actions)
        # paste States instead of their names
        if self.states:
            d={}
            for k,v in ui.items():
                # get state by name
                d[self.states.get(k)]=v
            ui = d
        #print('result\n')
        pp.pprint(ui)
        return ui

if __name__=='__main__':
    # some test code
    t= CoffeUI(
    """
    COURSE:
        t:ps 'Hello, %name'
        b:ps 'get_buttons'
        kb_txt: 'Welcome!'
        kb: a 'get_buttons'
    APPLY:
        t: 'Please type your first name'
        react: a 'name'
    LNAME:
        f:(f)->
            f.name='blah'
            f
        t: 'Please type your last name'
        react: a 'react_to_lname'
    PROGRESS:
        t: ps 'Im sorry %s but im not currently supportingname'
        b: [ 'Back Home': a 'HOME' ]
    """)

    t.a('get_buttons',h.choose('role',
    coffee_encode(
    """
    student:
        'Show assignments':a 'ASSIGNMENTS'
        'Submit assignment':a 'SEND_ASS'
        'My progress':a 'PROGRES'
    applicant:
        Apply:a 'APPLY'""")
                          ))
    t.a('react_to_lname',a(lambda i,s,**d:\
                                    (States.LNAME,dict(d,fname=i.text)),
                                     react_to='text'))
    t.a('name',a(lambda i,s,**d:\
                                    (States.LNAME,dict(d,fname=i.text)),
                                     react_to='text'))
    print('\n')

    ui = t.get_ui()
    print(type(a),a)
