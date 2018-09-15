from .base import tgfAPI
from .cli_bot import CLIBot

class cliAPI(tgfAPI):
    def __init__(self,token,**args):
        super().__init__(token)
        self.bot = CLIBot()

    def start(self,**args):
        while True:
           self.bot.start_polling(**args)

    def send(self,id,**args):
        self.bot.send_message(
            text=args['text'],
            reply_markup =args['markup']
        )

    def update(self,msg,**args):
        # here msg is the type set_message_handler pass
        text =args.get('text')
        markup=args.get('markup')
        self.bot.send_message(
            text=text,
            reply_markup =markup
        )

    def set_message_handler(self,clb):
        self.bot.set_message_handler(clb)

    def set_callback_handler(self,clb):
        self.bot.set_callback_handler(clb)

    def KeyboardButton(self,**args):
        return (args.get('text'),
                args.get('callback_data')
               )
    def KeyboardMarkup(self,buttons=None,**args):
        return buttons

