from telebot import types

# Custom buttons

# quiz buttons (pressed/unpressed states)
emoji_checkmark = u"\U00002714"
BUTTONS_QUIZ_TEMPLATE = {
    "Button 1": {'pressed': [types.InlineKeyboardButton(f"Button 1{emoji_checkmark}", callback_data='click:1')],
                 'unpressed': [
                     types.InlineKeyboardButton(f"Button 1", callback_data='click:1')]},
    "Button 2": {'pressed': [types.InlineKeyboardButton(f"Button 2{emoji_checkmark}", callback_data='click:2')],
                 'unpressed': [
                     types.InlineKeyboardButton(f"Button 2", callback_data='click:2')]},
    "Button 3": {'pressed': [types.InlineKeyboardButton(f"Button 3{emoji_checkmark}", callback_data='click:3')],
                 'unpressed': [
                     types.InlineKeyboardButton(f"Button 3", callback_data='click:3')]},
    "Button 4": {'pressed': [types.InlineKeyboardButton(f"Button 4{emoji_checkmark}", callback_data='click:4')],
                 'unpressed': [
                     types.InlineKeyboardButton(f"Button 4", callback_data='click:4')]},
    }