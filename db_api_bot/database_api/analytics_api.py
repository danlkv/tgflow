from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

class AnalyticsAPI:
    def __init__(self, auth_filepath):
        scope = 'https://www.googleapis.com/auth/analytics.readonly'
        creds = ServiceAccountCredentials.from_json_keyfile_name(auth_filepath, scope)
        self._client = build('analytics', 'v3', creds)