import asyncio
import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

TOKEN = "8749530424:AAGizeCaRJl1ReRkI-1j8Lefy0neB0Wh8o4"

bot = Bot(token=TOKEN)
dp = Dispatcher()

WEBAPP_URL = "https://YOUR-RENDER-URL.onrender.com"

def menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🎮 Play BTC Game",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ])

@dp.message()
async def start(msg: types.Message):
    await msg.answer("🚀 BTC Clicker Game", reply_markup=menu())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())