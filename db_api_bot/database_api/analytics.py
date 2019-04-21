import requests

class Analytics:
    def __init__(self, tid_filepath):
        with open(tid_filepath, 'r') as tid_file:
            self._tid = tid_file.read()[:-1]
        self._v = 1

    def post(self, type_, client_id, state):
        payload = {
            'v': self._v,
            'tid': self._tid,
            'cid': client_id,
            't': type_,
            'dp': state,
        }
        requests.post("http://www.google-analytics.com/collect", data=payload)
        return {}
