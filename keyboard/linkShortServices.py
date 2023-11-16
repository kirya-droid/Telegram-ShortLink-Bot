from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup



def get_keyboard():
    buttons = [
        [InlineKeyboardButton(text="clck.ru", callback_data="yandex")],
        [InlineKeyboardButton(text="tinyurl.com", callback_data="tinyurl")],
        [InlineKeyboardButton(text="is.gd", callback_data="isgd")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def menu(service):
    buttons = [
        [InlineKeyboardButton(text="Сократить еще одну ссылку", callback_data=f"{service}")],
        [InlineKeyboardButton(text="Изменить формат", callback_data="format")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
