from .base import tgfAPI
import telebot

class telegramAPI(tgfAPI):
    def __init__(self,token,**args):
        super().__init__(token)
        self.bot = telebot.TeleBot(token)

    def start(self,**args):
        self.bot.polling(**args)

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
        self.bot.set_update_listener(clb)

    def set_callback_handler(self,clb):
        # is there analog to upd_listener in telebot?
        @self.bot.callback_query_handler(func=lambda x:True)
        def stub(call):
            clb(call)

    def KeyboardButton(self,**args):
        return telebot.types.InlineKeyboardButton(
            **args
        )
    def KeyboardMarkup(self,buttons=None,**args):
        mk = telebot.types.InlineKeyboardMarkup(
            **args)
        mk.add(*buttons)
        return mk

