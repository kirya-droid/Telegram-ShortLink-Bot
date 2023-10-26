from aiogram import Bot, Dispatcher, executor, types
from main import fastlink
API_TOKEN = 'Your token'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
   await message.reply("Send the link for the abbreviation:")

@dp.message_handler()
async def echo(message: types.Message):
   await message.answer(fastlink(message.text))


if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)