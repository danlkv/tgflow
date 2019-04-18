import gspread
from oauth2client.service_account import ServiceAccountCredentials

class GSheetsApi:
    def __init__(self, auth_filepath):
        scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(auth_filepath, scope)
        self._client = gspread.authorize(creds)
    
    def open_sheet(self, name_or_url):
        if 'docs.google.com' in name_or_url:
            sheet = self._client.open_by_url(name_or_url).sheet1
        else:
            sheet = self._client.open(name_or_url).sheet1
        return sheet 

    def insert_row(self, sheet, row, idx):
        sheet.insert_row(row, idx)

    def get_row_values(self, sheet, idx):
        return sheet.row_values(idx)

    def get_all_values(self, sheet):
        return sheet.get_all_values()

    def del_row(self, sheet, idx):
        sheet.delete_row(idx)

    

    

