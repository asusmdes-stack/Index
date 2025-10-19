import os
import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import LabeledPrice
from fastapi import FastAPI, Request

BOT_TOKEN = os.getenv("BOT_TOKEN")
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://telega-nine.vercel.app")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dp.message(commands=["start"])
async def start_command(message: types.Message):
    """Кнопка для открытия мини-приложения"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    webapp_button = types.KeyboardButton(
        text="💫 Открыть Mini App",
        web_app=types.WebAppInfo(url=FRONTEND_URL)
    )
    keyboard.add(webapp_button)
    await message.answer(
        "👋 Привет! Это бот для оплаты услуги 5 ⭐\n"
        "Нажми кнопку ниже, чтобы открыть Mini App:",
        reply_markup=keyboard
    )


async def send_stars_invoice(chat_id: int, payload: dict):
    """Создание инвойса для оплаты в Telegram Stars"""
    title = "Оплата услуги — 5 ⭐"
    description = "Спасибо за использование сервиса!"
    currency = "XTR"
    amount_stars = int(payload.get("amount_stars", 5))
    prices = [LabeledPrice(label="Оплата услуги", amount=amount_stars)]

    invoice_payload = json.dumps({
        "uid": chat_id,
        "ts": payload.get("timestamp"),
        "type": "telegram_stars"
    })

    await bot.send_invoice(
        chat_id=chat_id,
        title=title,
        description=description,
        payload=invoice_payload,
        provider_token="",  # не нужен для XTR
        currency=currency,
        prices=prices
    )


@dp.message()
async def handle_message(message: types.Message):
    """Обработка данных из Mini App"""
    if message.web_app_data:
        try:
            data = json.loads(message.web_app_data.data)
        except Exception as e:
            logger.error(f"Ошибка JSON: {e}")
            await message.answer("Ошибка: неверные данные.")
            return

        if data.get("action") == "request_payment":
            await message.answer("Создаю инвойс на оплату 5 ⭐ ...")
            await send_stars_invoice(message.chat.id, data)
            return

    if message.text and message.text.startswith("/start"):
        await start_command(message)


@dp.pre_checkout_query()
async def pre_checkout(pre_checkout: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)


@dp.message(content_types=[types.ContentType.SUCCESSFUL_PAYMENT])
async def successful_payment(message: types.Message):
    payment = message.successful_payment
    logger.info(f"✅ Payment success: {payment.to_python()}")
    await message.answer("✅ Платёж получен, спасибо!")


@app.post("/api/webhook/{token}")
async def webhook(request: Request, token: str):
    """Основной endpoint для Telegram webhook"""
    if token != BOT_TOKEN:
        return {"ok": False, "error": "Unauthorized"}

    update = types.Update(**await request.json())
    await dp.process_update(update)
    return {"ok": True}


@app.get("/")
async def index():
    return {"ok": True, "info": "Telegram Stars Bot is running."}
