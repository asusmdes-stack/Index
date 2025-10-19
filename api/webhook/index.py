from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, PreCheckoutQuery, SuccessfulPayment, WebAppData, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from aiogram.filters import Command
from fastapi import FastAPI, Request
import asyncio
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    webapp_button = KeyboardButton(
        text="💫 Открыть Mini App",
        web_app=WebAppInfo(url="https://telega-nine.vercel.app")
    )
    keyboard.add(webapp_button)
    await message.answer("Нажми кнопку, чтобы открыть Mini App 💫", reply_markup=keyboard)

@dp.message(F.web_app_data)
async def handle_webapp_data(message: Message):
    data = message.web_app_data.data
    if '"action": "pay"' in data:
        await bot.send_invoice(
            chat_id=message.chat.id,
            title="Услуга Mini App",
            description="Оплата услуги через Telegram Stars",
            payload="stars_payment",
            provider_token="",  # пусто для Telegram Stars (XTR)
            currency="XTR",
            prices=[{"label": "Услуга", "amount": 5}]
        )

@dp.pre_checkout_query()
async def pre_checkout_query(pre_checkout: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)

@dp.message(F.successful_payment)
async def successful_payment(message: Message):
    await message.answer("✅ Платёж через Stars успешно выполнен!")

# --- FASTAPI WRAPPER ---
app = FastAPI()

@app.post("/api/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = dp._parse_update(data)
    await dp.feed_update(bot, update)
    return {"ok": True}
