import logging
from .settings import API_KEY, BUTTON_RUN, BUTTON_CANCEL
from .handlers.eoss import eoss
from .handlers.eoss_data_cancelled import eoss_data_cancelled
from .handlers.eoss_data_received import eoss_data_received
from .handlers.eoss_stats import eoss_stats
from .handlers.help_handler import help_handler
from .handlers.receive_poll import receive_poll
from .handlers.receive_poll_answer import receive_poll_answer
from .handlers.start import start
from .helpers.menu import Menu

from telegram import (
    Poll,
    ParseMode,
    KeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Updater,
    CommandHandler,
    PollAnswerHandler,
    PollHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    CallbackQueryHandler
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def run_bot():
    updater = Updater(API_KEY)
    menu = Menu()
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))

    # Setting property owning request
    # TODO: как-то пользователь присылает сообщения, чем он владеет. Когда он присылает — говорим, мол, спасибо, скоро заапрувим и вы получите об этом сообщение.

    # EOSS starting
    dispatcher.add_handler(MessageHandler(Filters.regex(menu.LABEL_EOSS_START), eoss))
    dispatcher.add_handler(MessageHandler(Filters.poll, receive_poll))
    dispatcher.add_handler(MessageHandler(Filters.regex(BUTTON_RUN), eoss_data_received))
    dispatcher.add_handler(MessageHandler(Filters.regex(BUTTON_CANCEL), eoss_data_cancelled))
    dispatcher.add_handler(PollAnswerHandler(receive_poll_answer))

    # EOSS Stats
    dispatcher.add_handler(MessageHandler(Filters.regex(menu.LABEL_STATS), eoss_stats))

    # Working with property
    dispatcher.add_handler(MessageHandler(Filters.regex(menu.LABEL_LIST_MY_PROPERTY), help_handler)) # TODO: change this
    dispatcher.add_handler(MessageHandler(Filters.regex(menu.LABEL_CHANGE_MY_PROPERTY), help_handler)) # TODO: change this

    dispatcher.add_handler(CommandHandler('help', help_handler))

    # TODO: ещё тут надо как-то ловить событие, что юзера подтвердили и отправлять ему сообщение

    # Start the Bot
    updater.start_polling()
    print("groups")
    print(dispatcher.groups)
    print("bot data")
    print(dispatcher.bot_data)
    print("chat data")
    print(dispatcher.chat_data)

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


    print ("OK")