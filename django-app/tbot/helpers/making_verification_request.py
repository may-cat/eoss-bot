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
from ..models import *

class MakingVerificationRequest():

    @staticmethod
    def _get_verification_request(user: User):
        verification_requests = VerificationRequest.objects.filter(user=user)
        return verification_requests[len(verification_requests)-1]

    @staticmethod
    def ask_flat(update: Update, context: CallbackContext, user: User):
        FIRST_FLAT = 463
        LAST_FLAT = 504
        keyboard = []
        floor = []
        for i in range(FIRST_FLAT, LAST_FLAT+1):
            floor.append(InlineKeyboardButton(str(i), callback_data="owning_flat_"+str(i)))
            if (i-FIRST_FLAT+1)%3 == 0:
                keyboard.append(floor)
                floor = []
        keyboard.append(floor)
        keyboard.append([InlineKeyboardButton("Нет квартиры", callback_data="owning_flat_none")])
        markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("🏠 Укажите, собственником какой квартиры вы являетесь:", reply_markup=markup)

        verification_request = VerificationRequest(
            user=user,
            section="10 секция" # TODO: это не должно быть хардкодом
        )
        verification_request.save()

    @staticmethod
    def catch_flat(update: Update, context: CallbackContext, user: User):
        verification_request = MakingVerificationRequest._get_verification_request(user)
        if  hasattr(update,'data'):
            verification_request.flat = update['data']
        else:
            verification_request.flat = update.message.text
        verification_request.save()

        update.message.reply_text(
            'Получил информацию о квартире'
        )

    @staticmethod
    def ask_parking(update: Update, context: CallbackContext, user: User):
        keyboard = []
        keyboard.append([InlineKeyboardButton("Нет паркинга", callback_data="owning_parking_none")])
        markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("🏠 Напишите ответным сообщением, какие у вас в собственности места паркинга или нажмите на кнопку \"Нет паркинга\"", reply_markup=markup)

    @staticmethod
    def catch_parking(update: Update, context: CallbackContext, user: User):
        verification_request = MakingVerificationRequest._get_verification_request(user)
        verification_request.parking = update.message.text
        verification_request.save()
        update.message.reply_text(
            'Получил информацию о паркинге'
        )

    @staticmethod
    def catch_no_parking(update: Update, context: CallbackContext, user: User):
        verification_request = MakingVerificationRequest._get_verification_request(user)
        verification_request.parking = "----"
        verification_request.save()

        update.message.reply_text(
            'Получил информацию что паркинга нет'
        )

    @staticmethod
    def ask_storeroom(update: Update, context: CallbackContext, user: User):
        keyboard = []
        keyboard.append([InlineKeyboardButton("Нет кладовок", callback_data="owning_parking_none")])
        markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("🏠 Напишите ответным сообщением, какие у вас в собственности кладовки или нажмите на кнопку \"Нет кладовок\"", reply_markup=markup)

    @staticmethod
    def catch_storeroom(update: Update, context: CallbackContext, user: User):
        verification_request = MakingVerificationRequest._get_verification_request(user)
        verification_request.storeroom = update.message.text
        verification_request.save()
        update.message.reply_text(
            'Получил информацию о кладовках'
        )

    @staticmethod
    def catch_no_storeroom(update: Update, context: CallbackContext, user: User):
        verification_request = MakingVerificationRequest._get_verification_request(user)
        verification_request.storeroom = "-----"
        verification_request.save()
        update.message.reply_text(
            'Получил информацию что кладовки нет'
        )

    @staticmethod
    def ask_commerce(update: Update, context: CallbackContext, user: User):
        keyboard = []
        keyboard.append([InlineKeyboardButton("Нет коммерческой недвижимости", callback_data="owning_parking_none")])
        markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("🏠 Напишите ответным сообщением, какая у вас в собственности коммерческая недвижимость или нажмите на кнопку \"Нет коммерческой недвижимости\"", reply_markup=markup)

    @staticmethod
    def catch_commerce(update: Update, context: CallbackContext, user: User):
        verification_request = MakingVerificationRequest._get_verification_request(user)
        verification_request.commerce = update.message.text
        verification_request.save()
        update.message.reply_text(
            'Получил информацию о коммерческой недвижимости'
        )

    @staticmethod
    def catch_no_commerce(update: Update, context: CallbackContext, user: User):
        verification_request = MakingVerificationRequest._get_verification_request(user)
        verification_request.commerce = "-----"
        verification_request.save()
        update.message.reply_text(
            'Получил информацию что коммерческой недвижимости нет'
        )


    @staticmethod
    def tell_verification_is_pending(update: Update, context: CallbackContext, user: User):
        update.message.reply_text(
            'Ваша заявка принята и обрабатывается администратором. Он скоро свяжется с вами.'
        )




















