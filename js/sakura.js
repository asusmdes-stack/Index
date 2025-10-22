// ИНИЦИАЛИЗАЦИЯ
window.Telegram.WebApp.ready();
window.Telegram.WebApp.expand();

// МАТРИЦА НЕОН
const canvas = document.getElementById('matrix');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const matrix = "サクラハナミ".repeat(50).split("");
const fontSize = 14;
const columns = canvas.width / fontSize;
const drops = Array(Math.floor(columns)).fill(1);

function drawMatrix() {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = '#ff0000';
    ctx.font = fontSize + 'px monospace';
    
    drops.forEach((y, i) => {
        const text = matrix[Math.floor(Math.random() * matrix.length)];
        ctx.fillText(text, i * fontSize, y * fontSize);
        
        if (y * fontSize > canvas.height && Math.random() > 0.975) {
            drops[i] = 0;
        }
        drops[i]++;
    });
}

setInterval(drawMatrix, 50);

// 6 ЦВЕТОВ САКУРЫ
const sakuraColors = [
    { 
        color: '#ffffff', name: '🌸 Белая', 
        poem: 'В тишине ночной, лепестки чисты,', 
        advice: 'Сердце свободно. Новые встречи ждут через 7 дней!'
    },
    { 
        color: '#ff69b4', name: '🌷 Розовая', 
        poem: 'Под луной цветы любви расцветают,', 
        advice: 'Страсть близко! Встреча с судьбой в ближайшие 3 дня!'
    },
    { 
        color: '#ff0000', name: '🌺 Красная', 
        poem: 'Огонь страсти в лепестках пылает,', 
        advice: 'Желания исполнятся! Действуй смело сегодня!'
    },
    { 
        color: '#8a2be2', name: '🥀 Фиолетовая', 
        poem: 'Тайны ночи в цветах скрыты,', 
        advice: 'Секрет откроется. Доверяй интуиции ближайшие 5 дней!'
    },
    { 
        color: '#ffd700', name: '💛 Жёлтая', 
        poem: 'Солнце счастья в лепестках сияет,', 
        advice: 'Удача рядом! Финансовый прорыв через 10 дней!'
    },
    { 
        color: '#4169e1', name: '🌼 Синяя', 
        poem: 'Спокойствие вод в цветах таится,', 
        advice: 'Время размышлений. Решение придёт через 14 дней.'
    }
];

// АНАЛИЗ ВОПРОСА
function analyzeQuestion(question) {
    const love = ['любовь', 'парень', 'девушка', 'чувства', 'отношения'];
    const money = ['деньги', 'работа', 'карьера', 'бизнес'];
    const health = ['здоровье', 'болезнь', 'энергия'];
    
    if (love.some(w => question.toLowerCase().includes(w))) return 1; // Розовая
    if (money.some(w => question.toLowerCase().includes(w))) return 4; // Жёлтая
    if (health.some(w => question.toLowerCase().includes(w))) return 5; // Синяя
    return Math.floor(Math.random() * 6); // Случайный
}

// ИСПРАВЛЕННАЯ ГЛАВНАЯ КНОПКА (10 STARS + РЕЗУЛЬТАТ!)
document.getElementById('gadanieBtn').onclick = () => {
    const question = document.getElementById('question').value.trim();
    if (!question) {
        alert('❓ Задай вопрос!');
        return;
    }
    
    // 1. ПОКАЗЫВАЕМ АНИМАЦИЮ
    document.getElementById('gadanieBtn').textContent = '🌸 РАСКРЫВАЮ...';
    document.getElementById('gadanieBtn').disabled = true;
    
    // 2. ОТКРЫВАЕМ ИНВОЙС 10 STARS
    window.Telegram.WebApp.openInvoice(
        'sakura|' + window.Telegram.WebApp.initDataUnsafe.user.id + '|sakura_app', 
        10
    );
    
    // 3. СИМУЛЯЦИЯ ОПЛАТЫ (3 СЕКУНДЫ ПОЗЖЕ)
    setTimeout(() => {
        showSakuraResult(question);
        document.getElementById('gadanieBtn').textContent = '🔴 РАСКРЫТЬ САКУРУ';
        document.getElementById('gadanieBtn').disabled = false;
    }, 3000);
};

// НОВАЯ ФУНКЦИЯ РЕЗУЛЬТАТА
function showSakuraResult(question) {
    const colorIndex = analyzeQuestion(question);
    const color = sakuraColors[colorIndex];
    
    document.getElementById('sakuraColor').style.background = color.color;
    document.getElementById('colorName').textContent = color.name;
    document.getElementById('poem').textContent = color.poem;
    document.getElementById('advice').textContent = color.advice;
    document.getElementById('result').classList.remove('hidden');
    
    // ВИБРАЦИЯ TELEGRAM
    window.Telegram.WebApp.HapticFeedback.notificationOccurred('success');
}

// КНОПКА STARS (ДОПОЛНИТЕЛЬНАЯ)
document.getElementById('starsBtn').onclick = () => {
    window.Telegram.WebApp.openInvoice(
        'sakura|' + window.Telegram.WebApp.initDataUnsafe.user.id + '|sakura_app', 
        10
    );
};

// SHARE
function shareResult() {
    const user = window.Telegram.WebApp.initDataUnsafe.user;
    const colorName = document.getElementById('colorName').textContent;
    const poem = document.getElementById('poem').textContent;
    const text = `🌸 Моя Сакура Судьбы: ${colorName}\n"${poem}"\n\nПопробуй своё! t.me/${user.username}`;
    
    window.Telegram.WebApp.openTelegramLink(`https://t.me/share/url?url=${encodeURIComponent(window.Telegram.WebApp.initDataUnsafe.start_param)}&text=${encodeURIComponent(text)}`);
}
