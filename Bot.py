import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

TOKEN = "8749530424:AAGizeCaRJl1ReRkI-1j8Lefy0neB0Wh8o4"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def handler(message: Message):
    if message.text == "/start":
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎮 Открыть игру",
                    web_app=WebAppInfo(url="https://telegram-game-eqtt.onrender.com/")
                )
            ]
        ])

        await message.answer(
            "👋 Добро пожаловать в игру BTC Clicker!",
            reply_markup=kb
        )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())