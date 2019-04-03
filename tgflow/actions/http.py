
from ..handles import action
import requests

class HTTPAction(action):
    def __init__(self, endpoint, state, key='http_result', **kw):
        def func(i, s, **d):
            d.update({'_text':i.text})
            ep = endpoint%d
            r = requests.get( ep )
            return state, {key:r.text}
        super().__init__(func, name='HTTP',**kw)
        self.endpoint = endpoint
        self.state = state
    def __repr__(self):
        return '<HTTPAction for %s to state %s'%(
            self.endpoint, self.state
        )



