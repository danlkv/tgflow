import requests
from tgflow.TgFlow import _print as _print

class Analytics:
    def __init__(self, tracking_id_filepath):
        with open(tracking_id_filepath, 'r') as tid_file:
            self._tracking_id = tid_file.read()[:-1] #the last symbol is '\n'
        self._version = 1

    def _post(self, type_, client_id, state):
        payload = {
            'v': self._version,
            'tid': self._tracking_id,
            'cid': client_id,
            't': type_,
            'dp': state,
        }
        r = requests.post("http://www.google-analytics.com/collect", data=payload)
        return r.ok

    def send_pageview(self, i, s, **d):
        _print('analytics: sending pageview \'{}\''.format(s.name))
        ok = self._post('pageview', i.from_user.id, s.name)
        if not ok:
            print("google analytics: error")
        return {}
