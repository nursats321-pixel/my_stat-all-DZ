import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from dotenv import load_dotenv
from aiogram.types import (
        Message,
        ReplyKeyboardMarkup,
        KeyboardButton, 
        InlineKeyboardMarkup,
        InlineKeyboardButton
)


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()


keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Товары"),
            KeyboardButton(text="заказ")

        ],
        [
            KeyboardButton(text="Профиль")
        ]
    ],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Привет! Выбери действие",
        reply_markup=keyboard
        )


@dp.message()
async def message_handler(message: Message):

    if message.text == "Товары":
        products = [
            "IPHONE 13 Стекло - 1000тг",
            "Type-C кабель - 1000тг",
            "Зарядка 20W - 2000тг"
        ]

        text = "наши товары:\n\n"

        for i, product in enumerate(products, start=1):
            text += f"{i}. {product}\n"

        await message.answer(text)

       
    elif message.text == "Заказ":
       await message.answer("здесь можно будет оформлять заказ")

    elif message.text == "Профиль":
       await message.answer(
           f"Твой Телеграмм ID: {message.from_user.id}"
       )

    else:
       await message.answer(
           f"Ты написал: {message.text}"
       )


async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())