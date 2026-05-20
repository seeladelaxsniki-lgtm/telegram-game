import asyncio
from aiogram import Bot, Dispatcher, types

TOKEN = "8749530424:AAGizeCaRJl1ReRkI-1j8Lefy0neB0Wh8o4"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def start(msg: types.Message):
    await msg.answer("🚀 Bot live")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())