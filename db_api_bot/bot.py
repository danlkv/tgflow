import tgflow
from enum import Enum
import database_api
from datetime import datetime 

#key = '650613812:AAErWCUWakQAl65dtvk-mTfmNvEYAEdltVA'
key='539066078:AAHCUsr8ZoP9JtP5KqOMuL7f_UoFyyH6wik'
auth_filepath = 'database_api/client_secret.json'
db_api = database_api.GSheetsApi(auth_filepath)

class States(Enum):
    ERROR = 0
    START = 1
    CHOOSE = 2
    SUCCESS = 3
    PUT = 4
    GET = 5
    
def open_sheet(i, s, **d):
    print('open sheet')
    try:
        sheet = db_api.open_sheet(i.text)
    except Exception as exc:
        print(exc)
        return States.ERROR, {}

    upd_data = {'sheet': sheet}
    return States.CHOOSE, upd_data

def insert_row(i, s, **d):
    idx, data = i.text.split(maxsplit=1)
    idx = int(idx)
    row = data.split()
    row = [datetime.now()] + row
    print ('insert row at index {}'.format(idx))
    try:
        db_api.insert_row(d['sheet'], row, idx)
    except Exception as exc:
        print(exc)
        return States.ERROR, {}

    return States.SUCCESS, {}

def get_all_data(i, s, **d):
    data = db_api.get_all_data(d['sheet'])
    return States.GET, {'data': data}

UI = {
    
    States.START:{
        'text' : ('Hello, I can help you work with Google Spreadsheets. '
                  'Share your sheet with developer@treebo.iam.gserviceaccount.com.' 
                  'Then just send me your spreadsheet name and let\'s get started!'),
        'react' : tgflow.action(open_sheet, react_to='text'),
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
        'text':'Sorry there was an err9r',
        'buttons': [{'Start':tgflow.action(States.START)}]
    }  
}


tgflow.configure(token=key,
                 state=States.START,
                 verbose=True
                )
tgflow.start(UI)
