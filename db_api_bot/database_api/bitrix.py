from bitrix24 import Bitrix24
import requests
from datetime import datetime

DOMAIN = 'b24-dw3931.bitrix24.ru'

class Bitrix:
    def __init__(self, tokens_filepath, creds_filepath):
        with open(tokens_filepath, 'r') as f:
            tokens = f.readlines()
        with open(creds_filepath, 'r') as f:
            creds = f.readlines()
        self._client = Bitrix24(DOMAIN, client_id=creds[0][:-1], client_secret=creds[1][:-1],
                                access_token=tokens[0][:-1], refresh_token=tokens[1][:-1])
        self._client.refresh_tokens()
        self._token_refresh_time = datetime.now()

    def _check_tokens(self):
        current_time = datetime.now()
        time_diff = current_time - self._token_refresh_time
        if time_diff.seconds > 60 * 50:
            self._client.refresh_tokens()
            self._token_refresh_time = current_time

    def add_lead(self, i, s, **d):
        self._check_tokens()
        lead_data = {
            "fields":{
                "TITLE": "FatJoint LLC",
                "NAME": i.from_user.first_name,
                "LAST_NAME": i.from_user.last_name,
                "STATUS_ID": "NEW",
                "OPENED": "Y",
                "ASSIGNED_BY_ID": 1,
                "CURRENCY_ID": "BTC",
                "OPPORTUNITY": 12500,
                "PHONE": [ { "VALUE": i.from_user.id, "VALUE_TYPE": "WORK" } ] 
            }
        }

        self._client.call_method('crm.lead.add', lead_data)
        return {}
