
import requests

class Longpoll():
    def __init__(self, upd_checker,
                 params_modifier=lambda x,u: x):
        """
        :param upd_checker:
            a function that returns if
            there was update
            :inp: dict
            :returns: Bool
        :param params_modifier:
            a function that maps previous params
            every time request done and provides
            info if there was updates
            :inp: (dict,bool)
            :returns: dict
        """
        self.func= upd_checker
        self.param_next= params_modifier

    def event_emmitter(self,addr,params={}):
        while True:
            r = requests.get(addr,params)
            js = r.json()
            if r.status_code==200:
                if (self.func(js)):
                    yield js
                    print('upd',params)
                    self.param_next(params,True)
                else:
                    print('no updates, listening more...')
                    self.param_next(params,False)
            else:
                raise Exception('longpoller error',
                                r.status_code,js,
                                'params:',params)

