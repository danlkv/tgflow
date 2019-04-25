import requests
from bitrix24 import Bitrix24 as bt24
from datetime import datetime
from tgflow.TgFlow import _print as _print

class Bitrix24:
    def __init__(self, creds_filepath, initial_tokens_filepath):
        with open(initial_tokens_filepath, 'r') as f:
            tokens = f.readlines()
        with open(creds_filepath, 'r') as f:
            creds = f.readlines()
        self._client = bt24(creds[0][:-1], client_id=creds[1][:-1], client_secret=creds[2][:-1],
                                access_token=tokens[0][:-1], refresh_token=tokens[1][:-1]) #the last symbol is '\n'
        self._client.refresh_tokens()
        self._token_refresh_time = datetime.now()

    def _check_tokens(self):
        current_time = datetime.now()
        time_diff = current_time - self._token_refresh_time
        if time_diff.seconds > 60 * 50:
            _print('bitrix24: refreshing tokens')
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
        _print('bitrix24: adding a new lead')
        lead_id = self._client.call_method('crm.lead.add', payload)['result']
        return {'bitrix24.lead_id': lead_id}

    def add_contact(self, i, s, **d):
        self._check_tokens()
        lead = self._client.call_method('crm.lead.get', {'id': d['bitrix24.lead_id']})['result']
        payload = {
            'fields': {
                "NAME": lead.get('NAME'),
                "LAST_NAME": lead.get('LAST_NAME'),
                "PHONE": lead["PHONE"],
            }
        }
        _print('bitrix24: adding a new contact')
        contact_id = self._client.call_method('crm.contact.add', payload)['result']
        update_dict = {
            'id': d['bitrix24.lead_id'],
            'fields': {
                'CONTACT_ID': contact_id,
            },
        }
        self._client.call_method('crm.lead.update', update_dict)
        return {'bitrix24.contact_id': contact_id}

    def add_deal(self, i, s, **d):
        self._check_tokens()
        payload = {
            'fields' : {
                "TITLE": "Deal with user {}".format(i.from_user.id), 
                "STAGE_ID": "NEW", 					
                "COMPANY_ID": 3,
                "CONTACT_ID": d.get('bitrix24.contact_id'),
            }
        }
        _print('bitrix24: adding a new deal')
        deal_id = self._client.call_method('crm.deal.add', payload)['result']
        return {'bitrix24.deal_id': deal_id}

    def update_deal(self, target):
        def _update_deal(i, s, **d):
            self._check_tokens()
            update_dict = {
                'id': d['bitrix24.deal_id'],
                'fields': {
                    'STAGE_ID': target,
                },
            }
            _print('bitrix24: updating deal {} to state {}: {}'.format(d['bitrix24.deal_id'], s.name, target))
            self._client.call_method('crm.deal.update', update_dict)
            return {}
        return _update_deal
