from .base import tgfAPI
from .vk_user_bot import VKUserBot
from .Types import *

class vk_userAPI(tgfAPI):
    def __init__(self,token,**args):
        super().__init__(token)
        self.bot = VKUserBot(token,
                args.get('group_id'),
                lp_ep='messages.getLongPollServer'
                )

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
        id = msg.chat.id
        self.bot.send_message(
            text=text,
            chat_id=id,
            parse_mode='Markdown',
            reply_markup =markup
        )

    def set_group_id(self,gid):
        # You should call this just after api creation
        self.bot.group = gid

    def set_message_handler(self,clb):
        self.bot.set_message_handler(clb)

    def set_callback_handler(self,clb):
        # is there analog to upd_listener in telebot?
        self.bot.set_callback_handler(clb)

    def KeyboardButton(self,**args):
        return VkKeyboardButton(
            **args
        )
    def KeyboardMarkup(self,buttons=None,**args):
        mk = VkKeyboard(buttons=buttons, **args)
        return mk


