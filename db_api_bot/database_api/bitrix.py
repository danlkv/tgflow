from bitrix24 import Bitrix24
import requests
from datetime import datetime

class Bitrix:
    def __init__(self, tokens_filepath, creds_filepath):
        with open(tokens_filepath, 'r') as f:
            tokens = f.readlines()
        with open(creds_filepath, 'r') as f:
            creds = f.readlines()
        self._client = Bitrix24(creds[2][:-1], client_id=creds[0][:-1], client_secret=creds[1][:-1],
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
        payload = {
            "fields":{
                "TITLE": 'Lead with id {}'.format(i.from_user.id),
                "NAME": i.from_user.first_name,
                "LAST_NAME": i.from_user.last_name,
                "STATUS_ID": "NEW",
                "PHONE": [ { "VALUE": i.from_user.id} ] 
            }
        }
        lead_id = self._client.call_method('crm.lead.add', payload)['result']
        return {'bitrix24.lead_id': lead_id}

    def add_contact(self, i, s, **d):
        self._check_tokens()
        lead = self._client.call_method('crm.lead.get', {'id': d['bitrix24.lead_id']})['result']
        payload = {
            'fields': {
                "NAME": lead['NAME'],
                "LAST_NAME": lead.get('LAST_NAME'),
                "PHONE": lead["PHONE"]
            }
        }
        contact_id = self._client.call_method('crm.contact.add', payload)['result']
        return {'bitrix24.contact_id': contact_id}

    def add_deal(self, i, s, **d):
        self._check_tokens()
        payload = {
            'fields' : {
                "TITLE": "Deal with user {}".format(i.from_user.id), 
                "STAGE_ID": "NEW", 					
                "COMPANY_ID": 3,
                "CONTACT_ID": d['bitrix24.contact_id'],
            }
        }
        deal_id = self._client.call_method('crm.deal.add', payload)['result']
        return {'bitrix24.deal_id': deal_id}
