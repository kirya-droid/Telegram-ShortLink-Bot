import asyncio
import logging
import sys
from os import getenv
from typing import Any, Dict

from keyboard.linkShortServices import menu, get_keyboard

from main import yandex_link, tinyurl_link, isgd_link
from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove, InlineKeyboardButton, CallbackQuery,
)
from aiogram.utils.keyboard import KeyboardBuilder

TOKEN ="Your token"

form_router = Router()


class Form(StatesGroup):
    subscribe = State()
    link_selection = State()
    send_link = State()


@form_router.message(CommandStart())
async def command_start( message: Message, state: FSMContext, bot: Bot) -> None:
    await state.set_state(Form.subscribe)
    channel_id = "-1001948011572"

    # Проверка подписки на канал
    status = await bot.get_chat_member(chat_id=channel_id, user_id=message.from_user.id)

    if status.status not in ["member", "administrator", "creator"]:
        await message.answer("Чтобы воспользоваться ботом, пожалуйста, подпишитесь на наш канал: " + "https://t.me/yogandhealthy")
    else:
        await message.answer(
            "Выберите формат ссылки: ",
            reply_markup=get_keyboard(),
        )
        await state.set_state(Form.link_selection)


@form_router.callback_query(F.data == "yandex")
async def yandex(query: CallbackQuery, state: FSMContext, bot: Bot):
    await state.update_data(service="yandex")
    await bot.send_message(query.message.chat.id, "Пришлите ссылку:")
    await state.set_state(Form.send_link)

@form_router.callback_query(F.data == "tinyurl")
async def tinyurl(query: CallbackQuery, state: FSMContext, bot: Bot):
    await state.update_data(service="tinyurl")
    await bot.send_message(query.message.chat.id, "Пришлите ссылку:")
    await state.set_state(Form.send_link)

@form_router.callback_query(F.data == "isgd")
async def tinyurl(query: CallbackQuery, state: FSMContext, bot: Bot):
    await state.update_data(service="isgd")
    await bot.send_message(query.message.chat.id, "Пришлите ссылку:")
    await state.set_state(Form.send_link)


@form_router.message(Form.send_link)
async def send_link(message: Message, state: FSMContext, bot: Bot):
    data = await state.update_data(link=message.text)
    if data['service'] == "yandex":
        send_func = yandex_link(data['link'])
    elif data['service'] == "tinyurl":
        send_func = tinyurl_link(data['link'])
    else:
        send_func = isgd_link(data['link'])
    print(data['service'])
    await bot.send_message(message.chat.id, f"<code>{send_func}</code>", reply_markup=menu(data['service']))


@form_router.message(Command("cancel"))
@form_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )

@form_router.callback_query(F.data == "format")
async def select_format(query: CallbackQuery, state: FSMContext, bot: Bot):
    await command_start(message=query.message, state=state, bot=bot)


async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(form_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())