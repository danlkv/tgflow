import tgflow
from enum import Enum
from gsheetsapi import GSheetsApi

key = '650613812:AAErWCUWakQAl65dtvk-mTfmNvEYAEdltVA'
auth_filepath = 'client_secret.json'
db_api = GSheetsApi(auth_filepath)

class States(Enum):
    ERROR = 0
    START = 1
    CHOOSE = 2
    SUCCESS = 3
    PUT = 4
    GET = 5

    
def open_sheet(i, s, **d):
    print('open sheet')
    sheet = db_api.open_sheet(i.text)
    upd_data = {'sheet': sheet}
    return States.CHOOSE, upd_data

def insert_row(i, s, **d):
    print('insert row')
    idx, row = i.text.split()
    idx = int(idx)
    db_api.insert_row(d['sheet'], row, idx)
    return States.SUCCESS, {}

def get_all_data(i, s, **d):
    data = db_api.get_all_values(d['sheet'])
    return States.GET, {'data': data}


UI = {
    
    States.START:{
        'text' : ('Hello, I can help you work with Google Spreadsheets. '
                    'Just send me your spreadsheet name and let\'s get started!'),
        'react' : tgflow.action(open_sheet, react_to='text')
    },
    
    States.CHOOSE:{
        'text' : 'What should I do?',
        'buttons' : [
            {'Insert row' : tgflow.action(States.PUT)},
            {'Recieve all data' : tgflow.action(get_all_data)}
        ],
    },
    
    States.PUT:{
        'text' : "Please type data as \'<row number> <your data>\'.",
        'buttons' : [{'Back' : tgflow.action(States.CHOOSE)}],
        'react' : tgflow.action(insert_row, react_to = 'text')       
    },
    
    States.SUCCESS:{
        'text' : 'Done successfully!', 
        'buttons' : [{'Continue' : tgflow.action(States.CHOOSE)}]
    },
    
    States.GET:{
        'text' : tgflow.handles.st('Here is your data:\n%s', 'data'),
        'buttons' : [{'Continue' : tgflow.action(States.CHOOSE)}]
    },
    
    States.ERROR:{
    }  
    
}


tgflow.configure(token=key,
                 state=States.START,
                 data={"foo":'bar'},
                 verbose=True)
tgflow.start(UI)