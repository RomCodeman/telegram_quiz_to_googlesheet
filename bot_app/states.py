from telebot import types

from bot_app.bot_text_templates import (LAUNCH_TEXT, WELCOME_TEXT, QUESTION_NAME_TEXT, QUESTION_PHONE_TEXT,
                                        QUESTION_WITH_VARS_TEXT,
                                        ANSWER_PROCESS_TEXT, ANSWER_CONFIRM_TEXT, FINAL_TEXT)
from bot_app.logger import logger

from config import bot


# STATE 0: Basic states signatures
class BasicState:
    text: str = WELCOME_TEXT
    button_title_get_this_state: str = ''
    callback_for_state: str = "getstate:BasicState"
    buttons_click_default_state: dict = {}

    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.keyboard: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()
        self.handlers = []
        self.buttons_state = {}

    # Returns Button with name and callback specified for State.
    @classmethod
    def button_next_state(cls, next_state_button_name_custom=None):
        if next_state_button_name_custom:
            return types.InlineKeyboardButton(text=next_state_button_name_custom, callback_data=cls.callback_for_state)
        return types.InlineKeyboardButton(text=cls.button_title_get_this_state, callback_data=cls.callback_for_state)

    # Returns State class relevant to callback
    @classmethod
    def handler_callback_to_state(cls, callback: types.CallbackQuery):
        if hasattr(callback, 'data'):
            if callback.data == cls.callback_for_state:
                return True, cls
            else:
                logger.warning(f"Callback unrecognized | button_callback == {callback.data}, "
                               f"cls.callback_data_for_state == {cls.callback_for_state} |||")
        return False, cls

    # Add buttons and handlers to current state instance
    @classmethod
    def insert_and_handle_button(cls, current_state: "BasicState", next_state_button_name_custom=None):
        current_state.keyboard.add(cls.button_next_state(next_state_button_name_custom))
        current_state.handlers.append(lambda msg: cls.handler_callback_to_state(msg))

    # Iterating button handlers for state class obtaining if it relevant to callback
    def process_with_callback_handlers(self, callback: types.CallbackQuery):
        for handler in self.handlers:
            ok, state_class = handler(callback)
            if ok:
                return state_class(self.chat_id)
        return self

    def display(self, message: types.Message or types.CallbackQuery):
        logger.error(f"Technical state: {self.__class__.__name__} | Method: display")


# State 1. "/start" command state
class LaunchState(BasicState):
    text: str = LAUNCH_TEXT

    def __init__(self, chat_id):
        super().__init__(chat_id)
        NameQuestionState.insert_and_handle_button(self)

    def display(self, message: types.Message):
        bot.send_message(self.chat_id, self.text, reply_markup=self.keyboard)


# State 1.1. Restart action state.
class WelcomeState(BasicState):
    text: str = WELCOME_TEXT
    button_title_get_this_state = 'RESTART'
    callback_for_state = "getstate:WelcomeState"

    def __init__(self, chat_id):
        super().__init__(chat_id)
        NameQuestionState.insert_and_handle_button(self)

    def display(self, callback: types.CallbackQuery):
        bot.send_message(self.chat_id, self.text, reply_markup=self.keyboard)


# State 2.
class NameQuestionState(BasicState):
    text = QUESTION_NAME_TEXT
    button_title_get_this_state = 'Fill out a Questionnaire?'
    callback_for_state = "getstate:NameQuestionState"

    def __init__(self, chat_id):
        super().__init__(chat_id)

    def display(self, message: types.Message):
        logger.info(f"State: {self.__class__.__name__} | Method: display")
        bot.send_message(self.chat_id, self.text, reply_markup=self.keyboard)


# State 3.
class PhoneQuestionState(BasicState):
    text = QUESTION_PHONE_TEXT

    def __init__(self, chat_id):
        super().__init__(chat_id)

    def display(self, message: types.Message):
        logger.info(f"State: {self.__class__.__name__} | Method: display")
        bot.send_message(self.chat_id, self.text, reply_markup=self.keyboard)


# State 4.
class VariantsQuestionState(BasicState):
    text = QUESTION_WITH_VARS_TEXT
    buttons_click_default_state = {"Button 1": False, "Button 2": False, "Button 3": False, "Button 4": False, }
    callback_for_state = "getstate:VariantsQuestionState"

    def __init__(self, chat_id):
        super().__init__(chat_id)
        from bot_app.buttons import BUTTONS_QUIZ_TEMPLATE
        self.keyboard_quiz_values = BUTTONS_QUIZ_TEMPLATE
        self.buttons_state: dict = self.buttons_click_default_state
        self.keyboard = self.get_quiz_keyboard_markup()
        self.handlers.append(lambda msg: AnswersConfirmationState.handler_callback_to_state(msg))
        self.handlers.append(lambda msg: WelcomeState.handler_callback_to_state(msg))

    # Depends on current "buttons_state", forms quiz keyboard markup
    def get_quiz_keyboard_markup(self,) -> types.InlineKeyboardMarkup:
        keyboard_callback_buttons = []
        for button_name, button_value in self.buttons_state.items():
            if button_value is False:
                keyboard_callback_buttons.append(self.keyboard_quiz_values[button_name]['unpressed'])
            if button_value is True:
                keyboard_callback_buttons.append(self.keyboard_quiz_values[button_name]['pressed'])

        keyboard_callback_buttons.append([AnswersConfirmationState.button_next_state()])
        keyboard_callback_buttons.append([WelcomeState.button_next_state()])
        keyboard_markup = types.InlineKeyboardMarkup(keyboard_callback_buttons)

        return keyboard_markup

    def display(self, message: types.Message):
        bot.reply_to(message, self.text, reply_markup=self.keyboard)


# State 5.
class AnswersConfirmationState(BasicState):
    text = ANSWER_CONFIRM_TEXT
    button_title_get_this_state = 'CONFIRM'
    callback_for_state = "getstate:AnswersConfirmationState"

    def __init__(self, chat_id=None):
        super().__init__(chat_id)
        AnswersProcessState.insert_and_handle_button(self)
        WelcomeState.insert_and_handle_button(self)

    def display(self, message: types.Message or types.CallbackQuery):
        bot.send_message(self.chat_id, "Вы ответили на все вопросы.", reply_markup=self.keyboard)
        logger.warning(f"Currently, use if this method is not provided: {self.__class__.__name__} | Method: display")

    def display_and_confirm(self, message: types.Message or types.CallbackQuery, user: "UserCredentials"):
        bot.send_message(self.chat_id, "You have answered all questions.\n"
                                       "Please, check your answers below.\n"
                                       f"Name: {user.name}\n"
                                       f"Phone number: {user.phone_num}\n"
                                       f"Selected answers: {', '.join(user.answers)}\n",
                         reply_markup=self.keyboard)


# State 6.
class AnswersProcessState(BasicState):
    text = ANSWER_PROCESS_TEXT
    button_title_get_this_state = 'Save Questionnaire results'
    callback_for_state = "getstate:AnswersProcessState"

    def __init__(self, chat_id=None):
        super().__init__(chat_id)
        WelcomeState.insert_and_handle_button(self)
        FinalState.insert_and_handle_button(self)

    def display(self, callback: types.Message or types.CallbackQuery):
        bot.send_message(callback.from_user.id,
                         f"Record by current chat ID({callback.from_user.id}) is already exist. "
                         f"You can finish work with a bot or restart this Questionnaire.", reply_markup=self.keyboard)


# State 7.
class FinalState(BasicState):
    text = FINAL_TEXT
    button_title_get_this_state = "Finish work"
    callback_for_state = "getstate:FinalState"

    def __init__(self, chat_id=None):
        super().__init__(chat_id)
        WelcomeState.insert_and_handle_button(self)

    def display(self, callback: types.Message or types.CallbackQuery):
        bot.send_message(callback.from_user.id,
                         self.text,
                         reply_markup=self.keyboard)
