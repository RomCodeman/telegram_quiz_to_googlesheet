import time

from telebot import types

from bot_app.logger import logger
from bot_app.models import UserDataDB
from bot_app.sheets.sheets_class import QuestionnaireSheet
from bot_app.sheets.sheets_class import UserCredentials
from bot_app.states import (WelcomeState, NameQuestionState, PhoneQuestionState, VariantsQuestionState,
                            AnswersConfirmationState, AnswersProcessState, LaunchState, FinalState)
from config import bot

# For operational states and user data storing
users_states_current: dict = {}  # {"chat_id": {"state_last": "BasicState", "user": "user_instance"}}


# State 1. LaunchState. Creates common variables and display LaunchState
@bot.message_handler(commands=['start'])
def bot_launch(message: types.Message):
    chat_id = message.chat.id

    # State entry point definition
    state_current = LaunchState(chat_id)
    logger.info(f" Current state: {state_current.__class__.__name__}")

    # Instance for user data storing
    user_instance = UserCredentials(chat_id)
    # Save login to user instance
    user_instance.login = message.from_user.username

    # Store current state as a last state and user_instance
    users_states_current[chat_id] = {"state_last": state_current, "user": user_instance}

    bot.send_chat_action(chat_id, 'typing')
    time.sleep(2)

    # Display current state to the client
    state_current.display(message)


# State 1.1. WelcomeState. Use's in 'RESTART' cases. (Like LaunchState, but with last state handling)
@bot.callback_query_handler(func=lambda callback: True if WelcomeState.callback_for_state == callback.data else False)
def send_welcome(callback: types.CallbackQuery):
    chat_id = callback.from_user.id

    if isinstance(users_states_current[chat_id]["state_last"], FinalState):
        pass  # "Welcome again" text and logic (UPDATE record in DB's)

    # Clear last state InlineKeyboard markup
    try:
        bot.edit_message_reply_markup(chat_id, callback.message.message_id, reply_markup=None)
    except Exception as e:
        logger.error(e)

    # Last state processing stage (in development)
    state_last: VariantsQuestionState = users_states_current[chat_id]["state_last"]
    logger.info(f" Last state was: {state_last.__class__.__name__}")

    # State entry point definition
    state_current = WelcomeState(chat_id)
    logger.info(f" Current state: {state_current.__class__.__name__}")

    # Instance for user data storing
    user_instance = UserCredentials(chat_id)
    # Save login to user instance
    user_instance.login = callback.from_user.username

    # Store current state as a last state and user_instance
    users_states_current[chat_id] = {"state_last": state_current, "user": user_instance}

    bot.send_chat_action(chat_id, 'typing')
    time.sleep(2)

    # Display current state to the client
    state_current.display(callback)


# State 2. NameQuestionState. Asks for name and go to next state, after it.
@bot.callback_query_handler(
    func=lambda callback: True if callback.data == NameQuestionState.callback_for_state else False)
def name_ask_step(callback: types.CallbackQuery):
    chat_id = callback.from_user.id

    # Clear last state InlineKeyboard markup
    try:
        bot.edit_message_reply_markup(chat_id, callback.message.message_id, reply_markup=None)
    except Exception as e:
        logger.error(e)

    # Last state processing stage (in development)
    state_last: LaunchState or WelcomeState = users_states_current[chat_id]["state_last"]

    # Current state entry point by callback processing
    state_current: NameQuestionState
    state_current = users_states_current[chat_id]["state_last"] = state_last.process_with_callback_handlers(callback)
    logger.info(f" Current state: {state_current.__class__.__name__}")

    bot.send_chat_action(chat_id, 'typing')
    time.sleep(2)

    # Waiting for a name from client
    response_from_user = bot.send_message(chat_id, f"{NameQuestionState.text}")

    # Next state registering
    bot.register_next_step_handler(response_from_user, phone_ask_step)


# State 3. PhoneQuestionState. Stores response with name from last state.
# Asks for a phone_num and go to next state, after it.
def phone_ask_step(message: types.Message):
    chat_id = message.chat.id

    # Storing name
    user_name = message.text
    users_states_current[chat_id]['user'].name = user_name
    logger.info(f"USER_NAME is: {users_states_current[chat_id]['user'].name}")

    # Current state entry point
    state_current: PhoneQuestionState
    state_current = users_states_current[chat_id]["state_last"] = PhoneQuestionState(chat_id)
    logger.info(f" Current state: {state_current.__class__.__name__}")

    bot.send_chat_action(chat_id, 'typing')
    time.sleep(2)

    # Waiting for a phone_num from client
    response_from_user: types.Message = bot.reply_to(message, f"{state_current.text}")
    # Next state registering
    bot.register_next_step_handler(response_from_user, variants_question_step)


# State 4. VariantsQuestionState. Stores response with phone_num from last state.
# Propose choices with InlineKeyboard.
def variants_question_step(message: types.Message):
    chat_id = message.chat.id

    # Storing phone_num
    user_phone_num = message.text
    users_states_current[chat_id]['user'].phone_num = user_phone_num
    logger.info(f"USER_PHONE_NUM is: {users_states_current[chat_id]['user'].phone_num}")

    # Current state entry point
    state_current: VariantsQuestionState
    state_current = users_states_current[chat_id]["state_last"] = VariantsQuestionState(chat_id)
    logger.info(f" Current state: {state_current.__class__.__name__}")

    # Default buttons state for keyboard with choices
    variants_buttons_state_default = {"Button 1": False, "Button 2": False, "Button 3": False, "Button 4": False}

    # Reset buttons state to default.
    state_current.buttons_state = variants_buttons_state_default

    bot.send_chat_action(chat_id, 'typing')
    time.sleep(2)

    # Display current state to the client
    state_current.display(message)


# State 4.1. VariantsQuestionState.keyboard quiz callback handler
@bot.callback_query_handler(func=lambda callback: True if "click" in callback.data else False)
def callback_click_handler(callback: types.CallbackQuery):
    chat_id = callback.from_user.id
    button_callback = callback.data

    # State entry point obtain from last state
    state_current: VariantsQuestionState = users_states_current[chat_id]["state_last"]

    user_instance: UserCredentials = users_states_current[chat_id]["user"]

    # Switches quiz buttons state after it's callback
    index_end = button_callback.find(":") + 1
    button_name = f"Button {button_callback[index_end:]}"
    last_button_state = state_current.buttons_state[button_name]
    state_current.buttons_state[button_name] = not last_button_state

    # Stores current state with new quiz buttons state
    users_states_current[chat_id]["state_last"] = state_current
    logger.info(f"'click' action. Current quiz buttons state: {state_current.buttons_state}")

    # Store 'clicked' button names to user.answers and then user instance to users_states_current
    #  by it's chat ID
    buttons_pressed = []
    for bt_name, bt_value in state_current.buttons_state.items():
        if bt_value:
            buttons_pressed.append(bt_name)
    user_instance.answers = buttons_pressed
    users_states_current[chat_id]["user"] = user_instance

    time.sleep(1)

    # Display state_current.keyboard with new quiz buttons_state
    bot.edit_message_reply_markup(chat_id, callback.message.message_id,
                                  reply_markup=state_current.get_quiz_keyboard_markup())


# State 5. AnswersConfirmationState. Shows stored user data for Confirmation
@bot.callback_query_handler(
    func=lambda callback: True if AnswersConfirmationState.callback_for_state in callback.data else False)
def callback_state_handler(callback: types.CallbackQuery):
    chat_id = callback.from_user.id

    if users_states_current.get(chat_id, False):
        state_last: VariantsQuestionState = users_states_current[chat_id]["state_last"]
        logger.info(f" Last state: {state_last.__class__.__name__}")
    else:
        state_last: WelcomeState = WelcomeState(chat_id)
        new_state = state_last
        logger.info(f" Last state was not found. New state: {new_state.__class__.__name__}")

    # State entry point obtain from callback handlers
    state_current: AnswersConfirmationState or WelcomeState
    state_current = users_states_current[chat_id]["state_last"] = state_last.process_with_callback_handlers(callback)
    users_states_current[chat_id]["state_last"] = state_current
    logger.info(f" Current state: {state_current.__class__.__name__}")

    if isinstance(state_current, AnswersConfirmationState):
        user_instance = users_states_current[chat_id]['user']

        bot.send_chat_action(chat_id, 'typing')
        time.sleep(2)

        state_current.display_and_confirm(callback, user_instance)
    elif isinstance(state_current, WelcomeState):
        bot.send_chat_action(chat_id, 'typing')
        time.sleep(2)

        state_current.display(callback)

    # Clear last state InlineKeyboard markup
    try:
        bot.edit_message_reply_markup(chat_id, callback.message.message_id, reply_markup=None)
    except Exception as e:
        logger.error(e)


# State 6. AnswersProcessState. Write data, stored in users_states_current to google sheets and DB-file
@bot.callback_query_handler(
    func=lambda callback: True if AnswersProcessState.callback_for_state in callback.data else False)
def answers_process(callback: types.CallbackQuery):
    chat_id = callback.from_user.id

    # Clear last state InlineKeyboard markup
    try:
        bot.edit_message_reply_markup(chat_id, callback.message.message_id, reply_markup=None)
    except Exception as e:
        logger.error(e)

    # Last state processing stage (in development)
    state_last: AnswersConfirmationState = users_states_current[chat_id]["state_last"]

    # State entry point obtain from callback handlers
    state_current: AnswersProcessState
    state_current = users_states_current[chat_id]["state_last"] = state_last.process_with_callback_handlers(callback)
    users_states_current[chat_id]["state_last"] = state_current
    logger.info(f" Current state: {state_current.__class__.__name__}")

    # Get last user data stored in users_states_current
    user_instance: UserCredentials = users_states_current[chat_id]["user"]

    # Save stored user data to Google sheets
    try:
        QuestionnaireSheet(user_instance).save_to_sheet()
        bot.send_chat_action(chat_id, 'typing')
        time.sleep(2)
        bot.send_message(chat_id, "Data saved to the Google Sheets.")
        logger.info(f"Saved to the google sheets: {user_instance}")
    except Exception as e:
        bot.send_chat_action(chat_id, 'typing')
        time.sleep(2)
        bot.send_message(chat_id, "Ooops. Data was not saved to the Google Sheets.")
        logger.error(e)

    # Adding new record to the DB
    user_data_db, created, chat_id_unique = UserDataDB.add_to_db(chat_id, user_instance,
                                                                 filtered_set=UserDataDB.filter_chat_id(chat_id))
    if user_data_db and created and chat_id_unique:
        bot.send_chat_action(chat_id, 'typing')
        time.sleep(2)

        bot.send_message(chat_id, "Data was saved to the DB.")
        logger.info(f"Data was saved to the DB.")
    if user_data_db and created and not chat_id_unique:
        bot.send_chat_action(chat_id, 'typing')
        time.sleep(2)

        bot.send_message(chat_id, "Ooops. Current chat ID, already in a DB. "
                                  "We have added new record with the same chat ID to the DB")
        logger.warning(f"Current chat ID({chat_id}), already in a DB. "
                       f"Added new record with the same chat ID to the DB.")
    if user_data_db and not created and not chat_id_unique:
        bot.send_chat_action(chat_id, 'typing')
        time.sleep(2)

        bot.send_message(chat_id, "Ooops. You already have the same record in a DB. "
                                  "You can restart bot, for a new try or leave previous record without changes.")
        logger.warning(f"The same record already in a DB.")

    # State entry point definition
    state_next = FinalState(chat_id)
    bot.send_message(chat_id, state_next.text, reply_markup=state_next.keyboard)


# State 7. FinalState. Thanks for the passing of the Questioning and propose 'restart' this Questioning
@bot.callback_query_handler(func=lambda callback: True if FinalState.callback_for_state in callback.data else False)
def finalizing(callback: types.CallbackQuery):
    chat_id = callback.from_user.id

    # Last state processing stage (in development)
    state_last: AnswersProcessState = users_states_current[chat_id]["state_last"]

    # State entry point obtain from callback handlers
    state_current: FinalState
    state_current = users_states_current[chat_id]["state_last"] = state_last.process_with_callback_handlers(callback)
    users_states_current[chat_id]["state_last"] = state_current
    logger.info(f" Current state: {state_current.__class__.__name__}")

    bot.send_chat_action(chat_id, 'typing')
    time.sleep(2)

    # Display current state to the client
    state_current.display(callback)
