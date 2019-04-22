import requests

class Analytics:
    def __init__(self, tid_filepath):
        with open(tid_filepath, 'r') as tid_file:
            self._tid = tid_file.read()[:-1]
        self._v = 1

    def _post(self, type_, client_id, state):
        payload = {
            'v': self._v,
            'tid': self._tid,
            'cid': client_id,
            't': type_,
            'dp': state,
        }
        r = requests.post("http://www.google-analytics.com/collect", data=payload)
        return r.ok

    def send_pageview(self, i, s, **d):
        ok = self._post('pageview', i.from_user.id, s.name)
        if not ok:
            print("google analytics: error")
        return {}
