const tg = window.Telegram.WebApp;
tg.ready();  // Init WebApp
tg.expand(); // Fullscreen

const payButton = document.getElementById('payButton');
const status = document.getElementById('status');

const BOT_WEBHOOK_URL = 'https://bot-server.vercel.app/api/create_invoice';  // Эндпоинт бота для инвойса (добавь в bot-server)

payButton.addEventListener('click', async () => {
    status.textContent = 'Генерируем инвойс...';
    payButton.disabled = true;

    // Отправляем запрос боту via WebApp data (payload='buy_5_stars')
    tg.sendData(JSON.stringify({ action: 'create_invoice', amount: 5 }));

    // Альтернатива: Fetch к боту для invoice link (если добавишь API в bot-server)
    // try {
    //     const response = await fetch(BOT_WEBHOOK_URL, { method: 'POST', body: JSON.stringify({user_id: tg.initDataUnsafe.user.id, amount: 5}) });
    //     const { invoice_link } = await response.json();
    //     tg.openInvoice(invoice_link, (status) => {
    //         if (status === 'paid') {
    //             status.textContent = 'Оплата успешна!';
    //             tg.close();
    //         } else {
    //             status.textContent = 'Оплата отменена.';
    //         }
    //     });
    // } catch (err) {
    //     status.textContent = 'Ошибка: ' + err.message;
    // }

    payButton.disabled = false;
});

// Event после оплаты (если via openInvoice)
tg.onEvent('invoiceClosed', ({ url, status }) => {
    if (status === 'paid') {
        status.textContent = 'Спасибо за оплату!';
        tg.HapticFeedback.notificationSuccess();
        setTimeout(() => tg.close(), 2000);
    } else {
        status.textContent = 'Оплата не удалась.';
    }
});

// Тема
document.body.style.backgroundColor = tg.themeParams.bg_color;
