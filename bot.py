import os
from datetime import datetime
from telegram import Update, LabeledPrice, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, PreCheckoutQueryHandler, MessageHandler, filters, CallbackQueryHandler

# === Конфигурация ===
BOT_TOKEN = os.environ.get("BOT_TOKEN")
LOG_CHAT_ID = int(os.environ.get("LOG_CHAT_ID", "0"))
OWNER_ID = int(os.environ.get("OWNER_ID", "0"))

if not BOT_TOKEN:
    raise SystemExit("❌ Error: BOT_TOKEN environment variable is required.")

# === Команды ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    now = datetime.utcnow().strftime("%Y-m-d %H:%M:%S UTC")

    if update.message:
        # ✅ КНОПКА ОПЛАТЫ Stars
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("⭐ Оплатить 10 Stars", callback_data="pay_10")]
        ])
        
        await update.message.reply_text(
            "🤖 Dualis Robot greets you!\n"
            "It invites you to learn more about its services in the app.\n\n"
            "💰 Получите премиум за 10 Stars:",
            reply_markup=keyboard
        )

    # Логирование входа
    if user.id != OWNER_ID and LOG_CHAT_ID:
        text = (
            f"📥 Новый вход:\n"
            f"🆔 ID: {user.id}\n"
            f"👤 Имя: {user.first_name or '—'}\n"
            f"💬 Username: @{user.username or '—'}\n"
            f"🕒 Время: {now}"
        )
        await context.bot.send_message(chat_id=LOG_CHAT_ID, text=text)

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🍀")

# ✅ Кнопка оплаты
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "pay_10":
        prices = [LabeledPrice("Премиум доступ", 10)]
        
        await context.bot.send_invoice(
            chat_id=query.from_user.id,
            title="⭐ Премиум в Dualis",
            description="Доступ к расширенным функциям Mini App",
            payload=f"premium|{query.from_user.id}|dualis_mini_app",
            provider_token="",  # Пусто для Stars
            currency="XTR",
            prices=prices
        )

# ✅ Подтверждение оплаты
async def pre_checkout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)

# ✅ Успешная оплата
async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    payment = update.message.successful_payment
    payload = payment.invoice_payload
    
    if payload.startswith('premium|'):
        _, user_id_str, source = payload.split('|', 2)
        user_id = int(user_id_str)
        
        text = (
            f"✅ ⭐ ОПЛАТА ИЗ MINI APP!\n\n"
            f"🆔 Пользователь: {user_id}\n"
            f"💰 Сумма: {payment.total_amount} Stars\n"
            f"📱 Источник: {source}\n"
            f"🆔 Charge: {payment.telegram_payment_charge_id}"
        )
        
        await context.bot.send_message(chat_id=LOG_CHAT_ID, text=text)
        
        await update.message.reply_text(
            f"🎉 Спасибо за {payment.total_amount} Stars!\n"
            "Премиум активирован! ⭐"
        )

# === Запуск POLLING ===
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # ✅ ВСЕ ХЕНДЛЕРЫ
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CallbackQueryHandler(button_handler, pattern="^pay_"))
    app.add_handler(PreCheckoutQueryHandler(pre_checkout_callback))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))
    
    print("🚀 POLLING + Stars запущен!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()  # ✅ ИСПРАВЛЕНО: main(), не main
