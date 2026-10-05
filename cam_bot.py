import telebot
import cv2
import io
import time
import subprocess
from config import BOT_TOKEN, ALLOWED_USER_ID

bot = telebot.TeleBot(BOT_TOKEN)

def get_webcam_shot():
    # 0 — встроенная камера по умолчанию
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return None
    
    # Небольшая пауза, чтобы камера успела настроить экспозицию/баланс белого
    time.sleep(1.0)
    
    # Читаем пару кадров для стабилизации сенсора
    for _ in range(3):
        ret, frame = cap.read()
        
    cap.release() # Сразу освобождаем камеру
    
    if not ret:
        return None
        
    # Кодируем кадр в JPEG прямо в памяти без записи на диск
    _, buffer = cv2.imencode('.jpg', frame)
    return io.BytesIO(buffer)

@bot.message_handler(commands=['snap'])
def handle_snap(message):
    # Защита: реагируем только на ваш ID
    if message.from_user.id != ALLOWED_USER_ID:
        return

    bot.send_message(message.chat.id, "Делаю снимок...")
    photo = get_webcam_shot()
    
    if photo:
        photo.seek(0)
        bot.send_photo(message.chat.id, photo, caption="Кадр из комнаты")
    else:
        bot.send_message(message.chat.id, "Ошибка: не удалось получить доступ к камере.")


@bot.message_handler(commands=['shutdown'])
def handle_shutdown(message):
    if message.from_user.id != ALLOWED_USER_ID:
        return

    bot.send_message(
        message.chat.id,
        "Получена команда на выключение. Компьютер выключится через 30 секунд."
    )

    try:
        subprocess.run(["shutdown", "/s", "/f", "/t", "30"], check=True)
    except (subprocess.CalledProcessError, OSError) as exc:
        bot.send_message(message.chat.id, f"Ошибка запуска выключения: {exc}")


if __name__ == '__main__':
    print("Бот запущен. Нажмите Ctrl+C для остановки.")
    bot.infinity_polling()