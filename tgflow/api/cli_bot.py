class Message():
    def __init__(s,text):
        s.chat=Chat('0')
        s.text=text
class Chat():
    def __init__(s,i):
        s.id = i
class Callback():
    def __init__(self,msg,data):
        self.message=msg
        self.data = data

BUTTON_KEY = '_'
START_KB_IDX = 1

class CLIBot:
    def __init__(self):
        self.keyboard = []
        pass

    def start_polling(self,**args):
        print("cli|bot>>>",end=' ')
        msg = Message(input())
        call =None
        if msg.text[0]==BUTTON_KEY:
            call_id=msg.text[1:]
            call = self.keyboard[int(call_id)-START_KB_IDX]
            call = Callback(msg,call)
        if call:
            self.callback_handler(call)
        else:
            self.message_handler([msg])

    def _update_kb(s,button):
        s.keyboard.append(button[1])

    def send_message(self,text,**args):
        self.keyboard = []
        mk = args.get('reply_markup')
        butnames = []
        if mk:
            kb,i = "",START_KB_IDX
            for b in mk:
                butnames.append(BUTTON_KEY+"%i:%s"%(i,b[0]))
                self._update_kb(b)
                i+=1
        kb=tabeled(butnames)

        print("\ncli|bot:>>new message>>")
        msg = bordered(text+"\n"+kb)
        print(msg)
        return text

    def set_message_handler(self,clb):
        self.message_handler =  clb
    def set_callback_handler(self,clb):
        self.callback_handler = clb

def tabeled(texts):
    width = max(len(t) for t in texts)
    res = ['┌' + '─' * width + '┐']
    if len(texts)>1:
        for text in texts[:-1]:
            res.append('│' + (text + ' ' * width)[:width] + '│')
            res.append('├' + '┄' * width + '┤')
        res.append('│' + (texts[-1] + ' ' * width)[:width] + '│')
        res.append('└' + '─' * width + '┘')
        return '\n'.join(res)
    else:
        return bordered(texts[0])

def bordered(text):
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = ['┌' + '─' * width + '┐']
    for s in lines:
        res.append('│' + (s + ' ' * width)[:width] + '│')
    res.append('└' + '─' * width + '┘')
    return '\n'.join(res)
