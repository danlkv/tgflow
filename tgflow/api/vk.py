from .base import tgfAPI
from .vk_bot import VKBot

class vkAPI(tgfAPI):
    def __init__(self,token):
        super().__init__(token)
        self.bot = VKBot(token)

    def start(self,**args):
        self.bot.start_polling(**args)

    def send(self,id,**args):
        self.bot.send_message(
            text=args['text'],
            chat_id=id,
            parse_mode='Markdown',
            reply_markup =args['markup']
        )

    def update(self,msg,**args):
        # here msg is the type set_message_handler pass
        text =args.get('text')
        markup=args.get('markup')
        if text:
            self.bot.edit_message_text(
                text=text,
                chat_id=msg.chat.id,
                parse_mode='Markdown',
                message_id=msg.message_id,
            )
        if markup:
            print("tgflow: updating markup",markup)
            self.bot.edit_message_reply_markup(
                chat_id=msg.chat.id,
                message_id=msg.message_id,
                reply_markup=markup)

    def set_message_handler(self,clb):
        self.bot.set_message_handler(clb)

    def set_callback_handler(self,clb):
        # is there analog to upd_listener in telebot?
        self.bot.set_callback_handler(clb)

